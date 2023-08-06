from collections import deque


class InjectionContext:
    def __init__(self):
        self._dependents = deque()

    def contains_crumb(self, instance_type) -> bool:
        return instance_type in self._dependents

    def add_crumb(self, instance_type):
        self._dependents.append(instance_type)

    def pop_crumb(self):
        self._dependents.pop()

    def crumb_depth(self) -> int:
        return len(self._dependents)
