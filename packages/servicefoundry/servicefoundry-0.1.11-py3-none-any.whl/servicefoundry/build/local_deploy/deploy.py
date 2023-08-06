import os.path
import sys
import urllib
import webbrowser

from ..model.service_def import ServiceDef
from ..output_callback import OutputCallBack
from ..util import execute


def deploy(env, service_def: ServiceDef, package_dir, callback: OutputCallBack):
    virtualenv = f"{service_def.build.build_dir}/virtualenv.pyz"
    if not os.path.isfile(virtualenv):
        callback.print_header("Going to download virtualenv")
        urllib.request.urlretrieve("https://bootstrap.pypa.io/virtualenv.pyz", virtualenv)

    python_location = sys.executable

    venv = f"{service_def.build.build_dir}/venv"
    if not os.path.isdir(venv):
        callback.print_header("Going to create virtualenv")
        cmd = [python_location, virtualenv, venv]
        for path in execute(cmd):
            callback.print_line(path)

    callback.print_header("Going to install dependency")
    cmd = [f"{venv}/bin/pip",
           "install",
           "-r",
           f"{package_dir}/{service_def.build.packages}"
           ]
    for path in execute(cmd):
        callback.print_line(path)

    callback.print_header("Going to run service")
    command = service_def.build.get_run_command()
    command = f"{venv}/bin/{command}"
    cmd = command.split(" ")
    iterator = execute(cmd)

    url = f"http://127.0.0.1:{service_def.build.port}"
    callback.print_line(f"Service is up on {url}\n")
    webbrowser.open(url)
    for path in iterator:
        callback.print_line(path)
