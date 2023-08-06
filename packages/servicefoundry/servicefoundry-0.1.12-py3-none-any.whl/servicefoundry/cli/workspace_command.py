import logging
import os

import rich_click as click
from rich import print_json

from .config import CliConfig
from ..build.clients.service_foundry_client import ServiceFoundryServiceClient
from .display_util import print_list, print_obj
from .util import handle_exception

logger = logging.getLogger(__name__)

DISPLAY_FIELDS = ['id', 'name', 'namespace', 'status', 'clusterId', 'createdBy', 'createdAt', 'updatedAt']


def get_workspace_command():
    @click.group(
        name="workspace", help="servicefoundry workspace list|show|create|update "
    )
    def workspace():
        pass

    @workspace.command(name="list", help="list workspaces")
    def list():
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            spaces = tfs_client.list_workspace()
            print_list('Workspaces', spaces, DISPLAY_FIELDS)
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="show", help="show workspace metadata")
    @click.argument("workspace_name")
    def get(workspace_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            space = tfs_client.get_workspace(workspace_name)
            print_obj('Workspace', space, DISPLAY_FIELDS)
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="remove", help="remove workspace")
    @click.argument("workspace_name")
    def remove(workspace_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            space = tfs_client.remove_workspace(workspace_name)
            tfs_client.tail_logs(space['pipelinerun']['name'])
            if not CliConfig.get('json'):
                print_json(data=space)
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="create", help="create new workspace")
    @click.argument("cluster_name")
    @click.argument("space_name")
    def create(cluster_name, space_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            space = tfs_client.create_workspace(cluster_name, space_name)
            print_obj('Workspace', space['workspace'], DISPLAY_FIELDS)
            if not CliConfig.get('json'):
                tfs_client.tail_logs(space['runId'])
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="update", help="update workspace")
    def update():
        click.echo("Hello world")

    return workspace
