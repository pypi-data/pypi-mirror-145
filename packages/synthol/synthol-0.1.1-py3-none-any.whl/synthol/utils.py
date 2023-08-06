import inspect
import types
from typing import Type, List, Callable, Any

import typing_inspect


def is_built_in_type(type: Type) -> bool:
    """
    Determine if the provided type is defined in a built-in module. Examples include str, int etc...
    """
    if type is types.BuiltinFunctionType:
        return False
    try:
        inspect.getfile(type)
        return False
    except TypeError:
        return True


def get_provided_interfaces(type: Type) -> List[Type]:
    """
    Get all the interfaces implemented by the provided class type (including the class type itself).
    """
    if not inspect.isclass(type):
        raise TypeError("The provided type must be a class type")
    interfaces = []
    all_interfaces = type.__mro__
    for provided_interface in all_interfaces:
        try:
            inspect.getfile(provided_interface)
            interfaces.append(provided_interface)
        except TypeError:
            pass
    return interfaces


def get_type_label(type: Type) -> str:
    """
    Get a clean label for a class/built in type
    """
    if inspect.isclass(type):
        return type.__qualname__
    if typing_inspect.is_union_type(type):
        subclass_labels = [get_type_label(subclass) for subclass in typing_inspect.get_args(type)]
        return f"Union[{', '.join(subclass_labels)}]"

    else:
        return str(type)


def get_callable_label(callable: Callable[..., Any]) -> str:
    """
    Get a clean label for a callable object.
    """
    return callable.__qualname__
