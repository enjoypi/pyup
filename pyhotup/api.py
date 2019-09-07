def reload(module_name, class_name):
    def get_class(mod, classname):
        import inspect
        for _name, _class in inspect.getmembers(mod):
            if _name == classname and inspect.isclass(_class):
                return _class

    import sys
    mod = sys.modules[module_name]
    if not mod:
        return

    cls = get_class(mod, class_name)

    import importlib
    new_mod = importlib.reload(sys.modules[module_name])
    if not mod:
        return

    new_class = get_class(new_mod, class_name)

    if new_class:
        import gc
        for obj in gc.get_objects():
            if isinstance(obj, cls):
                obj.__class__ = new_class


def reload_module(module_name):
    import sys
    module = sys.modules[module_name]

    old_classes = get_classes(module)

    import importlib
    new_module = importlib.reload(module)
    print('module', module_name, 'reloaded')
    new_classes = get_classes(new_module)

    import gc
    for obj in gc.get_objects():
        _class = obj.__class__
        if _class and (_class.__name__ in old_classes):
            obj.__class__ = new_classes[_class.__name__]
            print('<{0}.{1} object at {2}> update'.format(
                _class.__module__, _class.__name__, hex(id(obj))))


def get_classes(module):
    classes = dict()
    import inspect
    for class_name, _class in inspect.getmembers(module):
        if inspect.isclass(_class):
            classes[class_name] = _class
    return classes
