import logging

import rich_click as click
from rich import print_json

from ..build.clients.service_foundry_client import ServiceFoundryServiceClient
from .display_util import print_list, print_obj
from .util import handle_exception

logger = logging.getLogger(__name__)


def get_secret_group_command():
    @click.group(
        name="secret-group", help="servicefoundry secret-group show|create|remove "
    )
    def secret_group():
        pass

    @secret_group.command(name="list", help="list")
    def list():
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.get_secret_groups()
            print_list('Secret Groups', response)
        except Exception as e:
            handle_exception(e)

    @secret_group.command(name="show", help="show secret-group")
    @click.argument("secret_group_id")
    def show(secret_group_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.get_secret_group(secret_group_id)
            print_obj(f'Secret Group', response)
        except Exception as e:
            handle_exception(e)

    @secret_group.command(name="create", help="create secret-group")
    @click.argument("secret_group_name")
    def create(secret_group_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.create_secret_group(secret_group_name)
            print_obj(f'Secret Group', response)
        except Exception as e:
            handle_exception(e)

    @secret_group.command(name="remove", help="remove secret-group")
    @click.argument("secret_group_id")
    def remove(secret_group_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.delete_secret_group(secret_group_id)
            print_json(data=response)
        except Exception as e:
            handle_exception(e)

    return secret_group
