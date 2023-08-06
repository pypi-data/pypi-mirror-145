import os
import pathlib
import shutil

import toml
from dotenv import dotenv_values
from pydantic import BaseModel, BaseSettings

from . import __version__
from .constants import STATIC_USER_ID, STATIC_WBS_CLIENT_SUB

EAD_SCHEMA_FILE = "ead-app-schema-draft-3.json"
EATS_NET = "eats"


class JobEnv:
    class JobEnvSettings(BaseModel):
        empaia_job_id: str
        empaia_token: str
        empaia_app_api: str

    def __init__(self, env_file, encoding="utf-8"):
        values = dotenv_values(env_file, encoding=encoding)
        values = {key.lower(): val for key, val in values.items()}
        self.settings = self.JobEnvSettings(**values)


class EatsSettings(BaseSettings):
    debug: bool = False

    class Config:
        env_prefix = "eats_"
        env_file = ".env"


def get_databases():
    return [
        {
            "name": "eats-postgres-db",
            "image": "registry.gitlab.com/empaia/integration/ci-docker-images/custom-postgres:0.1.4",
            "command": "postgres -c config_file=/etc/postgresql/postgresql.conf",
            "environment": {
                "POSTGRES_DB": "eats",
                "POSTGRES_USER": "empaia",
                "POSTGRES_PASSWORD": "empaia",
            },
            "volume": {
                "name": "eats-postgres-db-vol",
                "mount": "/var/lib/postgresql/data",
            },
        },
        {
            "name": "eats-mongo-db",
            "image": "mongo:3.6.9",
            "environment": {},
            "volume": {
                "name": "eats-mongo-db-vol",
                "mount": "/data/db",
            },
        },
    ]


