import json
import os
import re
import shutil
import subprocess
import sys
import time


DEPLOYMENT_SPEC_FILE = 'production/deployment.yaml'
SERVICE_SPEC_FILE = 'production/service.yaml'
BLUE = 'blue'
GREEN = 'green'
DEPLOYMENT_COLOR_REGEX = re.compile(r'([$]{DEPLOY_VERSION})')
TEMP_FOLDER = 'temp_prod'


def copy_file_to_temp(file_path):
    file_name = file_path.split('/')[-1]
    temp_file_path = os.path.join(TEMP_FOLDER, file_name)
    if not os.path.isdir(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)
    
    shutil.copyfile(file_path, temp_file_path)
    return temp_file_path

def delete_folder(folder):
    shutil.rmtree(folder)

def replace_color_at(file_path, color):
    """Search DEPLOYMENT_COLOR_REGEX matches and replace them by 'color'.

    Args:
        file_path (str): file to be edited
        color (str): color to edit wherever DEPLOYMENT_COLOR_REGEX matches
    """
    # read
    with open(file_path, 'r') as f:
        content = f.read()

    # replace
    match = DEPLOYMENT_COLOR_REGEX.search(content)
    while match:
        content = content.replace(match.group(0), color)  # replace tag match by given color
        match = DEPLOYMENT_COLOR_REGEX.findall(content)

    # write
    print(f'replacing file with color {color}')
    with open(file_path, 'w') as f:
        f.write(content)

def apply(file_path, color):
    """Applies a kubernetes configuration set on 'file_path' after
    replacing the 'color' wherever the DEPLOYMENT_COLOR_REGEX matches.

    Args:
        file_path (str): file to be edited
        color (str): color to edit wherever DEPLOYMENT_COLOR_REGEX matches
    """
    print(f'handling {file_path}')
    # copy the original file to a temporal folder
    temp_file_path = copy_file_to_temp(file_path)

    # replace color and apply configuration
    replace_color_at(temp_file_path, color)

    print(f'applying {file_path}')
    subprocess.call(['kubectl', 'apply' ,'-f', temp_file_path])


def get_deployment_label(deployment_name):
    """Gets current deployment color.

    Args:
        deployment_name (str): target deployment label found in
        (spec -> template -> metadata -> labels -> deployment)

    Returns:
        (str) current deployment color
    """
    ret = subprocess.check_output(['kubectl', 'get', 'deploy', deployment_name, '-o', 'json'])
    d = json.loads(ret)
    color = d['spec']['template']['metadata']['labels']['deployment']
    return color


def run(project_root, deployment_name):
    """Execute a blue-green deployment.

    Args:
        project_root (str): path to the project's root folder
        deployment_name (str): deployment's name used to get its data
    """
    # check which is the current color and deploy with new color
    old_color = get_deployment_label(deployment_name)
    print(f'Old deployment color: {old_color}')

    new_color = BLUE if old_color == GREEN else GREEN

    # deploy new color using deployment.yaml
    path = os.path.join(project_root, DEPLOYMENT_SPEC_FILE)
    apply(path, new_color)

    # check whenever new deployment is ready
    time.sleep(3)
    subprocess.call(['kubectl', 'rollout', 'status', 'deployment', deployment_name], timeout=500)

    # tell service to use new deployment applying service.yaml
    path = os.path.join(project_root, SERVICE_SPEC_FILE)
    apply(path, new_color)

    # remove temporal folder
    time.sleep(3)
    delete_folder(TEMP_FOLDER)


if __name__ == "__main__":
    # get project root and deployment name from command line attributes
    project_root = sys.argv[1]
    deployment_name = sys.argv[2]
    run(project_root, deployment_name)

