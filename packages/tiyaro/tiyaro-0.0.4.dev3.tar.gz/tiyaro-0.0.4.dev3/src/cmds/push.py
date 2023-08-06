import base64
import hashlib
import json
import os

import click
import requests

from ..common.constants import *
from ..common.utils import (failed, get_model_endpoint, get_tiyaro_token,
                            success, warn)
from ..handler.model_manifest import get_model_name, get_model_version
from ..handler.utils import validate_handler_exists


@click.command()
@click.option('-v', '--verbose', is_flag=True, default=False, help=VERBOSE_HELP)
def push(verbose):
    """
    - Pushes model repo to Tiyaro Infrastructure
    """
    do_push(verbose)


def push_model(tiyaro_jwt_token: str, is_verbose):
    tiyaro_model_name = get_model_name()
    tiyaro_model_version = get_model_version()

    def tiyaro_get_name_reservation_record(api_token):
        headers = {
            "Authorization": f"Bearer {api_token}"
        }

        resp = requests.get(url=NAME_RESERVATION_ENDPOINT, headers=headers)
        if resp.status_code not in (200, 201):
            failed(
                f"Failed to reserve namespace.  Error code on {NAME_RESERVATION_ENDPOINT}: STATUS {resp.status}, REASON {resp.content}")
            warn('Kindly reach out to Tiyaro Support Team')
            exit(-1)
        return json.loads(resp.content)

    tiyaro_model_vendor = tiyaro_get_name_reservation_record(tiyaro_jwt_token)[
        'vendor_name']

    # TODO - USING PYTHON
    os.system(f"mkdir -p {UPLOAD_ARTIFACT_DIR}")
    # os.system("cp ./.tiyaro-install/state.json ./build") TODO: MULTI MODELS
    os.system(
        f"git archive --output={UPLOAD_ARTIFACT_DIR}/{GIT_SNAPSHOT_FILE_NAME} HEAD .")

    package_for_upload_client(UPLOAD_ARTIFACT_DIR, tiyaro_model_name,
                              tiyaro_model_vendor, tiyaro_model_version, tiyaro_jwt_token, is_verbose)

    success(
        f'\n***Uploaded {tiyaro_model_name} to be converted onto Tiyaro Infrastructure', is_verbose)
    return get_model_endpoint(tiyaro_model_vendor, tiyaro_model_version, tiyaro_model_name)


def package_for_upload_client(build_subdir, tiyaro_model_name, tiyaro_model_vendor, model_version, tiyaro_jwt_token, is_verbose):
    # TODO: Also send git hash info
    manifest_json = {
        'tiyaro_job_descriptor': TIYARO_JOB_DESCRIPTOR,
        'env_TIYARO_PUSH_NAME_BASE': None,
        'model_name': tiyaro_model_name,
        'model_vendor': tiyaro_model_vendor,
        'version': model_version,
        'model_type': TIYARO_MODEL_TYPE,
        'tiyaro_authorization_token': tiyaro_jwt_token
    }

    # Need to decorate with some tensor-specific information
    # with signature input and output

    manifest_json_filename = '/'.join([build_subdir, JSON_MANIFEST_FILE_NAME])
    with open(manifest_json_filename, 'w') as fout:
        fout.write(json.dumps(manifest_json, indent=4))

    required_header = 'file-upload-md5-binary-base64'

    success('START - Tarballing the artifacts into a single file', is_verbose)
    os.system(f'tar cf - {build_subdir} | gzip > {FILE_TO_UPLOAD}')
    success('FINISH - Tarballing the artifacts into a single file', is_verbose)

    success('START - Generating MD5 for tarball', is_verbose)

    def file_md5_hash_binary(filename: str) -> bytes:
        with open(filename, 'rb') as fin:
            file_contents = fin.read()
            return hashlib.md5(file_contents).digest()

    md5_binary = file_md5_hash_binary(FILE_TO_UPLOAD)
    md5_binary_b64_encoded = base64.b64encode(md5_binary).decode('ascii')
    success(
        f'FINISH - Generating MD5 {md5_binary_b64_encoded} for tarball', is_verbose)

    success('START - Requesting a presigned url for upload', is_verbose)
    response_presigned_request = requests.get(
        PRESIGNED_REQUEST_ENDPOINT,
        headers={
            required_header: md5_binary_b64_encoded,
            'Authorization': tiyaro_jwt_token
        })
    if response_presigned_request.status_code == 401:
        failed(
            f'Token Authorization Error.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)
    elif response_presigned_request.status_code != 200:
        failed(
            f'Failed to received the presigned url from API endpoint {PRESIGNED_REQUEST_ENDPOINT}.', is_verbose)
        exit(-1)

    response_presigned_request_json = response_presigned_request.json()
    url = response_presigned_request_json['post_url']
    data = response_presigned_request_json['post_data_required']
    bucket_name = url.split('//')[1].split('.')[0]
    bucket_key = data['key']
    # click.echo(f'INFO - Received a presigned for S3 bucket {bucket_name} and key {bucket_key}')
    success(f'FINISH - Received a presigned url for upload {url}', is_verbose)

    size_payload = os.path.getsize(FILE_TO_UPLOAD)
    success(
        f'START - Upload of payload size {str(round(size_payload / (1024 * 1024), 2))}MB to a presigned url for upload {url}')
    with open(FILE_TO_UPLOAD, 'rb') as test_file_to_upload:
        # the key supposed to be file may be
        files = {'file': test_file_to_upload}
        response_file_upload = requests.post(url, data=data, files=files)
    if response_file_upload.status_code != 204:
        failed(f'Failed to upload the {FILE_TO_UPLOAD} to API endpoint {url}.')
        exit(-1)

    success(f'FINISH - Upload to a presigned url for upload {url}')
    os.remove(FILE_TO_UPLOAD)
    return bucket_name, bucket_key


def do_push(is_verbose):
    validate_handler_exists()
    token = get_tiyaro_token()
    api = push_model(token, is_verbose)
    result = f'\t\t\tYour model will be available at : {api}'
    star_count = len(result) + 25
    success('\n\n\t {}'.format("*"*star_count))
    success(result)
    success('\t {}'.format("*"*star_count))
