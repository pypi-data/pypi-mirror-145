import fnmatch
import os
from shutil import copytree, ignore_patterns
from ..util import read_text, create_file_from_content, clean_dir

from jinja2 import Template


def prepare_build_dir(name, service_build):
    build_path = f"{service_build.build_dir}/{name}"
    clean_dir(build_path)

    build_dir = service_build.build_dir
    if build_dir.startswith("./"):
        build_dir = build_dir[2:]

    # Copy contents excluding pattern.
    if service_build.ignore_patterns:
        patterns = ignore_patterns(*service_build.ignore_patterns, f"{build_dir}*")
    else:
        patterns = ignore_patterns(f"{service_build.build_dir}")
    copytree("./", build_path, ignore=patterns)
    return build_path


def create_requirements_file(service_auto_build):
    requirement_txt_file = None
    if type(service_auto_build.packages) == str:
        requirement_txt_file = service_auto_build.packages
    return requirement_txt_file


def create_docker_file(build_path, template, **kwargs):
    create_file(f"{build_path}/Dockerfile", template, **kwargs)


def create_file(file_location, template, **kwargs):
    template = Template(read_text(template))
    file_str = template.render(**kwargs)
    create_file_from_content(file_location, file_str)
