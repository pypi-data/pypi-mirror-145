import os

import click

from .constants import INFERENCE_ENDPOINT_PREFIX, TIYARO_TOKEN


def wip():
    warn(f'** WORK IN PROGRESS **\n Please wait for new version release..')


def get_tiyaro_token():
    token = os.getenv(TIYARO_TOKEN, None)
    if token is None:
        click.echo(f'Please set {TIYARO_TOKEN} env var')
        exit(-1)
    return token


def get_model_endpoint(vendor, version, model):
    return f'{INFERENCE_ENDPOINT_PREFIX}/{vendor}/{version}/{model}'


def success(msg, is_verbose=True):
    if is_verbose:
        click.secho(msg, fg='green')


def failed(msg, is_verbose=True):
    if is_verbose:
        click.secho(msg, fg='red')


def warn(msg, is_verbose=True):
    if is_verbose:
        click.secho(msg, fg='yellow')
