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
    hydra.cloud.registered_platforms.append(clazz)
    return clazz


@mark_disabled
class AbstractPlatform():
    def __init__(self, model_path, options):
        self.model_path = model_path
        self.options = options

    def train(self):
        raise Exception("Not Implemented: Please implement this function in the subclass.")

    def serve(self):
        raise Exception("Not Implemented: Please implement this function in the subclass.")

    def run_command(self, command):
        subprocess.run(command)
