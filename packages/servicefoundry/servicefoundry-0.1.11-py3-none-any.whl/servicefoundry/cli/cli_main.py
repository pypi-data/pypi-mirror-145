import rich_click as click

from servicefoundry.cli.config import CliConfig

click.rich_click.STYLE_ERRORS_SUGGESTION = "blue italic"
click.rich_click.MAX_WIDTH = 100

from .authorization_command import get_authorization_command
from .cluster_command import get_cluster_command
from .deployment_command import get_deployment_command

# from .version import __version__
from .init_command import get_init_command
from .login_command import get_login_command
from .run_command import get_run_command
from .secret_command import get_secret_command
from .secret_group_command import get_secret_group_command
from .service_command import get_service_command
from .workspace_command import get_workspace_command


def create_service_foundry_cli():
    """Generates CLI by combining all subcommands into a main CLI and returns in
    Returns:
        function: main CLI functions will all added sub-commands
    """
    _cli = service_foundry_cli
    init_sub_command = get_init_command()
    run_sub_command = get_run_command()
    login_sub_command = get_login_command()
    workspace_sub_command = get_workspace_command()
    cluster_sub_command = get_cluster_command()
    deployment_sub_command = get_deployment_command()
    service_sub_command = get_service_command()

    _cli.add_command(init_sub_command)
    _cli.add_command(run_sub_command)
    _cli.add_command(login_sub_command)
    _cli.add_command(workspace_sub_command)
    _cli.add_command(cluster_sub_command)
    _cli.add_command(deployment_sub_command)
    _cli.add_command(service_sub_command)
    _cli.add_command(get_secret_group_command())
    _cli.add_command(get_secret_command())
    _cli.add_command(get_authorization_command())
    return _cli


@click.group()
@click.option("--json", is_flag=True)
@click.option("--logs", is_flag=True)
def service_foundry_cli(json, logs):
    CliConfig.set('json', json)
    CliConfig.set('logs', logs)
