from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules


for finder, name, isPkg in iter_modules(__path__):
    module = import_module('models.'+name)
    for name, value in getmembers(module, isclass):
        if value.__module__ == module.__name__:
            globals()[name] = value

metadata_to_migrate = globals()['Base'].metadata
