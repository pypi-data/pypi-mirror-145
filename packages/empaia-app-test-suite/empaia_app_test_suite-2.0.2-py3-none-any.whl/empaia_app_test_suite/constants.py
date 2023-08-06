STATIC_USER_ID = "02792914-0eb0-4c72-a896-a4de43f0371a"
STATIC_CASE_ID = "e5087613-ac4b-4bf9-9d0e-dd37917c3277"
STATIC_WBS_CLIENT_SUB = "1e96c2f8-e1f3-4a7a-b3ba-9717314f3ad1"
ALLOWED_ANNOTATION_TYPES = [
    "point",
    "line",
    "arrow",
    "rectangle",
    "polygon",
    "circle",
]

ALLOWED_PRIMITIVE_TYPES = ["integer", "float", "bool", "string"]

SERVICE_API_MAPPING = {
    "workbench-service": "wbs-api",
    "medical-data-service": "mds-api",
    "job-execution-service": "jes-api",
    "app-service": "app-api",
    "marketplace-service-mock": "mps-api",
    "aaa-service-mock": "aaa-api",
    "ead-validation-service": "eadvs-api",
    "workbench-client": "wbc",
    "workbench-client-v2": "wbc-v2",
    "workbench-client-v2-sample-ui": "sample-app-ui",
}
