"""Misc. utility functions"""

import threading
from typing import Any, Callable, cast, Generic, Optional, Set, TypeVar

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
        if func in self.callbacks:
            self.callbacks.remove(func)

    def update(self) -> None:
        """Call all callbacks with the current value"""

        # An attempt to make this (sorta) thread-safe. Python throws a
        # RuntimeError if a set changes size while iterating over it, so we
        # copy to a list first and then double-check membership each iteration
        for func in list(self.callbacks):
            if func in self.callbacks:
                func(self.value)

    def set(self, value: T) -> None:
        """Set a new value"""
        self.value = value
        self.update()

    def get(self) -> T:
        """Get the current value"""
        return self.value


class Observer(Generic[T]):
    """A callback that can change observables"""

    def __init__(
        self,
        callback: Callback[T],
        initial_observable: Optional[Observable[T]] = None,
        call: bool = True,
    ):
        self.observable: Optional[Observable[T]] = initial_observable
        if self.observable:
            self.observable.subscribe(callback, call=call)
        self.callback = callback

    def get(self) -> Optional[T]:
        """Gets the value of the current observable if it exists, else None"""
        if not self.observable:
            return None
        return self.observable.get()

    def stop(self) -> None:
        """Stop observing the current observable"""
        if self.observable:
            self.observable.unsubscribe(self.callback)

    def set_observable(self, new_observable: Observable[T], call: bool = True) -> None:
        """Change the observable we're observing"""
        if self.observable == new_observable:
            return
        if self.observable:
            self.observable.unsubscribe(self.callback)
        new_observable.subscribe(self.callback, call=call)
        self.observable = new_observable


F = TypeVar("F", bound=Callable[..., Any])


def in_main_thread(func: F) -> F:
    """Decorate an instance method of a view such that it is always executed
    on the main thread using tkthread."""

    def wrapper(self, *args, **kwargs):  # type: ignore
        closure = lambda: func(self, *args, **kwargs)
        self.controller.tkt(closure)

    return cast(F, wrapper)


def run_thread(func: Callable[[], None]) -> None:
    """Run a function in another thread"""
    threading.Thread(target=func).start()
