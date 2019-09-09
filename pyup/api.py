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

    import importlib
    new_module = importlib.reload(module)
    print('module', module_name, 'reloaded')
    new_classes = get_classes(new_module)

    import gc
    for obj in gc.get_objects():
        old_class = obj.__class__
        class_name = old_class.__name__
        if old_class and (class_name in new_classes):
            new_class = new_classes[class_name]
            if old_class == new_class:
                continue
            obj.__class__ = new_class
            print('object<{0}>.__class__({1}.{2}<{3}>) is updated to <{4}>'.
                  format( hex(id(obj)), module_name, class_name, hex(id(old_class)), hex(id(new_class))))


def get_classes(module):
    classes = dict()
    import inspect
    for class_name, _class in inspect.getmembers(module):
        if inspect.isclass(_class):
            classes[class_name] = _class
    return classes
