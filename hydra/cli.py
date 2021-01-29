import os
import yaml
import json
import click
import hydra.utils.constants as const
from hydra.utils.git import check_repo
from hydra.utils.utils import dict_to_string, inflate_options
import hydra.cloud

from hydra.version import __version__

@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
# Generic options
@click.option('-y', '--yaml_path', default='hydra.yaml', type=str)
@click.option('-p', '--project_name', default=None, type=str)
@click.option('-m', '--model_path', default=None, type=str)
@click.option('--cloud', default=None, type=click.Choice(hydra.cloud.registered_platforms.keys(), case_sensitive=False))
@click.option('--github_token', envvar='GITHUB_TOKEN') # Takes either an option or environment var

# Cloud specific options
@click.option('--cpu_count', default=None, type=click.IntRange(0, 96), help='Number of CPU cores required')
@click.option('--memory_size', default=None, type=click.IntRange(0, 624), help='GB of RAM required')

@click.option('--gpu_count', default=None, type=click.IntRange(0, 8), help="Number of accelerator GPUs")
@click.option('--gpu_type', default=None, type=str, help="Accelerator GPU type")

@click.option('--region', default=None, type=str, help="Region of cloud server location")

# Docker Options
@click.option('-t', '--image_tag', default=None, type=str, help="Docker image tag name")
@click.option('-u', '--image_url', default=None, type=str, help="Url to the docker image on cloud")

# Env variable of model file
@click.option('-o', '--options', default=None, type=str, help='Environmental variables for the script')

def train(
    yaml_path,
    project_name,
    model_path,
    cloud,
    github_token,
    cpu_count,
    memory_size,
    gpu_count,
    gpu_type,
    region,
    image_tag,
    image_url,
    options):

    # If YAML config file available to supplement the command line arguments
    if os.path.isfile(yaml_path):
        with open(yaml_path) as f:
            print("[Hydra Info]: Loading run info from {}...".format(yaml_path))

            data = yaml.load(f, Loader=yaml.FullLoader)
            train_data = data.get('train', '')
            project_name = train_data.get('project_name')

            if project_name is None:
                raise Exception("project_name option is required")

            model_path = train_data.get('model_path', const.MODEL_PATH_DEFAULT) if model_path is None else model_path
            cloud = train_data.get('cloud', const.CLOUD_DEFAULT).lower() if cloud is None else cloud

            # Cloud specific 
            region = train_data.get('region', const.REGION_DEFAULT) if region is None else region

            cpu_count = train_data.get('cpu_count', const.CPU_COUNT_DEFAULT) if cpu_count is None else cpu_count
            memory_size = train_data.get('memory_size', const.MEMORY_SIZE_DEFAULT) if memory_size is None else memory_size
            gpu_count = train_data.get('gpu_count', const.GPU_COUNT_DEFAULT) if gpu_count is None else gpu_count
            gpu_type = train_data.get('gpu_type', const.GPU_TYPE_DEFAULT) if gpu_type is None else gpu_type

            image_tag = train_data.get('image_tag', const.IMAGE_TAG_DEFAULT) if image_tag is None else image_tag
            image_url = train_data.get('image_url', const.IMAGE_URL_DEFAULT) if image_url is None else image_url

            options_list = train_data.get('options', const.OPTIONS_DEFAULT) if options is None else options
    # Read the options for run from CLI
    else:
        model_path = const.MODEL_PATH_DEFAULT if model_path is None else model_path
        cloud = const.CLOUD_DEFAULT if cloud is None else cloud

        region = const.REGION_DEFAULT if region is None else region

        cpu_count = const.CPU_COUNT_DEFAULT if cpu_count is None else cpu_count
        memory_size = const.MEMORY_SIZE_DEFAULT if memory_size is None else memory_size
        gpu_count = const.GPU_COUNT_DEFAULT if gpu_count is None else gpu_count
        gpu_type = const.GPU_TYPE_DEFAULT if gpu_type is None else gpu_type

        image_tag = const.IMAGE_TAG_DEFAULT if image_tag is None else image_tag
        image_url = const.IMAGE_URL_DEFAULT if image_url is None else image_url

        options = str(const.OPTIONS_DEFAULT) if options is None else options
        options_list = json.loads(options)

    if isinstance(options_list, dict):
        options_list = [options_list]

    options_list_inflated = inflate_options(options_list)

    print("\n[Hydra Info]: Executing experiments with the following options: \n {}\n".format(options_list_inflated))

    for i, options in enumerate(options_list_inflated):
        options_str = dict_to_string(options)

        print("\n[Hydra Info]: Runnning experiment #{} with the following options: \n {}\n".format(i, options))

        git_url, commit_sha = check_repo(github_token)
        args = dict(
            model_path=model_path,
            options=options_str,
            git_url=git_url,
            commit_sha=commit_sha,
            github_token=github_token,
            cpu=cpu_count,
            memory=memory_size,
            gpu_count=gpu_count,
            gpu_type=gpu_type,
            region=region,
            image_url=image_url,
            image_tag=image_tag,
            project_name=project_name,
        )
        
        platform = hydra.cloud.registered_platforms[cloud](**args)
        platform.train()

    return 0
