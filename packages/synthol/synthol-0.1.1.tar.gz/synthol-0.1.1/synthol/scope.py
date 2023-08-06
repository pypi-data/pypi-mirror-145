from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from synthol.context import InjectionContext

T = TypeVar("T")


class AbstractInjectionScope(ABC, Generic[T]):
    """
    The injection scope defines when an existing instance of an object is reused when it is
    requested by the container.
    """

    @abstractmethod
    def is_instance_cached(self, context: InjectionContext) -> bool:
        """
        Determines if an instance already exists for the provided context.
        :param context:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_instance(self, context: InjectionContext) -> Optional[T]:
        """
        Get an instance for the provided context. If there is no existing instance for the provided
        context, it returns None.
        :param context:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def set_instance(self, context: InjectionContext, instance: T):
        """
        Set an instance for the provided context. It can only be invoked if calling the
        is_instance_cached method would return False.
        :param context:
        :param instance:
        :return:
        """
        raise NotImplementedError()


class SingletonScope(AbstractInjectionScope[T]):
    """
    The singleton scope ensures that a single instance of an object exists throughout the
    application.
    """

    def __init__(self, instance: T = None):
        self._instance = instance
        self._is_set = self._instance is not None

    def is_instance_cached(self, context: InjectionContext):
        return self._is_set is True

    def get_instance(self, context: InjectionContext) -> Optional[T]:
        return self._instance

    def set_instance(self, context: InjectionContext, instance: T):
        self._instance = instance
        self._is_set = True


class PrototypeScope(AbstractInjectionScope[T]):
    """
    The prototype scope ensures that new instance of an object is created when it is requested by
    the container.
    """

    def is_instance_cached(self, context: InjectionContext):
        return False

    def get_instance(self, context: InjectionContext) -> Optional[T]:
        raise NotImplementedError()

    def set_instance(self, context: InjectionContext, instance: T):
        pass
