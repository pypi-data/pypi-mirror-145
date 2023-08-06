import subprocess

import pkg_resources
import logging
import os
import shutil
import requests
import tarfile

logger = logging.getLogger()


def read_text(file_name, name=__name__):
    return pkg_resources.resource_string(name, file_name).decode("utf-8")


def clean_dir(dir_name):
    if os.path.isfile(dir_name):
        os.remove(dir_name)
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)


def create_file_from_content(file_name, content):
    with open(file_name, "w") as text_file:
        text_file.write(content)


def upload_package_to_s3(metadata, package_file):
    with open(package_file, "rb") as file_to_upload:
        http_response = requests.put(
            metadata["url"], data=file_to_upload
        )

        if http_response.status_code not in [204, 201, 200]:
            raise RuntimeError(f"Failed to upload to S3 {http_response.content}")


class BadRequestException(Exception):
    def __init__(self, status_code, message=None):
        super(BadRequestException, self).__init__()
        self.status_code = status_code
        self.message = message


def request_handling(res):
    try:
        status_code = res.status_code
    except Exception:
        raise Exception("Unknown error occurred. Couldn't get status code.")
    if 200 <= status_code <= 299:
        if res.content == b"":
            return None
        return res.json()
    if 400 <= status_code <= 499:
        try:
            message = res.json()["message"]
        except Exception:
            message = res
        raise BadRequestException(res.status_code, message)
    if 500 <= status_code <= 599:
        raise Exception(res.content)


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
