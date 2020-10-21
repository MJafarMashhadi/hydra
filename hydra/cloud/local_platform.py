import os
import subprocess
from hydra.cloud.abstract_platform import AbstractPlatform

class LocalPlatform(AbstractPlatform):
    def __init__(self, model_path, prefix_params, git_url, commit_sha, github_token, google_credential_path):
        self.git_url = git_url
        self.commit_sha = commit_sha
        self.github_token = github_token
        self.google_credential_path = google_credential_path
        super().__init__(model_path, prefix_params)

    def train(self):
        execution_script_path = os.path.join(os.path.dirname(__file__), '../../docker/local_execution.sh')
        command = ['sh', execution_script_path, '-g', self.git_url, '-c', self.commit_sha,
            '-o', self.github_token, '-m', self.model_path, '-p', self.prefix_params '-a', self.google_credential_path]

        self.run_command(command)
        return 0

    def serve(self):
        pass
