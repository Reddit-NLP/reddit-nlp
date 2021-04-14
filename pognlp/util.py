"""Misc. utility functions"""

import threading
from typing import Callable, Generic, Set, TypeVar

T = TypeVar("T")
Callback = Callable[[T], None]


class Observable(Generic[T]):
    """Basic implementation of an observable. Used for passing state down a
    (possibly) long chain of views and controllers. Initialize with some
    initial value and use observable.subscribe(func) to call func whenever the
    value changes.

    Adapted from https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017
    """

    def __init__(self, initial_value: T):
        self.value = initial_value
        self.callbacks: Set[Callback[T]] = set()

    def subscribe(self, func: Callback[T], call: bool = True) -> None:
        """Add a callback that gets called whenever the value changes. Optionally
        call the function immediately"""
        self.callbacks.add(func)
        if call:
            func(self.value)

    def unsubscribe(self, func: Callback[T]) -> None:
        """Remove a callback"""
        self.callbacks.remove(func)

    def update(self) -> None:
        """Call all callbacks with the current value"""
        for func in self.callbacks:
            func(self.value)

    def set(self, value: T) -> None:
        """Set a new value"""
        self.value = value
        self.update()

    def get(self) -> T:
        """Get the current value"""
        return self.value


def run_thread(func: Callable[[], None]) -> None:
    """Run a function in another thread"""
    threading.Thread(target=func).start()
