import os
import sys
import string
import random
from hashlib import md5

from . import (
    _compat,
    _format,
    _json,
    colog,
    decorators,
    form_data,
    reverify,
    const,
)

__version__ = '0.1.7'


def md5sum(content):
    m = md5()
    if not isinstance(content, bytes):
        content = content.encode('utf-8').strip()
    m.update(content)
    s = m.hexdigest().lower()
    return s


def short_uuid(length):
    charset = string.ascii_letters + string.digits
    return ''.join([random.choice(charset) for i in range(length)])


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def dirpath(path, depth=1):
    """
    usage: index to source and add to sys.path
    >>> folder = dirpath(__file__, 1)
    >>> sys.path.insert(0, folder)
    """
    path = os.path.abspath(path)
    for i in range(depth):
        path = os.path.dirname(path)
    return path


def _generate_parent_dir(fp_path, limit=1, subdir=".git"):
    fn = os.path.abspath(fp_path)
    if os.path.isdir(fn):
        p = fn
    else:
        p = os.path.dirname(fn)
    while limit:
        p2 = os.path.join(p, subdir)
        if os.path.isdir(p2):
            limit -= 1
            yield p
        p3 = os.path.dirname(p)
        if p3 == p:
            limit = 0
        else:
            p = p3


def get_parent_dir(fp_path, subdir=".git"):
    _gen = _generate_parent_dir(fp_path, limit=1, subdir=subdir)
    ps = list(_gen)
    if len(ps) > 0:
        return ps[0]


def import_file(py_file, module_name=None, nullable=False):
    # eg1: x = reload_py_file("your/path/x.py")
    # eg2: x3 = reload_py_file("your/path/x.py", "x2")
    import importlib
    import importlib.util

    if not module_name:
        module_name = os.path.basename(py_file).rstrip(".py").replace(".", "_")

    print("[todo] import_py_file: ", py_file, module_name)
    if not os.path.isfile(py_file):
        print("NOT FOUND:", py_file)
        if nullable:
            return None
        raise FileNotFoundError(py_file)

    imp_prev = sys.modules.get(module_name, None)
    if imp_prev is not None:
        fn_prev = "backup: {}._prev".format(module_name)
        print("backup module:", fn_prev, imp_prev)
        sys.modules[fn_prev] = imp_prev

    imp_spec = importlib.util.spec_from_file_location(module_name, py_file)
    if imp_spec is not None:
        py_imp = imp_spec.loader.load_module()
        print("reset sys.module:", module_name, py_imp)
        sys.modules[module_name] = py_imp
        return py_imp
    elif not nullable:
        print("ImportError", module_name, py_file)
        raise ImportError("{} => {}".format(module_name, py_file))
    else:
        print("ImportFailed", module_name, py_file)
        return None


def reload_module(py_module_dir, module_name=None, auto_init=True, nullable=False):
    # eg1: x = reload_py_file("your/path/x")
    # eg2: x3 = reload_py_file("your/path/x", "x2")
    import importlib
    import importlib.util
    from datetime import datetime as DT

    if not os.path.exists(py_module_dir):
        if nullable:
            return None
        raise FileNotFoundError(py_module_dir)
    elif os.path.isdir(py_module_dir):
        py_module_init = os.path.join(py_module_dir, "__init__.py")
        py_module_init = os.path.abspath(py_module_init)
        if not os.path.exists(py_module_init):
            if auto_init:
                print("auto create: ", py_module_init)
                now_str = DT.now()
                with open(py_module_init, "w") as fw:
                    fw.write("# coding:utf-8")
                    fw.write("## auto created @ {}".format(now_str))
                    fw.write("## created by pyco-utils.reload_module({})".format(py_module_dir))
            else:
                print("Python Module missing __init__.py", py_module_dir)
                raise FileNotFoundError(py_module_init)
    else:
        # if os.path.isfile(py_module_dir)
        if not py_module_dir.endswith(".py"):
            print("warning: {} is not a python file".format(py_module_dir))
        py_module_init = py_module_dir

    py_module_dir = os.path.abspath(os.path.dirname(py_module_init))
    sys.path.insert(0, py_module_dir)
    try:
        imp_module = import_file(py_module_init, module_name=module_name, nullable=nullable)
        return imp_module
    except Exception as e:
        if not nullable:
            print("ImportError", module_name, py_module_init)
            raise e
        else:
            print("ImportFailed", module_name, py_module_init)
            return None
