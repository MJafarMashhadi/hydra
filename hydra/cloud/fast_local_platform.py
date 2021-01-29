import os
from hydra.cloud.abstract_platform import AbstractPlatform

class FastLocalPlatform(AbstractPlatform):
    short_name = 'fast_local'

    def __init__(self, model_path, options, **ignored_args):
        super().__init__(model_path, options)

    def train(self):
        os.system(" ".join([self.options, 'python3', self.model_path]))
        return 0

    def serve(self):
        pass
