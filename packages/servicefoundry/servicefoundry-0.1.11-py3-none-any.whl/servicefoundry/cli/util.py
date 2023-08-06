import tarfile
import zipfile

import requests
import rich_click as click
from requests.exceptions import ConnectionError
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel

from ..build.util import BadRequestException


def handle_exception(exception):
    if type(exception) == BadRequestException:
        print_error(f"[cyan bold]statusCode[/]  {exception.status_code} \n"
                    f"[cyan bold]message[/]     {exception.message}")
    elif type(exception) == ConnectionError:
        print_error(f"Couldn't connect to Servicefoundry.")
    else:
        console = Console()
        console.print(exception)


def print_error(message):
    console = Console()
    text = Padding(message, (0, 1))
    console.print(Panel(text, border_style="red", title="Command failed", title_align="left",
                        width=click.rich_click.MAX_WIDTH))


def print_message(message):
    console = Console()
    text = Padding(message, (0, 1))
    console.print(Panel(text, border_style="cyan", title="Success", title_align="left",
                        width=click.rich_click.MAX_WIDTH))


def download_file(url, file_path):
    r = requests.get(url, allow_redirects=True) 
    open(file_path, 'wb').write(r.content)


def unzip_package(path_to_package, destination):
    with zipfile.ZipFile(path_to_package, 'r') as zip_ref:
        zip_ref.extractall(destination)

def uncompress_tarfile(file_path, destination):
    file = tarfile.open(file_path)
    file.extractall(destination)
    file.close()