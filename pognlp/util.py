import threading, time


class Observable:
    """Basic implementation of an observable. Used for passing state down a
    (possibly) long chain of views and controllers. Initialize with some
    initial value and use observable.subscribe(func) to call func whenever the
    value changes.

    Adapted from https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017
    """

    def __init__(self, initial_value=None):
        self.data = initial_value
        self.callbacks = set()

    def subscribe(self, func, call=True):
        self.callbacks.add(func)
        if call:
            func(self.data)

    def unsubscribe(self, func):
        self.callbacks.remove(func)

    def update(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self.update()

    def get(self):
        return self.data


def run_thread(func):
    threading.Thread(target=func).start()
