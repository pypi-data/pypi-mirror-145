import os
import tarfile

from servicefoundry.build.model.service_def import ServiceDef
from servicefoundry.build.session_factory import get_session
from servicefoundry.build.clients.service_foundry_client import ServiceFoundryServiceClient


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        for fn in os.listdir(source_dir):
            p = os.path.join(source_dir, fn)
            tar.add(p, arcname=fn)


def deploy(env, service_def: ServiceDef, package_dir, stdout):
    package_zip = f"{service_def.build.build_dir}/{service_def.name}.tar.gz"
    make_tarfile(package_zip, package_dir)

    session = get_session()
    tf_client = ServiceFoundryServiceClient(session)
    resp = tf_client.build_and_deploy(service_def, package_zip, env)
    return resp
