import subprocess

import click

from ..common.constants import (HANDLER_MODEL_MANIFEST_FILE,
                                HANDLER_MODEL_MODEL_TEST_FILE)
from ..common.utils import failed, success
from ..handler.utils import (validate_handler_exists,
                             validate_handler_test_file_exists)


@click.command()
@click.option('-p', '--pretrained', required=False, help=f'pretrained_file path or url.  default is value from {HANDLER_MODEL_MANIFEST_FILE}')
@click.option('-i', '--input', required=True, help=f'Valid JSON input string or file path')
def test(pretrained, input):
    """
    - Test model locally
    """
    do_test(pretrained, input)


def do_test(pretrained, input):
    validate_handler_exists()
    validate_handler_test_file_exists()
    if not pretrained:
        pretrained = 'from-config'

    p = subprocess.run(
        f'python {HANDLER_MODEL_MODEL_TEST_FILE} {pretrained} {input}', shell=True)
    if p.returncode == 0:
        success('Test successful !  You can push your model now.')
    else:
        failed('Test failed !')
