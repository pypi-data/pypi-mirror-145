# -*- coding: utf-8 -*-
import importlib
import pathlib
from functools import wraps

from src.common.util import get_dir_files, line_to_hump, get_class_func

__ajax_map = {}
__sio_map = {}


def auth():
    def decorate(func):
        return func

    return decorate


def ajax(route=None, methods=None):
    if methods is None:
        methods = ["GET", "POST"]

    def decorate(func):
        class_name, func_name = get_class_func(func).split(".")
        __ajax_map[func_name] = {
            "class_name": class_name,
            "func_name": func_name,
            "methods": methods,
            "rule": route
        }
        return func
    return decorate


def get_actions(module="action", suffix="action"):
    py_files = get_dir_files(module, filter_re=f".*_{suffix}.py$", absolute=True)
    klass_list = []
    for py_file in py_files:
        py_name = pathlib.Path(py_file).name[:-3]
        base_name = py_name[:-len(suffix) - 1]
        m = importlib.import_module(f'{module}.{py_name}')
        importlib.reload(m)
        c_name = line_to_hump(py_name)
        klass = getattr(m, c_name)

        # --------ajax----------
        ajax_map = {}
        for a in __ajax_map.keys():
            cname, fname = __ajax_map[a]["class_name"], __ajax_map[a]["func_name"]
            if cname == c_name:
                ajax_map[fname] = __ajax_map[a]

        # --------websocket----------
        sio_map = {}
        for a in __sio_map.keys():
            cname, fname = __sio_map[a]["class_name"], __sio_map[a]["func_name"]
            if cname == c_name:
                if __sio_map[a]["namespace"] is None:
                    __sio_map[a]["namespace"] = cname
                sio_map[fname] = __sio_map[a]

        setattr(klass, "ajax_map", ajax_map)
        setattr(klass, "sio_map", sio_map)
        setattr(klass, "base_name", base_name)
        klass_list.append(klass)
    return klass_list


def sio(event=None, namespace=None):

    def decorate(func):
        class_name, func_name = get_class_func(func).split(".")
        __sio_map[func_name] = {
            "class_name": class_name,
            "func_name": func_name,
            "namespace": namespace,
            "event": event if event else func_name
        }
        return func
    return decorate
