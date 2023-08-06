import logging

import rich_click as click
import rich
from rich.console import Console

from servicefoundry.build import util
from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.display_util import print_obj
from .rich_output_callback import RichOutputCallBack

from ..build.build import build_and_deploy
from .util import handle_exception
from ..build.build import LOCAL, REMOTE
from ..build.clients.service_foundry_client import ServiceFoundryServiceClient

console = Console()
logger = logging.getLogger(__name__)


def get_run_command():
    @click.command(help="Create servicefoundry run")
    @click.option("--local", is_flag=True, default=False)
    @click.option("--env", "-e", type=click.STRING)
    @click.argument("service_dir", type=click.Path(exists=True), nargs=1)
    def run(local, env, service_dir):
        try:
            build = LOCAL if local else REMOTE
            deployment = build_and_deploy(env=env, base_dir=service_dir, build=build,
                                          callback=RichOutputCallBack())
            print_obj('Deployment', deployment)
            if not CliConfig.get('json'):
                # tail logs
                tfs_client = ServiceFoundryServiceClient.get_client()
                tfs_client.tail_logs(deployment['runId'])
        except Exception as e:
            handle_exception(e)

    return run
