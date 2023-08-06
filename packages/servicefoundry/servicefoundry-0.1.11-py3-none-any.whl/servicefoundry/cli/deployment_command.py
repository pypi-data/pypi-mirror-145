import logging

import rich_click as click
from rich import print_json

from servicefoundry.cli.display_util import print_list, print_obj

from ..build.clients.service_foundry_client import ServiceFoundryServiceClient
from .util import handle_exception

logger = logging.getLogger(__name__)

DISPLAY_FIELDS = ['id', 'serviceId', 'domain', 'deployedBy', 'createdAt', 'updatedAt']


def get_deployment_command():
    @click.group(name="deployment", help="servicefoundry deployment list|show ")
    def deployment():
        pass

    @deployment.command(name="list", help="list deployment")
    @click.argument("service_id")
    def list(service_id):
        try:
            tfs_client: ServiceFoundryServiceClient = ServiceFoundryServiceClient.get_client()
            deployments = tfs_client.list_deployment(service_id)
            print_list(f'Deployments of Service: {service_id}', deployments, DISPLAY_FIELDS)
        except Exception as e:
            handle_exception(e)

    @deployment.command(name="show", help="show deployment metadata")
    @click.argument("deployment_id")
    def get(deployment_id):
        try:
            tfs_client: ServiceFoundryServiceClient = ServiceFoundryServiceClient.get_client()
            deployment = tfs_client.get_deployment(deployment_id)
            print_obj('Deployment', deployment, DISPLAY_FIELDS)
        except Exception as e:
            handle_exception(e)

    return deployment
