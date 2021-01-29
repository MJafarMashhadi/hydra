import subprocess


def _check_class(clazz):
    if clazz.__name__ == 'AbstractPlatform':
        return

    if not issubclass(clazz, AbstractPlatform):
        raise ValueError("Your class should inherit from hydra.cloud.abstract_platform.AbstractPlatform.")


def mark_disabled(clazz):
    _check_class(clazz)
    setattr(clazz, '__hydra_plugin_disabled__', classmethod(lambda cls: cls is clazz))
    return clazz


def register_plugin(clazz):
    import hydra.cloud 
    _check_class(clazz)
    name = clazz.get_short_name()
    if name in hydra.cloud.registered_platforms:
        raise ValueError(f"Conflicting platform name {name}: {clazz}, {hydra.cloud.registered_platforms[name]}")

    hydra.cloud.registered_platforms[clazz.get_short_name()] = clazz
    return clazz


@mark_disabled
class AbstractPlatform():
    short_name = 'Abstract Platform'

    def __init__(self, model_path, options, **kwargs):
        self.model_path = model_path
        self.options = options

    def train(self):
        raise Exception("Not Implemented: Please implement this function in the subclass.")

    def serve(self):
        raise Exception("Not Implemented: Please implement this function in the subclass.")

    @classmethod
    def get_short_name(cls):
        """
        Short name of the platform, used in cli. 
        Subclasses can either override short_name class variable
        or this class method.
        """
        return cls.short_name

    def run_command(self, command):
        subprocess.run(command)
