# -*- coding: utf-8 -*-
import importlib
import pathlib

from flask_socketio_web.common.util import get_dir_files, line_to_hump, get_class_func

__ajax_map = {}
__sio_map = {}


def auth():
    def decorate(func):
        return func

    return decorate


def route(name=None, methods=None):
    def decorate(func):
        class_name, func_name = get_class_func(func).split(".")
        __ajax_map[func_name] = {
            "class_name": class_name,
            "func_name": func_name,
            "methods": methods,
            "rule": name
        }
        return func

    if methods is None:
        methods = ["GET", "POST"]

    if callable(name):
        return decorate(name)
    else:
        return decorate


def is_match(s, p):
    """
    s 原字符
    p 匹配表达式：点'？' 匹配任何单个字符 星号“ *”匹配零个或多个字符。
    """
    sl = len(s)
    pl = len(p)
    dp = [[False for i in range(pl + 1)] for j in range(sl + 1)]
    s = " " + s
    p = " " + p
    dp[0][0] = True
    for i in range(1, pl + 1):
        if p[i] == '*':
            dp[0][i] = dp[0][i - 1]
    for i in range(1, sl + 1):
        for j in range(1, pl + 1):
            if s[i] == p[j] or p[j] == '?':
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j] == '*':
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[sl][pl]


def get_actions(scan):
    klass_list = []
    if isinstance(scan, list):
        for sc in scan:
            py_files = get_dir_files(sc, filter_re=f".*.py$", absolute=True)
            for py in py_files:
                klass_list.append(import_new_module(py))
    else:
        py_files = get_dir_files(scan, filter_re=f".*.py$", absolute=True)
        for py in py_files:
            klass_list.append(import_new_module(py))
    return klass_list


def import_new_module(name):
    py_lib = pathlib.Path(name)
    m = importlib.import_module(f'{".".join(py_lib.parts[:-1])}.{py_lib.name[:-3]}')
    importlib.reload(m)
    c_name = line_to_hump(py_lib.name[:-3])
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
            sio_map[fname] = __sio_map[a]

    setattr(klass, "ajax_map", ajax_map)
    setattr(klass, "sio_map", sio_map)
    return klass() # 实例化


def define(name=None):
    """定义类的路径名"""

    def decorate(clazz):
        setattr(clazz, "__basename__", name)
        return clazz

    return decorate


def event(name=None, namespace=None):
    def decorate(func, _name=name):
        class_name, func_name = get_class_func(func).split(".")
        __sio_map[func_name] = {
            "class_name": class_name,
            "func_name": func_name,
            "namespace": namespace,
            "event": _name or func_name
        }
        return func

    if callable(name):
        return decorate(name, name.__name__)
    else:
        return decorate
