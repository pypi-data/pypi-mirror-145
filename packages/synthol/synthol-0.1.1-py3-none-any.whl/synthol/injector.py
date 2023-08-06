import importlib
import inspect
import json
import logging
import os
import pkgutil
import sys
import time
from typing import cast, List, Callable, TypeVar, Type, Dict, Any, Tuple, Iterator, Optional, \
    Iterable

import tempfile
import typing_inspect

from synthol.context import InjectionContext
from synthol.provider import (
    AbstractInstanceProvider,
    StaticProvider,
    AutoFactoryProvider,
    DependencyValue,
)
from synthol.utils import get_provided_interfaces, get_type_label, is_built_in_type
from synthol.scope import AbstractInjectionScope

T = TypeVar("T")
LOGGER = logging.getLogger(__name__)
PYINSTALLER_INJECTOR_DIR = "dependency_injection"
PYINSTALLER_MODULES_FILE = "modules.json"
PYINSTALLER_MODULES: Optional[Dict[str, List[str]]] = None


class NotFoundError(Exception):
    pass


class DependencyInjector:
    def __init__(self):
        self._providers: Dict[Type, List[AbstractInstanceProvider]] = {}

    def bind(self, provider: AbstractInstanceProvider):
        """
        Bind an instance provider to the injector.

        If there is already a list of providers for the corresponding interface(s), the new provider is added with
        the highest priority (including if it's already in the list, in which case it's moved to have the highest
        priority).
        """
        for provided_interface in provider.get_provided_interfaces():
            existing_providers = self._providers.get(provided_interface, [])
            # Add the new provider with highest priority, removing it first if it already exists
            existing_providers = [ep for ep in existing_providers if ep != provider]
            existing_providers.append(provider)
            self._providers[provided_interface] = existing_providers

    def bind_instance(self, instance: Any):
        """
        Create and bind a new static provider to the injector.
        """
        self.bind(StaticProvider(get_provided_interfaces(type(instance)), instance))

    def bind_factory(
        self,
        factory: Callable[..., Any],
        scope: AbstractInjectionScope = None,
        **factory_kwargs,
    ):
        """
        Create and bind a new auto factory provider to the injector. The factory can be
        (sync/async) function, method or class.
        """
        self.bind(AutoFactoryProvider(factory, factory_kwargs, scope=scope))

    @staticmethod
    def _load_pyinstaller_modules_children():
        """
        Load the data structure that contains modules' children when running within a PyInstaller
        application
        """
        modules_path = os.path.join(
            sys._MEIPASS, PYINSTALLER_INJECTOR_DIR, PYINSTALLER_MODULES_FILE
        )
        if not os.path.isfile(modules_path):
            raise ValueError(
                "Cannot iterate child module sin a PyInstaller application that does not "
                "package a modules file created by the method `pyinstaller_discover`"
            )
        with open(modules_path, "r") as f:
            return json.load(f)

    @staticmethod
    def _iterate_child_modules(module) -> Iterator[Tuple[Any, bool]]:
        """
        Iterate over all the direct children of the module. If the child has not been imported yet,
        it is imported.
        """
        if not hasattr(module, "__path__"):
            return
        if hasattr(sys, "_MEIPASS"):
            global PYINSTALLER_MODULES
            # PyInstaller application
            if PYINSTALLER_MODULES is None:
                PYINSTALLER_MODULES = DependencyInjector._load_pyinstaller_modules_children()
            modules_names = PYINSTALLER_MODULES.get(module.__name__, [])
        else:
            modules_names = [
                name for _, name, _ in pkgutil.iter_modules(module.__path__, module.__name__ + ".")
            ]
        for module_name in modules_names:
            if module_name not in sys.modules:
                yield importlib.import_module(module_name), True
            else:
                yield sys.modules[module_name], False

    @staticmethod
    def _get_pyinstaller_discover_structure(module, structure: Dict[str, List[str]]):
        """
        Populate the dictionary structure so that the key is the module name and the value is a
        list of direct children name.
        :return:
        """
        children_names = []
        for child_module, _ in DependencyInjector._iterate_child_modules(module):
            children_names.append(child_module.__name__)
            DependencyInjector._get_pyinstaller_discover_structure(child_module, structure)
        if children_names:
            structure[module.__name__] = children_names

    @staticmethod
    def pyinstaller_discover(modules: List) -> Tuple[List[str], str]:
        """
        Run the same logic as discover but should be used when generating a pyinstaller bundle. It
        return a list of full module names and the path to a file that allows the normal discover
        method to run in a pyinstaller application. That file should be provided to the
        PyInstaller's Analysis constructor in the binaries argument. The target path in the tuple
        provided to the binaries argument should be set to 'dependency_injection.json'
        """
        module_names = []
        module_structure: Dict[str, List[str]] = {}
        for module in modules:
            module_names.extend(
                [
                    m.name
                    for m in pkgutil.walk_packages(
                        path=module.__path__, prefix=module.__name__ + "."
                    )
                ]
            )
            DependencyInjector._get_pyinstaller_discover_structure(module, module_structure)
        temp_path = tempfile.mkdtemp()
        with open(os.path.join(temp_path, PYINSTALLER_MODULES_FILE), "w") as f:
            json.dump(module_structure, f)
        return module_names, temp_path

    def discover(
        self,
        module,
        blacklisted_interfaces: Iterable[Type] = (),
        blacklisted_modules: Iterable[Any] = (),
        _depth: int = 0,
    ):
        """
        Recursively discover and bind non-abstract classes within the provided module. Modules
        that have not been imported yet are imported.
        """
        indent = "\t" * _depth
        start_time = time.time()
        blacklisted_interfaces = set(blacklisted_interfaces)
        blacklisted_modules = set(blacklisted_modules)

        for blacklisted_m in blacklisted_modules:
            if not inspect.ismodule(blacklisted_m):
                error_msg = f"Cannot blacklist {blacklisted_m} as it is not a valid Python module!"
                parent_module = inspect.getmodule(blacklisted_m)
                if parent_module is not None:
                    error_msg += (
                        f" Perhaps you meant to blacklist the module that it was imported from: "
                        f"{parent_module.__name__}"
                    )
                raise ValueError(error_msg)

        if module in blacklisted_modules:
            return

        if not inspect.ismodule(module):
            raise ValueError("The provided module is not a valid Python module")

        LOGGER.log(5, f"{indent}Discovering module {module.__name__}")
        # Import any child module so that it shows up in the inspect.getmembers call below.
        for child_module, was_imported in DependencyInjector._iterate_child_modules(module):
            if was_imported:
                LOGGER.log(5, f"{indent}\tImporting module {child_module.__name__}")
            # Recursively discover what's in the child module
            self.discover(child_module, blacklisted_interfaces, blacklisted_modules, _depth + 1)

        module_path = inspect.getfile(module)
        discovered_items = 0
        for name, child in inspect.getmembers(module):
            if name.startswith("__") and name.endswith("__"):
                continue
            try:
                if not inspect.getfile(child).startswith(module_path):
                    # Avoid function/classes that are not defined in the current module
                    continue
            except TypeError:
                # That can be raised for built-in object
                continue

            if not inspect.isclass(child) or inspect.isabstract(child):
                # If it's not a class, or it's an abstract class, ignore it
                continue
            class_interfaces = set(child.__mro__)
            child_blacklisted_interfaces = blacklisted_interfaces.intersection(class_interfaces)
            if child_blacklisted_interfaces:
                # One (or more) of the interfaces implemented by the class are blacklisted
                blacklist_str = [get_type_label(bi) for bi in child_blacklisted_interfaces]
                LOGGER.log(
                    5,
                    f"{indent}\tSkipping class {get_type_label(child)} because the interfaces "
                    f"{', '.join(blacklist_str)} are blacklisted",
                )
                continue
            LOGGER.log(5, f"{indent}\tDiscovered class {get_type_label(child)}")
            discovered_items += 1
            self.bind_factory(child)
        LOGGER.log(
            5,
            f"{indent}\tDiscovery of module {module.__name__} took {time.time() - start_time:.2f} "
            f"seconds",
        )

    async def _get_provider_instance(
        self,
        instance_type: Type[T],
        context: InjectionContext,
        provider: AbstractInstanceProvider[T],
    ) -> T:
        if context.contains_crumb(instance_type):
            raise ValueError("Cyclic dependency")

        indent = "\t" * context.crumb_depth()
        if provider.get_scope().is_instance_cached(context):
            provider_instance = provider.get_scope().get_instance(context)
            assert (
                provider_instance is not None
            ), "instance already exists because is_instance_cached() is true"
            LOGGER.log(
                5,
                f"{indent}\tAn instance of type {get_type_label(type(provider_instance))} "
                f"already exist",
            )
            return provider_instance
        context.add_crumb(provider.get_provided_implementation())
        try:
            populated_dependencies = []
            for dependency_reference in provider.get_dependencies():
                dependency_instance = await self.get_instance(
                    dependency_reference.instance_type,
                    context,
                )
                populated_dependencies.append(
                    DependencyValue(
                        dependency_reference.name,
                        dependency_instance,
                    )
                )
        except NotFoundError:
            LOGGER.log(
                5,
                f"{indent}\tCould not get a dependency to instantiate "
                f"{get_type_label(provider.get_provided_implementation())}",
            )
            raise
        finally:
            context.pop_crumb()
        provider_instance = await provider.create_instance(populated_dependencies)
        provider.get_scope().set_instance(context, provider_instance)
        LOGGER.log(
            5, f"{indent}\tReturning an instance of type {get_type_label(type(provider_instance))}"
        )
        return provider_instance

    async def _get_list_instance(
        self,
        instance_type: Type[List[T]],
        context: InjectionContext,
        existing_instance=False,
    ) -> List[T]:
        # The first condition is for python3.6, the second one is for python3.7
        if (
            typing_inspect.get_origin(instance_type) is not List
            and typing_inspect.get_origin(instance_type) is not list
        ):
            raise ValueError("The injection container only support dependencies of type List[T]")
        wrapped_instance_types = typing_inspect.get_args(instance_type)
        if len(wrapped_instance_types) != 1:
            raise ValueError("Expected a single type wrapped by the list type")
        indent = "\t" * context.crumb_depth()
        wrapped_instance_type = wrapped_instance_types[0]
        if existing_instance:
            LOGGER.log(
                5, f"{indent}Getting existing instances of {get_type_label(wrapped_instance_type)}"
            )
        else:
            LOGGER.log(
                5, f"{indent}Getting all instances of {get_type_label(wrapped_instance_type)}"
            )
        providers = self._providers.get(wrapped_instance_type)
        if providers is None:
            LOGGER.log(
                5,
                f"{indent}\tNo provider for interface" f" {get_type_label(wrapped_instance_type)}",
            )
            return []
        instances: List[T] = []
        context.add_crumb(List)
        try:
            for provider in providers:
                LOGGER.log(
                    5,
                    f"{indent}\tGetting instance of "
                    f"{get_type_label(provider.get_provided_implementation())}",
                )
                if existing_instance:
                    if not provider.get_scope().is_instance_cached(context):
                        LOGGER.log(5, f"{indent}\t\tNo existing instance")
                        continue
                    instance = provider.get_scope().get_instance(context)
                    assert (
                        instance is not None
                    ), "instance already exists because is_instance_cached() is true"
                    LOGGER.log(
                        5,
                        f"{indent}\t\tReturning an instance of "
                        f"{get_type_label(type(instance))}",
                    )
                    instances.append(instance)
                    continue
                instances.append(
                    await self._get_provider_instance(
                        wrapped_instance_type,
                        context,
                        provider,
                    )
                )
        finally:
            context.pop_crumb()
        return instances

    async def _get_union_instance(
        self,
        instance_type: Type[T],
        context: InjectionContext,
        existing_instance=False,
    ) -> T:
        indent = "\t" * context.crumb_depth()
        LOGGER.log(5, f"{indent}Getting instance in {get_type_label(instance_type)}")
        context.add_crumb(instance_type)
        try:
            for union_instance_type in typing_inspect.get_args(instance_type):
                try:
                    return await self.get_instance(union_instance_type, context, existing_instance)
                except NotFoundError:
                    continue
        finally:
            context.pop_crumb()
        raise NotFoundError(f"No provider defined for of any the types in {instance_type}")

    async def _get_class_instance(
        self,
        instance_type: Type[T],
        context: InjectionContext,
        existing_instance=False,
    ) -> T:
        providers = self._providers.get(instance_type)
        indent = "\t" * context.crumb_depth()
        LOGGER.log(5, f"{indent}Getting instance for class {get_type_label(instance_type)}")
        if providers is None:
            error_msg = f"{indent}\tNo provider for class {get_type_label(instance_type)}"
            LOGGER.log(5, error_msg)
            raise NotFoundError(error_msg)
        if existing_instance is True:
            for provider in reversed(providers):
                if provider.get_scope().is_instance_cached(context):
                    instance = provider.get_scope().get_instance(context)
                    assert (
                        instance is not None
                    ), "instance already exists because is_instance_cached() is true"
                    return instance
            error_msg = (
                f"{indent}\tNo existing instance for interface" f" {get_type_label(instance_type)}"
            )
            LOGGER.log(5, error_msg)
            raise NotFoundError(error_msg)

        for provider in reversed(providers):
            # We do not want the provider to be in the crumb, to prevent circular dependencies. This
            #  is helpful when an implementation has a dependency on another implementation of the
            #  same interface (for example, a cache repository backed by another implementation
            #  of the same repository).
            if context.contains_crumb(provider.get_provided_implementation()):
                continue
            return await self._get_provider_instance(
                instance_type,
                context,
                provider,
            )
        error_msg = f"{indent}\tCircular dependency for class {get_type_label(instance_type)}"
        LOGGER.log(5, error_msg)
        raise NotFoundError(error_msg)

    async def get_instance(
        self,
        instance_type: Type[T],
        context: InjectionContext = None,
        existing_instance=False,
    ) -> T:
        if context is None:
            context = InjectionContext()
        # Handle the List type
        if typing_inspect.is_generic_type(instance_type):
            return await self._get_list_instance(instance_type, context, existing_instance)  # type: ignore
        # Handle the Union/Optional type
        if typing_inspect.is_union_type(instance_type):
            return await self._get_union_instance(instance_type, context, existing_instance)
        # Handle the None type which can happen when the parent is an Optional type
        if instance_type == type(None):
            indent = "\t" * context.crumb_depth()
            LOGGER.log(5, f"{indent}Getting None")
            return cast(T, None)
        # Make sure we're not trying to instantiate a built in class (like int, str etc...)
        if is_built_in_type(instance_type):
            raise AssertionError(
                "Cannot define a provider for built in type, it shouldn't have gotten here"
            )
        # Handle a classic type.
        return await self._get_class_instance(instance_type, context, existing_instance)
