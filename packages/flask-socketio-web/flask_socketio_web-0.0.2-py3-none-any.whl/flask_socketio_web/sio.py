# -*- coding: utf-8 -*-
from functools import wraps

__sio_map = {}


def sio(namespace=None, event=None):
    def wrapper(func):
        @wraps(func)
        def decorate(self, *args, **kwargs):
            _event = event if event else func.__name__
            __sio_map[event] = {
                "event": _event,
                "namespace": namespace,
                "func": func
            }
            return decorate

    return wrapper
