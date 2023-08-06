import logging

import rich_click as click
from rich import print_json
from rich.console import Console

from ..build.clients.service_foundry_client import ServiceFoundryServiceClient
from .display_util import print_list, print_obj
from .util import handle_exception

console = Console()
logger = logging.getLogger(__name__)


def get_cluster_command():
    @click.group(name="cluster", help="servicefoundry cluster list|show|create|update ")
    def workspace():
        pass

    @workspace.command(name="list", help="list cluster")
    def list():
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            clusters = tfs_client.list_cluster()
            print_list('Clusters', clusters)
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="show", help="show cluster metadata")
    @click.argument("space_name")
    def get(space_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            cluster = tfs_client.get_workspace(space_name)
            print_obj('Cluster', cluster)
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="remove", help="remove cluster")
    @click.argument("cluster_name")
    def remove(cluster_name):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            tfs_client.remove_cluster(cluster_name)
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="create", help="create new workspace")
    @click.argument("name")
    @click.argument("region")
    @click.argument("aws_account_id")
    @click.argument("server_name")
    @click.argument("ca_data")
    @click.argument("server_url")
    def create(name, region, aws_account_id, server_name, ca_data, server_url):
        try:
            tfs_client = ServiceFoundryServiceClient.get_client()
            cluster = tfs_client.create_cluster(
                name, region, aws_account_id, server_name, ca_data, server_url
            )
            print_obj('Cluser', cluster)
        except Exception as e:
            handle_exception(e)

    @workspace.command(name="update", help="update workspace")
    def update():
        click.echo("Hello world")

    return workspace
