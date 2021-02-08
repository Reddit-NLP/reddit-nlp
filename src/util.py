import threading, time


def run_thread(func):
    threading.Thread(target=func).start()
