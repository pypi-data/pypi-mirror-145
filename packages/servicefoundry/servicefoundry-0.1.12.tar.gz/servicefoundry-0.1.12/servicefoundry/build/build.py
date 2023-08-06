import os

from .const import SERVICE_DEF_FILE_NAME
from .output_callback import OutputCallBack
from .package.packaging_factory import package
from .model.service_def import ServiceDef
from .parser.parser import Parser

from .local_deploy.deploy import deploy as local_deploy
from .remote_deploy.deploy import deploy as remote_deploy

LOCAL = "local"
REMOTE = "remote"


def run_local_from_file(service_file):
    pass


def build_and_deploy(env, base_dir="./", service_def_file_name=SERVICE_DEF_FILE_NAME,
                     build=REMOTE, callback=OutputCallBack()):
    if not base_dir.endswith("/"):
        base_dir = f"{base_dir}/"
    os.chdir(base_dir)

    if not os.path.isfile(service_def_file_name):
        raise RuntimeError(
            f"Service definition {service_def_file_name} doesn't exist in {base_dir}"
        )

    service_def: ServiceDef = Parser().parse(service_def_file_name)
    package_dir = package(service_def.name, service_def.build)

    if build == LOCAL:
        return local_deploy(env, service_def, package_dir, callback)
    elif build == REMOTE:
        return remote_deploy(env, service_def, package_dir, callback)
    else:
        raise RuntimeError(f"Unrecognised build type {build}")



