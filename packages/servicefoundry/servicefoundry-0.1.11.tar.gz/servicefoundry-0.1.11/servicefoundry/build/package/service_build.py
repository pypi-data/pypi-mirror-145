# from depfoundry.dependency_generator import RequirementsGenerator, find_local_py_modules
# from depfoundry.depfoundry import build_dependency
import logging
from .util import prepare_build_dir, create_requirements_file, create_docker_file
from servicefoundry.build.model.service_def import ServiceBuild

logger = logging.getLogger()


def package(name, service_build: ServiceBuild):
    build_path = prepare_build_dir(name, service_build)

    create_docker_file(
        build_path,
        "package/docker_template/python_service.j2",
        python_version=service_build.version,
        requirement_txt_file=service_build.get_requirement_txt(),
        packages=service_build.get_packages(),
        run_command=service_build.get_run_command(),
    )

    return build_path
