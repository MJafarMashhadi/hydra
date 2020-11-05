import os
import shutil
import argparse
import subprocess

CONDA_ENV_NAME = "hydra"

args_parser = argparse.ArgumentParser()

args_parser.add_argument('--git_url',required=True)
args_parser.add_argument('--commit_sha',required=True)
args_parser.add_argument('--oauth_token',required=True)
args_parser.add_argument('--options')
args_parser.add_argument('--model_path',required=True)
args_parser.add_argument('--platform',required=True)

args = args_parser.parse_args()

os.mkdir("project")
os.chdir("project")

# Clone and checkout the specified project repo from github
subprocess.run(["git", "clone", "https://{}:x-oauth-basic@{}".format(args.oauth_token, args.git_url), "."])
subprocess.run(["git", "checkout", args.commit_sha])

# Move data from tmp storage to project/data for local execution
if args.platform == 'local':
    if os.path.exists('/home/project/data'):
        shutil.rmtree('/home/project/data')
    shutil.copytree("/home/data", "/home/project/data")

subprocess.run(["conda", "env", "create", "-n", CONDA_ENV_NAME, "-f", "environment.yml"])
subprocess.run(["conda", "run", "-n", "hydra", "pip", "install", "hydra-ml"])

for arg in args.options.split():
    [key, val] = arg.split('=')
    os.putenv(key, val)

subprocess.run(["conda", "run", "-n", CONDA_ENV_NAME, "python3", args.model_path])
