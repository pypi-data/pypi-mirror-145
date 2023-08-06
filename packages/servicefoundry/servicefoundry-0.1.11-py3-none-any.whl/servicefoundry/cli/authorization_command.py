import logging

import click
from rich import print_json

from servicefoundry.cli.display_util import print_list, print_obj

from ..build.clients.service_foundry_client import ServiceFoundryServiceClient
from .util import handle_exception

logger = logging.getLogger(__name__)


def get_authorization_command():
    @click.group(
        name="auth", help="servicefoundry auth list|create|update|remove "
    )
    def authorize():
        pass

    @authorize.command(name="list", help="list authorize for a resource id.")
    @click.argument("resource_type", type=click.Choice(['workspace'], case_sensitive=False))
    @click.argument("resource_id")
    def list(resource_type, resource_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.get_authorization_for_resource(resource_type, resource_id)
            print_list(f'Auth for {resource_type}: {resource_id}')
        except Exception as e:
            handle_exception(e)

    @authorize.command(name="create", help="create auth")
    @click.argument("resource_type")
    @click.argument("resource_id")
    @click.argument("user_id")
    @click.argument("role")
    def create(resource_id, resource_type, user_id, role):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.create_authorization(resource_id, resource_type, user_id, role)
            print_obj(f'Auth for {resource_type}: {resource_id}', response)
        except Exception as e:
            handle_exception(e)

    @authorize.command(name="update", help="update auth")
    @click.argument("authorization_id")
    @click.argument("role")
    def update(authorization_id, role):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.update_authorization(authorization_id, role)
        except Exception as e:
            handle_exception(e)

    @authorize.command(name="remove", help="remove authorization")
    @click.argument("authorization_id")
    def remove(authorization_id):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            response = tfs_client.delete_authorization(authorization_id)
            print_json(data=response)
        except Exception as e:
            handle_exception(e)

    return authorize
