import logging
import os
import os.path
import shutil
from secrets import choice
from turtle import down

import questionary
import rich_click as click
import yaml
from jinja2 import Template
from questionary import Choice
from rich.console import Console

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.session_factory import get_session
from servicefoundry.cli.const import TEMP_FOLDER, TEMPLATE_INDEX_FILE_URL
from servicefoundry.cli.login_command import login_user
from servicefoundry.cli.util import download_file, uncompress_tarfile

from ..build.util import BadRequestException

console = Console()
logger = logging.getLogger(__name__)

def get_init_command():
    @click.command(help="Initialize new service for servicefoundry")
    def init():
        try:
            get_session()
        except BadRequestException:
            doLogin = questionary.select('You need to login to create a project', [
                                       'Login', 'Exit']).ask()
            if doLogin == 'Login':
                login_user()
            else:
                return

        if os.path.exists(TEMP_FOLDER):
            shutil.rmtree(TEMP_FOLDER)
        os.mkdir(TEMP_FOLDER)

        download_file(TEMPLATE_INDEX_FILE_URL, f'{TEMP_FOLDER}/index.yaml')
        
        with open(f'{TEMP_FOLDER}/index.yaml', 'r') as file:
            templates = yaml.safe_load(file)
        
        template_choices = [Choice(f'{t["id"]} - {t["description"]}', value=t['id']) for t in templates]
        template_id = questionary.select('Choose a template', template_choices).ask()

        package_url = f'https://github.com/truefoundry/servicefoundry-templates/raw/gh-pages/{template_id}.tgz'

        package_file = f'{TEMP_FOLDER}/{template_id}.tgz'
        template_folder = f'{TEMP_FOLDER}/{template_id}'
        download_file(package_url, package_file)
        uncompress_tarfile(package_file, template_folder)

        template_details = None
        with open(f'{template_folder}/template.yaml', 'r') as stream:
            template_details = yaml.safe_load(stream)

        param_value_dict = {}
        for param in template_details.get('params', []):
            if (param['type'] in ['string', 'number']):
                param_value_dict[param['id']] = questionary.text(
                    param['prompt'], default=param['default']).ask()
            elif (param['type'] == 'options'):
                param_value_dict[param['id']] = questionary.select(
                    param['prompt'], choices=param['options']).ask()
            elif (param['type'] == 'tfy-workspace'):
                tfs_client = ServiceFoundryServiceClient.get_client()
                spaces = tfs_client.list_workspace()
                if len(spaces) == 0:
                    console.print(
                        'You do not have any workspaces. Create one using', end=' ')
                    console.print(
                        'servicefoundry workspace create <CLUSTER_ID> <WORKSPACE_NAME>', end=' ', style='red')
                    return

                param_value_dict[param['id']] = questionary.select(
                    param['prompt'], choices=[space['id'] for space in spaces]).ask()

        template = None
        with open(f'{template_folder}/servicefoundry.yaml', 'r') as template_file:
            template = Template(template_file.read())

        with open(f'{template_folder}/servicefoundry.yaml', 'w') as template_file:
            template_file.write(template.render(param_value_dict))

        new_folder = param_value_dict.get('service_name', f'{template_id}_service')
        if os.path.exists(new_folder):
            console.print('Failed to create project directory.', end=' ')
            console.print(new_folder, end=' ', style='red')
            console.print('already exists.')
        else:
            shutil.move(template_folder, new_folder)
            console.print(
                f'Your ServiceFoundry project is created in [bold]{new_folder}![/]')

        if os.path.exists(TEMP_FOLDER):
            shutil.rmtree(TEMP_FOLDER)

    return init
