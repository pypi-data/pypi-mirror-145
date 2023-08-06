# ENDPOINTS
PUSH_SUPPORT_FILES_ENDPOINT = 'https://wpxkueck1a.execute-api.us-west-2.amazonaws.com/Prod/customer_download'
NAME_RESERVATION_ENDPOINT = 'https://wpxkueck1a.execute-api.us-west-2.amazonaws.com/Prod/registered_vendor_name'
PRESIGNED_REQUEST_ENDPOINT = 'https://wpxkueck1a.execute-api.us-west-2.amazonaws.com/Prod/hello'
INFERENCE_ENDPOINT_PREFIX = 'https://api.tiyaro.ai/v1/ent'

# SHARED CONSTANTS
TIYARO_TOKEN = 'TIYARO_TOKEN'
TIYARO_JOB_DESCRIPTOR = 'GIT_PYTORCH_SNAPSHOT'
TIYARO_MODEL_TYPE = 'GIT_PASSTHROUGH'

VERBOSE_HELP = f'Display more logs'

# INIT CONSTANTS
TIYARO_HANDLER_DIR = './tiyaro_handler'
ARTIFACTS_DOWNLOAD_DIR = f'{TIYARO_HANDLER_DIR}/artifacts'
ARTIFACTS_FILE_NAME = 'tiyaro_handler_templates.tgz'
ARTIFACTS_FILES_DIR = 'staging/tiyaro_handler/'
HANDLER_MODEL_MANIFEST_FILE = f'{TIYARO_HANDLER_DIR}/model_manifest.yml'
HANDLER_MODEL_MODULE_FILE = f'{TIYARO_HANDLER_DIR}/__init__.py'
HANDLER_MODEL_BASE_HANDLER_FILE = f'{TIYARO_HANDLER_DIR}/base_handler.py'
HANDLER_MODEL_MODEL_HANDLER_FILE = f'{TIYARO_HANDLER_DIR}/model_handler.py'
HANDLER_MODEL_MODEL_TEST_FILE = 'tiyaro_handler_test.py'

INIT_HELP = f'Forcefully recreates {TIYARO_HANDLER_DIR}, {HANDLER_MODEL_MODEL_TEST_FILE} templates'


# PUSH CONSTANTS
UPLOAD_ARTIFACT_DIR = './build'
GIT_SNAPSHOT_FILE_NAME = 'git_snapshot.tgz'
JSON_MANIFEST_FILE_NAME = 'manifest.json'
FILE_TO_UPLOAD = '/tmp/build.tgz'

CLEAR_HELP = f'Forcefully clear {TIYARO_HANDLER_DIR}, {HANDLER_MODEL_MODEL_TEST_FILE} templates'