def get_services(
    nginx_port=None,
    wbs_url=None,
    isyntax_sdk=None,
    gpu_driver=None,
    frontend_token_exp=None,
    scope_token_exp=None,
    app_ui_frame_ancestors=None,
    app_ui_connect_src=None,
):
    nginx_port = nginx_port or 8888
    frontend_token_exp = frontend_token_exp or 86400
    scope_token_exp = scope_token_exp or 86400

    wbs_url = wbs_url.rstrip("/") if wbs_url else f"http://localhost:{nginx_port}/wbs-api"

    if app_ui_frame_ancestors is None:
        app_ui_frame_ancestors = ""

    if app_ui_connect_src is None:
        app_ui_connect_src = ""

    path_to_this_file = pathlib.Path(__file__).parent.absolute()
    path_to_services = os.path.join(path_to_this_file, "services")
    default_version = f"eats-{__version__}"

    path_to_this_file = pathlib.Path(__file__).parent.absolute()
    path_to_services = os.path.join(path_to_this_file, "services")

    services = [
        {
            "name": "app-service",
            "image": "registry.gitlab.com/empaia/services/app-service:0.5.6",
            "environment": {
                "AS_IDP_URL": "https://url",
                "AS_VS_URL": "http://marketplace-service-mock:8000",
                "AS_CLIENT_ID": "id",
                "AS_CLIENT_SECRET": "secret",
                "AS_MDS_URL": "http://medical-data-service:8000",
                "AS_ROOT_PATH": "/app-api",
            },
            "command": ["--port=8000", "--host=0.0.0.0"],
            "ports": {},
        },
        {
            "name": "annotation-service",
            "image": "registry.gitlab.com/empaia/services/annotation-service:0.14.28",
            "environment": {
                "ANNOT_DB_HOST": "eats-postgres-db",
                "ANNOT_DB_PORT": 5432,
                "ANNOT_DB": "eats",
                "ANNOT_DB_USERNAME": "empaia",
                "ANNOT_DB_PASSWORD": "empaia",
                "ANNOT_API_V1_INTEGRATION": "annotation_service.api.v1.integrations.disable_auth:DisableAuth",
                "ANNOT_ALLOW_EXTERNAL_IDS": "True",
                "ANNOT_ITEM_LIMIT": 10000,
                "ANNOT_POST_LIMIT": 10000,
            },
            "command": ["run.sh", "--host=0.0.0.0", "--workers=4", "--port=8000"],
            "ports": {},
        },
        {
            "name": "job-service",
            "image": "registry.gitlab.com/empaia/services/job-service:0.4.39",
            "environment": {
                "JS_DB_HOST": "eats-postgres-db",
                "JS_DB_PORT": 5432,
                "JS_DB": "eats",
                "JS_DB_USERNAME": "empaia",
                "JS_DB_PASSWORD": "empaia",
                "JS_RSA_KEYS_DIRECTORY": "/app/rsa",
            },
            "command": ["run.sh", "--host=0.0.0.0", "--port=8000"],
            "ports": {},
            "volume": {
                "name": "job-service-vol",
                "mount": "/app/rsa",
            },
        },
        {
            "name": "examination-service",
            "image": "registry.gitlab.com/empaia/services/examination-service:0.6.20",
            "environment": {
                "ES_DB_HOST": "eats-postgres-db",
                "ES_DB_PORT": 5432,
                "ES_DB": "eats",
                "ES_DB_USERNAME": "empaia",
                "ES_DB_PASSWORD": "empaia",
                "ES_API_V1_INTEGRATION": "examination_service.api.v1.integrations.disable_auth:DisableAuth",
                "ES_SCOPE_TOKEN_EXP": scope_token_exp,
            },
            "command": ["run.sh", "--host=0.0.0.0", "--port=8000"],
            "ports": {},
        },
        {
            "name": "clinical-data-service",
            "image": "registry.gitlab.com/empaia/services/clinical-data-service:0.2.27",
            "environment": {
                "CDS_DB_HOST": "eats-postgres-db",
                "CDS_DB_PORT": 5432,
                "CDS_DB": "eats",
                "CDS_DB_USERNAME": "empaia",
                "CDS_DB_PASSWORD": "empaia",
                "CDS_ALLOW_EXTERNAL_IDS": "True",
            },
            "command": ["run.sh", "--host=0.0.0.0", "--port=8000"],
            "ports": {},
        },
        {
            "name": "storage-mapper-service",
            "image": "registry.gitlab.com/empaia/services/storage-mapper-service:0.1.14",
            "environment": {
                "SM_DB_USERNAME": "empaia",
                "SM_DB_PASSWORD": "empaia",
                "SM_DB": "eats",
                "SM_DB_HOST": "eats-postgres-db",
                "SM_DB_PORT": 5432,
            },
            "command": [],
            "ports": {},
        },
        {
            "name": "wsi-service",
            "image": "registry.gitlab.com/empaia/services/wsi-service-plugin-integration:0.7.4",
            "environment": {
                "WS_DATA_DIR": "/data",
                "WS_MAPPER_ADDRESS": "http://storage-mapper-service:8000/v1/slides/{slide_id}",
            },
            "command": [],
            "ports": {},
        },
        {
            "name": "medical-data-service",
            "image": "registry.gitlab.com/empaia/services/medical-data-service:0.4.52",
            "environment": {
                "MDS_API_V1_INTEGRATION": "medical_data_service.api.v1.integrations.disable_auth:DisableAuth",
                "MDS_WS_URL": "http://wsi-service:8080",
                "MDS_SMS_URL": "http://storage-mapper-service:8000",
                "MDS_JS_URL": "http://job-service:8000",
                "MDS_AS_URL": "http://annotation-service:8000",
                "MDS_CDS_URL": "http://clinical-data-service:8000",
                "MDS_ES_URL": "http://examination-service:8000",
                "MDS_ROOT_PATH": "/mds-api",
            },
            "command": ["uvicorn", "--host=0.0.0.0", "--port=8000", "--workers=2", "medical_data_service.app:app"],
            "ports": {},
        },
        {
            "name": "ead-validation-service",
            "image": "registry.gitlab.com/empaia/services/ead-validation-service:0.1.3",
            "environment": {},
            "ports": {},
            "command": [
                "java",
                "-DeadValidation.schemaLocation=schemas/ead-app-schema-draft-3.json",
                "-jar",
                "ead-validation.jar",
            ],
        },
        {
            "name": "marketplace-service-mock",
            "image": "registry.gitlab.com/empaia/service-mocks/marketplace-service-mock:0.1.3",
            "environment": {
                "MPSM_API_V1_INTEGRATION": "marketplace_service_mock.api.v1.integrations.disable_auth:DisableAuth",
                "MPSM_ROOT_PATH": "/mps-api",
            },
            "command": ["uvicorn", "--host=0.0.0.0", "--port=8000", "marketplace_service_mock.app:app"],
            "ports": {},
            "volume": {
                "name": "marketplace-service-mock-vol",
                "mount": "/data",
            },
        },
        {
            "name": "aaa-service-mock",
            "image": "registry.gitlab.com/empaia/service-mocks/aaa-service-mock:0.1.4",
            "environment": {
                "AAAM_API_V1_INTEGRATION": "aaa_service_mock.api.v1.integrations.disable_auth:DisableAuth",
                "AAAM_ROOT_PATH": "/aaa-api",
            },
            "command": ["uvicorn", "--host=0.0.0.0", "--port=8000", "aaa_service_mock.app:app"],
            "ports": {},
            "volume": {
                "name": "aaa-service-mock-vol",
                "mount": "/data",
            },
        },
        {
            "name": "job-execution-service",
            "image": "registry.gitlab.com/empaia/services/job-execution-service:0.4.7",
            "environment": {
                "JES_DATABASE_URL": "mongodb://eats-mongo-db:27017",
                "JES_DOCKER_NETWORK": EATS_NET,
                "JES_DOCKER_GPU_DRIVER": gpu_driver,
                "JES_JOB_RUNNER": "EVENTED",
                "JES_MAX_NUMBER_OF_JOBS": 1,
                "JES_ENABLE_RECEIVER_AUTH": "False",
                "JES_DOCKER_ALWAYS_PULL": "False",
                "JES_MPS_URL": "http://marketplace-service-mock:8000",
                "JES_ROOT_PATH": "/jes-api",
            },
            "command": [],
            "ports": {},
            "volume": {
                "name": "/var/run/docker.sock",
                "mount": "/var/run/docker.sock",
            },
        },
        {
            "name": "workbench-daemon",
            "image": "registry.gitlab.com/empaia/services/workbench-daemon:0.2.2",
            "environment": {
                "WBD_MDS_URL": "http://medical-data-service:8000",
                "WBD_JES_URL": "http://job-execution-service:8000",
                "WBD_CLIENT_SUB": STATIC_WBS_CLIENT_SUB,
            },
            "command": ["wbd"],
            "ports": {},
        },
        {
            "name": "workbench-service",
            "image": "registry.gitlab.com/empaia/services/workbench-service:0.5.100",
            "environment": {
                "WBS_ENABLE_EATS_MODE": "True",
                "WBS_AAA_SERVICE_URL": "http://aaa-service-mock:8000",
                "WBS_MEDICAL_DATA_SERVICE_URL": "http://medical-data-service:8000",
                "WBS_APP_SERVICE_URL": "http://app-service:8000",
                "WBS_JOB_EXECUTION_SERVICE_URL": "http://job-execution-service:8000",
                "WBS_MARKETPLACE_SERVICE_URL": "http://marketplace-service-mock:8000",
                "WBS_CORS_ALLOW_ORIGINS": '["*"]',
                "WBS_API_V1_INTEGRATION": "workbench_service.api.v1.integrations.disable_auth:DisableAuth",
                "WBS_API_V2_INTEGRATION": "workbench_service.api.v2.integrations.disable_auth:DisableAuth",
                "WBS_CLIENT_SUB": STATIC_WBS_CLIENT_SUB,
                "WBS_FRONTEND_TOKEN_EXP": frontend_token_exp,
                "WBS_ROOT_PATH": "/wbs-api",
                "WBS_APP_UI_FRAME_ANCESTORS": app_ui_frame_ancestors,
                "WBS_APP_UI_CONNECT_SRC": app_ui_connect_src,
            },
            "command": ["run.sh", "--host=0.0.0.0", "--port=8000"],
            "ports": {},
            "extra_hosts": {"host.docker.internal": "host-gateway"},
        },
        {
            "name": "workbench-client",
            "image": "registry.gitlab.com/empaia/integration/frontend-workspace/workbench-client:0.1.0",
            "environment": {
                "WBC_WBS_SERVER_API_URL": wbs_url,
                "WBC_WBS_USER_ID": STATIC_USER_ID,
            },
            "ports": {},
            "command": [],
        },
        {
            "name": "workbench-client-v2",
            "image": "registry.gitlab.com/empaia/integration/frontend-workspace/workbench-client-v2:0.2.0",
            "environment": {
                "WBC_WBS_SERVER_API_URL": wbs_url,
                "WBC_WBS_USER_ID": STATIC_USER_ID,
            },
            "ports": {},
            "command": [],
        },
        {
            "name": "workbench-client-v2-sample-ui",
            "image": "registry.gitlab.com/empaia/integration/frontend-workspace/sample-app:0.1.0",
            "environment": {},
            "command": [],
        },
        {
            "name": "nginx",
            "environment": {},
            "path": str(pathlib.Path(path_to_services, "nginx")),
            "dockerfile_path": "Dockerfile",
            "ports": {"80": nginx_port},
            "command": [],
        },
    ]

    # check for isyntax sdk
    isyntax_sdk_path = os.path.join(
        path_to_services,
        "wsi-service-plugin-isyntax/isyntax_backend",
        "philips-pathologysdk-2.0-ubuntu18_04_py36_research.zip",
    )
    if isyntax_sdk:
        shutil.copy(isyntax_sdk, isyntax_sdk_path)
        services.append(
            {
                "name": "isyntax-backend",
                "environment": {},
                "ports": {},
                "command": [],
                "path": str(pathlib.Path(path_to_services, "wsi-service-plugin-isyntax/isyntax_backend")),
            }
        )

    for service in services:
        if "path" not in service:
            service["path"] = str(pathlib.Path(path_to_services, service["name"]))

        if "image" not in service:
            pyproject_file = pathlib.Path(service["path"], "pyproject.toml")
            version = default_version
            if pyproject_file.exists():
                version = toml.load(pyproject_file)["tool"]["poetry"]["version"]
            service["image"] = "eats-" + service["name"] + ":" + version

    return services
