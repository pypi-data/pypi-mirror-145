import inspect
from abc import ABC, abstractmethod
from typing import (
    cast,
    Awaitable,
    Generic,
    List,
    Type,
    Any,
    Callable,
    Dict,
    TypeVar,
    Optional,
    Union,
)

import typing_inspect
from dataclasses import dataclass
from synthol.scope import AbstractInjectionScope, SingletonScope
from synthol.utils import (
    get_provided_interfaces,
    is_built_in_type,
    get_callable_label,
)

T = TypeVar("T")
Factory = Callable[..., Union[T, Awaitable[T]]]


@dataclass
class DependencyReference(Generic[T]):
    """
    A reference to a dependency required by a factory/constructor
    """

    name: str
    instance_type: Type[T]


@dataclass
class DependencyValue(Generic[T]):
    """
    The value for a dependency required by a factory/constructor
    """

    name: str
    instance: T


class AbstractInstanceProvider(ABC, Generic[T]):
    """
    The provider is responsible for instantiating an implementation of the specified interfaces and
    defining the dependencies it requires to instantiate it. It defines a scope that determines
    when a new instance is required or when an existing one can be reused.
    """

    def __init__(self, provided_interfaces: List[Type[T]]):
        for provided_interface in provided_interfaces:
            if is_built_in_type(provided_interface):
                raise TypeError(f"The provider cannot provide built-in types")
        self._provided_interfaces = provided_interfaces

    def get_provided_interfaces(self) -> List[Type[T]]:
        """
        Get a list of interfaces implemented by the instances provided by the provider.
        :return:
        """
        return self._provided_interfaces

    def get_provided_implementation(self) -> Type[T]:
        """
        Get a list of interfaces implemented by the instances provided by the provider.
        :return:
        """
        return self._provided_interfaces[0]

    @abstractmethod
    def get_scope(self) -> AbstractInjectionScope[T]:
        """
        Get the scope associated with the provider. The scope takes care of caching instances
        provided by the provider for a given injection context.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_dependencies(self) -> List[DependencyReference]:
        """
        Get a list of interfaces required by the provider to provide a new instance.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    async def create_instance(self, dependencies: List[DependencyValue]) -> T:
        """
        Create a new instance that implements all the interfaces returned by the
        `get_provided_interfaces` method.
        :param dependencies:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError()


class StaticProvider(AbstractInstanceProvider[T]):
    """
    An instance provider implementation that can only provide the instance passed to the
    constructor. As implied by its definition, this implementation can only use the singleton scope.
    """

    def __init__(self, provided_interfaces: List[Type[T]], instance: T):
        super().__init__(provided_interfaces)
        self._scope = SingletonScope(instance)

    def get_dependencies(self) -> List[DependencyReference]:
        raise NotImplementedError()

    def get_scope(self):
        return self._scope

    async def create_instance(self, dependencies: List[DependencyValue]) -> T:
        raise NotImplementedError()

    def __eq__(self, other):
        if not isinstance(other, StaticProvider):
            return False
        return type(other._scope._instance) is type(self._scope._instance)


class AbstractFactoryProvider(AbstractInstanceProvider[T], ABC):
    """
    An abstract instance provider implementation that relies on a factory function/constructor to
    provide a class instance.
    """

    def __init__(
        self,
        factory: Factory[T],
        factory_kwargs: Dict[str, Any],
        provided_interfaces: List[Type[T]],
    ):
        self._factory = factory
        self._factory_kwargs = factory_kwargs
        super().__init__(provided_interfaces)

    async def create_instance(self, dependencies: List[DependencyValue]) -> T:
        args = {d.name: d.instance for d in dependencies}
        args.update(self._factory_kwargs)
        result = self._factory(**args)
        if inspect.isawaitable(result):
            result = await cast(Awaitable[T], result)
        else:
            result = cast(T, result)
        if result is None:
            raise ValueError(
                f"The dependency factory {get_callable_label(self._factory)} did not return a "
                f"value."
            )
        return result


class FactoryProvider(AbstractFactoryProvider[T]):
    """
    An instance provider implementation that relies on a factory function/constructor to
    provide a class instance. The scope, dependencies and provided interfaces are defined when
    the provider is instantiated.
    """

    def __init__(
        self,
        factory: Factory[T],
        factory_kwargs: Dict[str, Any],
        provided_interfaces: List[Type[T]],
        dependencies: List[DependencyReference],
        scope: AbstractInjectionScope,
    ):
        super().__init__(factory, factory_kwargs, provided_interfaces)
        self._scope = scope
        self._dependencies = dependencies

    def get_scope(self) -> AbstractInjectionScope[T]:
        return self._scope

    def get_dependencies(self) -> List[DependencyReference]:
        return self._dependencies

    def get_provided_interfaces(self) -> List[Type[T]]:
        return self._provided_interfaces

    def __eq__(self, other):
        if not isinstance(other, FactoryProvider):
            return False
        return other._factory == self._factory


class AutoFactoryProvider(AbstractFactoryProvider[T]):
    """
    An instance provider implementation that relies on a factory function/constructor to
    provide a class instance. The dependencies and provided interfaces are optional. If not
    provided, they are created from the signature of the factory function/constructor. The scope is
    also optional and defaults to a singleton scope. The dependencies and scope are created (and
    memoized) only when the corresponding methods are called, making this provider very lightweight
    to instantiate.
    """

    def __init__(
        self,
        factory: Factory[T],
        factory_kwargs: Optional[Dict[str, Any]] = None,
        provided_interfaces: Union[Type[T], List[Type[T]], None] = None,
        dependencies: List[DependencyReference] = None,
        scope: AbstractInjectionScope = None,
    ):
        if not callable(factory):
            raise ValueError(f"The factory provided for is not callable.")

        if not isinstance(provided_interfaces, list):
            if provided_interfaces is not None:
                provided_type = provided_interfaces
            elif inspect.isclass(factory):
                provided_type = cast(Type[T], factory)
            elif not hasattr(factory, "__annotations__"):
                raise ValueError(
                    f"The provided factory {get_callable_label(factory)} does not provide any "
                    f"information about its annotations."
                )
            else:
                return_type = factory.__annotations__.get("return")
                if return_type is None:
                    raise ValueError(
                        f"The provided interfaces are not explicitly defined by the provider and "
                        f"the provided factory {get_callable_label(factory)} does not provide an "
                        f"annotation for its return type"
                    )
                provided_type = return_type
            if is_built_in_type(provided_type):
                raise TypeError(
                    f"The provider factory {get_callable_label(factory)} returns a built-in type"
                )
            provided_interfaces = get_provided_interfaces(provided_type)

        factory_kwargs = factory_kwargs if factory_kwargs is not None else {}
        super().__init__(factory, factory_kwargs, provided_interfaces)
        self._dependencies = dependencies
        self._scope = scope

    def get_scope(self) -> AbstractInjectionScope[T]:
        if self._scope is not None:
            return self._scope
        self._scope = SingletonScope()
        return self._scope

    def get_dependencies(self) -> List[DependencyReference]:
        if self._dependencies is not None:
            return self._dependencies
        if inspect.isclass(self._factory):
            arg_specs = inspect.getfullargspec(self._factory.__init__)
        else:
            arg_specs = inspect.getfullargspec(self._factory)
        self._dependencies = []
        for i, arg_name in enumerate(arg_specs.args):
            # Skip the 'self' or 'cls' argument.
            if i == 0 and (inspect.ismethod(self._factory) or inspect.isclass(self._factory)):
                continue
            # Skip argument that will be overridden by the provided kwargs
            if arg_name in self._factory_kwargs:
                continue
            arg_annotation = arg_specs.annotations.get(arg_name)
            # Make sure a type annotation exists for the argument, otherwise it can't be injected
            if arg_annotation is None:
                raise ValueError(
                    f"The argument {arg_name} of {get_callable_label(self._factory)} must be "
                    f"annotated to be populated by the injector."
                )
            elif type(arg_annotation) is str:
                # More info:
                # https://github.com/python/peps/commit/454c88950bca978ddff30144c66f2e420f51f96e
                raise ValueError(
                    "Annotation type is 'str'. This indicates that the type hint is "
                    "stringified, most likely because of a "
                    "`from __future__ import annotations` directive. In future we "
                    "may want to evaluate such annotations at runtime."
                )
            # Check that the argument is not a built-in type (although it can be from the typing
            # module). Trying to inject them is a can of worms that requires uniquely identifying
            # instances.
            if (
                is_built_in_type(arg_annotation)
                and not typing_inspect.is_generic_type(arg_annotation)
                and not typing_inspect.is_union_type(arg_annotation)
            ):
                has_default_value = arg_specs.defaults is not None and i >= len(
                    arg_specs.args
                ) - len(arg_specs.defaults)
                if has_default_value:
                    # It's ok to have a built-in type if there is a default value for it. It is just
                    #  ignored as a dependency.
                    continue
                raise ValueError(
                    f"The required argument {arg_name} of {get_callable_label(self._factory)} is a "
                    f"built-in type in without a default value"
                )

            self._dependencies.append(DependencyReference(arg_name, arg_annotation))
        return self._dependencies

    def __eq__(self, other):
        if not isinstance(other, AbstractFactoryProvider):
            return False
        return other._factory == self._factory
