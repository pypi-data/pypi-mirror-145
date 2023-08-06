import os
import shutil
import subprocess
import tarfile
from email.policy import default

import click
import requests

from ..common.constants import *
from ..common.utils import failed, get_tiyaro_token, success, warn


@click.command()
@click.option('-f', '--force', is_flag=True, default=False, help=INIT_HELP)
@click.option('-v', '--verbose', is_flag=True, default=False, help=VERBOSE_HELP)
def init(force, verbose):
    """
    - Initializes model repo for Tiyaro Push
    """
    get_templates(force, verbose)


def get_templates(is_overwrite, is_verbose):

    if (os.path.isdir(TIYARO_HANDLER_DIR)):
        if not is_overwrite:
            warn(
                f'{TIYARO_HANDLER_DIR} already exists.  To force init, kindly use -f with your init command')
            exit(-1)
        else:
            if is_verbose:
                subprocess.run(f'tiyaro clear -f -v', shell=True)
            else:
                subprocess.run(f'tiyaro clear -f', shell=True)

    if (os.path.isfile(HANDLER_MODEL_MODEL_TEST_FILE)):
        if not is_overwrite:
            warn(f'{HANDLER_MODEL_MODEL_TEST_FILE} already exists.  To force init kindly use -f with your init command')
            exit(-1)
        else:
            subprocess.run(f'tiyaro clear -f', shell=True)

    token = get_tiyaro_token()
    resp = requests.get(
        f'{PUSH_SUPPORT_FILES_ENDPOINT}/{ARTIFACTS_FILE_NAME}',
        headers={
            'Authorization': token
        })
    if resp.status_code == 200:
        template_url = resp.content
    else:
        failed(
            f'Unable to get templates URL.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)

    os.makedirs(ARTIFACTS_DOWNLOAD_DIR)
    downloaded_artifact = f'{ARTIFACTS_DOWNLOAD_DIR}/ARTIFACTS_FILE_NAME'

    resp = requests.get(template_url, stream=True)
    if resp.status_code == 200:
        with open(downloaded_artifact, 'wb') as f:
            f.write(resp.raw.read())
    else:
        failed(
            f'Unable to get templates.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)

    def members(tf, sub_folder):
        l = len(sub_folder)
        for member in tf.getmembers():
            if member.path.startswith(sub_folder):
                member.path = member.path[l:]
                yield member

    tar = tarfile.open(downloaded_artifact)
    tar.extractall(path=TIYARO_HANDLER_DIR,
                   members=members(tar, ARTIFACTS_FILES_DIR))
    # move test file to project root for tiyaro test
    shutil.move(f'{TIYARO_HANDLER_DIR}/{HANDLER_MODEL_MODEL_TEST_FILE}',
                f'{HANDLER_MODEL_MODEL_TEST_FILE}')
    shutil.rmtree(ARTIFACTS_DOWNLOAD_DIR)
    success(
        f'Created {TIYARO_HANDLER_DIR}, {HANDLER_MODEL_MODEL_TEST_FILE} templates successfully !')
