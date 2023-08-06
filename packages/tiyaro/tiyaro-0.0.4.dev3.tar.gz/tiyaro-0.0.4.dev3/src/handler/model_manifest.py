import imp
import os
import uuid

import click
import yaml

from ..common.constants import HANDLER_MODEL_MANIFEST_FILE, MODEL_VERSION
from .utils import validate_model_manifest_file_exists


def get_model_version():
    validate_model_manifest_file_exists()
    return f'{MODEL_VERSION}'

# TODO: this function is currently invoked only once.  If it's invoked more than once, we have to save model uuid suffix in a local state file
def get_model_name():
    validate_model_manifest_file_exists()
    return '{}_{}'.format(_get_param('name'),__rand())


def __rand(string_length=6):
    random = str(uuid.uuid4())
    return random[0:string_length]

def _get_param(field):
    with open(HANDLER_MODEL_MANIFEST_FILE, 'r') as file:
        contents = yaml.safe_load(file)
        value = contents[field]
        if (
            (value is None)
            or (not isinstance(value, str))
            or (not value.strip())
        ):
            click.echo(
                f'Please set a valid model {field} in {HANDLER_MODEL_MANIFEST_FILE}')
        return value
