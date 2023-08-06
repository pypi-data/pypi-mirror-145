import logging

import rich_click as click
from rich import print_json

from ..build.clients.service_foundry_client import ServiceFoundryServiceClient
from .display_util import print_list, print_obj
from .util import handle_exception

logger = logging.getLogger(__name__)


def get_secret_command():
    @click.group(
        name="secret", help="servicefoundry secret show|create|remove "
    )
    def secret():
        pass

    @secret.command(name="list", help="list secrets in a group")
    @click.argument("secret_group_id")
    def list(secret_group_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.get_secrets_in_group(secret_group_id)
            print_list('Secrets', response)
        except Exception as e:
            handle_exception(e)

    @secret.command(name="show", help="show secret")
    @click.argument("secret_id")
    def show(secret_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.get_secret(secret_id)
            print_obj(response['id'], response)
        except Exception as e:
            handle_exception(e)

    @secret.command(name="create", help="create secret")
    @click.argument("secret_group_id")
    @click.argument("secret_key")
    @click.argument("secret_value")
    def create(secret_group_id, secret_key, secret_value):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.create_secret(secret_group_id, secret_key, secret_value)
            print_obj(response['id'], response)
        except Exception as e:
            handle_exception(e)

    @secret.command(name="remove", help="remove secret")
    @click.argument("secret_id")
    def remove(secret_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.delete_secret(secret_id)
            print_json(data=response)
        except Exception as e:
            handle_exception(e)

    return secret
