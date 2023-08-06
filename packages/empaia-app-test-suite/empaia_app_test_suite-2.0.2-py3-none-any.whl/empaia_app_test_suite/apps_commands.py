import json
from datetime import datetime
from uuid import uuid4

import requests

from .print_helpers import PrintStep
from .shared import ValidationError, get_service_url


def get_mps_apps_list(client):
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")
    r = requests.get(f"{mps_url}/api/v0/app/list")
    r.raise_for_status()
    return r.json()


def apps_register(client, ead, docker_image, config_file=None, app_ui_url=None):
    mps_url = get_service_url(client=client, service_name="marketplace-service-mock")
    eadvs_url = get_service_url(client=client, service_name="ead-validation-service")
    aaa_url = get_service_url(client=client, service_name="aaa-service-mock")

    with PrintStep("Validate EAD"):
        _validate_ead(eadvs_url, ead)
    with PrintStep("Validate configuration"):
        config = _validate_configuration_parameters(ead, config_file)
    if len(client.images.list(name=docker_image)) == 0:
        with PrintStep(f"Pull image {docker_image}"):
            client.images.pull(docker_image)
    else:
        with PrintStep("Image found on host system"):
            pass
    with PrintStep("Register app"):
        aaa_orga = _generate_organization_json(name="placeholder", organization_id=1)
        _aaa_post_organization(aaa_url, aaa_orga)
        mps_app = _generate_app_json(ead, docker_image, aaa_orga, app_ui_url)
        _mps_post_app(mps_url, mps_app)
        app_id = mps_app["id"]
    if config_file:
        with PrintStep("Register configuration"):
            _register_configuration_parameters(app_id, config_file, config, mps_url)

    return mps_app


def _generate_app_json(ead: dict, docker_registry: str, organization: dict, app_ui_url: str):
    now = str(datetime.now())
    data = {
        "mapp": {
            "name": ead["name_short"],
            "description": ead["description"],
            "tags": [{"tagGroup": "string", "tagName": "string", "id": "string"}],
            "id": str(uuid4()),
            "vendor_name": organization["name"],
            "vendor_uuid": organization["keycloak_id"],
            "vendor_id": organization["organization_id"],
            "created_at": now,
            "updated_at": now,
        },
        "aim": {
            "name": "string",
            "namespace": docker_registry,
            "tag": "string",
            "hash": "string",
            "size": 0,
            "id": "string",
            "uploaded_at": now,
        },
        "ead": {
            "content": ead,
            "id": str(uuid4()),
        },
        "amd": {
            "id": "string",
            "description": "string",
            "store_url": "https://www.empaia.org/",
            "store_docs_url": "https://www.empaia.org/",
            "change_log": "string",
            "medias": [
                {
                    "id": "string",
                    "image": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Microscope_icon_%28black_OCL%29.svg",
                    "alternative_image": "string",
                    "video": "string",
                    "description": "string",
                    "media_type": "VIDEO",
                    "step_number": 0,
                }
            ],
            "status": "ACCEPTED",
        },
        "version": ead["namespace"].split(".")[-1],
        "status": "ACCEPTED",
        "id": str(uuid4()),
        "created_at": now,
        "app_ui_url": app_ui_url,
    }
    return data


def _generate_organization_json(name: str, organization_id: int):
    now = str(datetime.now())
    data = {
        "organization_id": organization_id,
        "keycloak_id": str(uuid4()),
        "name": name,
        "normalized_name": name,
        "street_name": "string",
        "street_number": "string",
        "zip_code": "string",
        "place_name": "string",
        "country_code": "string",
        "department": "string",
        "email": "string",
        "phone_number": "string",
        "fax_number": "string",
        "website": "string",
        "picture": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Microscope_icon_%28black_OCL%29.svg",
        "organization_role": "AI_VENDOR",
        "account_state": "ACTIVE",
        "date_created": now,
        "date_last_change": now,
        "contact_person_user_id": 0,
        "clientGroups": [
            {
                "client_group_id": 0,
                "group_organization_id": 0,
                "group_type": "AAA_SERVICE",
                "group_namespace": "string",
                "group_authorization_from": [
                    {"client_group_authorization_id": 0, "authorization_from": 0, "authorization_for": 0}
                ],
                "group_authorization_for": [
                    {"client_group_authorization_id": 0, "authorization_from": 0, "authorization_for": 0}
                ],
                "clients": [
                    {
                        "client_id": "string",
                        "name": "string",
                        "url": "string",
                        "group_id": 0,
                        "keycloak_id": "string",
                        "description": "string",
                        "token_lifetime_in_seconds": 0,
                        "redirect_uris": ["string"],
                    }
                ],
            }
        ],
        "solutions": [{"organization_id": 0, "solution_id": 0}],
        "user_count": 0,
    }
    return data


def _register_configuration_parameters(app_id: str, config_file: str, config: dict, mps_url):
    if config_file:
        url = f"{mps_url}/api/v0/admin/{app_id}"
        r = requests.post(url, json=config)
        r.raise_for_status()


def _validate_ead(eadvs_url: str, ead: dict):
    try:
        url = f"{eadvs_url}/api/v0/validate"
        r = requests.post(url, json=ead)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error = f"Validation of EAD failed: {e}, {r.content}, {r.status_code}"
        raise ValidationError(error) from e
    except requests.exceptions.RequestException as e:
        error = f"Validation of EAD failed: {e}"
        raise ValidationError(error) from e


def _validate_configuration_parameters(ead: dict, config_file: str):
    if "configuration" in ead:
        if not config_file:
            raise ValidationError("Configuration file needed due to defined configuration section in EAD")
        # if str(Path(input_dir).expanduser()) == str(Path(config_file).expanduser().parent):
        #     raise ValidationError("Configuration file must not reside in [input_folder]")
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        for ead_config_name in ead["configuration"]:
            item_is_optional = ead["configuration"][ead_config_name].get("optional", False)
            if ead_config_name not in config and not item_is_optional:
                raise ValidationError(
                    f"Configuration entry {ead_config_name} defined in EAD not present in given config file"
                )
            if "type" not in ead["configuration"][ead_config_name]:
                raise ValidationError(f"Configuration entry {ead_config_name} does not have a type")
            if ead_config_name in config:
                required_type_name = ead["configuration"][ead_config_name]["type"]
                provided_type = type(config[ead_config_name])
                if not required_type_name.startswith(provided_type.__name__):
                    raise ValidationError(
                        f"Configuration entry {ead_config_name} defined in EAD must have type {required_type_name}"
                    )
        return config
    elif config_file:
        raise ValidationError("Configuration file given although no configuration section present in EAD")


def _mps_post_app(mps_url, data):
    url = f"{mps_url}/api/v0/custom-mock/app"
    r = requests.post(url, json=data)
    return r


def _aaa_post_organization(sss_url, data):
    url = f"{sss_url}/api/custom-mock/organization"
    r = requests.post(url, json=data)
    return r
