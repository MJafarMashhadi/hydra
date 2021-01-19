import pkgutil
import importlib
import os
import logging
import sys
from hydra.utils import reflection
from .abstract_platform import AbstractPlatform

logger = logging.getLogger("plugin_loader")

def discover_plugins():
    _packages = map(
        lambda info: info.name, 
        filter(
            lambda info: not info.ispkg, 
            pkgutil.walk_packages(
                [os.path.dirname(__file__)], 
                prefix='hydra.cloud.'
            )
        )
    )

    modules = []
    for p in _packages:
        try:
            mod = importlib.import_module(p)
        except ImportError as e:
            logger.warning(f"Could not load {p}, possible cause: dependencies are not installed. Exception: {e}")
        else:
            modules.append(mod)

    _registered_platforms = []
    for plugin in reflection.get_all_subclasses(AbstractPlatform):
        if getattr(plugin, '__hydra_plugin_disabled__', lambda *_: False)():
            continue
        _registered_platforms.append(plugin)

    return _registered_platforms


if sys.version_info >= (3, 7):
    _uninitialized = object()
    _registered_platforms = _uninitialized

    def __getattr__(name: str):
        global _registered_platforms
        if name == 'registered_platforms':
            if _registered_platforms is _uninitialized:
                _registered_platforms = discover_plugins()
            return _registered_platforms

        raise AttributeError(f"module {__name__} has no attribute {name}")
else:
    from hydra.utils import lazy

    class _LazyProxy(object):
        def __init__(self, name):
            self.module = sys.modules[name]
            sys.modules[name] = self
            self.initializing = True
        
        @lazy.LazyLoaded
        def registered_platforms(self):
            return discover_plugins()

        def __getattr__(self, name):
            # call module.__init__ after import introspection is done
            if self.initializing and not name[:2] == '__' == name[-2:]:
                self.initializing = False
                __init__(self.module)  # noqa
            return getattr(self.module, name)

    _LazyProxy(__name__)
