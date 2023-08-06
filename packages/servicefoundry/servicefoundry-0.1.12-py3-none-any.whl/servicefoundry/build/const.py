import os
from pathlib import Path

if "SERVICE_FOUNDRY_SERVER" not in os.environ:
    SERVICE_FOUNDRY_SERVER = (
        "https://sf-server.tfy-ctl-us-east-1-develop.develop.truefoundry.io"
    )
    # SERVICE_FOUNDRY_SERVER = (
    #     "http://localhost:3000"
    # )
else:
    SERVICE_FOUNDRY_SERVER = os.environ["SERVICE_FOUNDRY_SERVER"]

# Auth related config
# @TODO Call service foundry to get this.
DEFAULT_TENANT_ID = "895253af-ec9d-4be6-83d1-6f248e644e79"
AUTH_UI = "https://app.develop.truefoundry.io"
AUTH_SERVER = "https://auth-server.tfy-ctl-us-east-1-develop.develop.truefoundry.io"
# AUTH_SERVER = "http://localhost:3000"
SESSION_FILE = f"{str(Path.home())}/.truefoundry"


# Build related Config
SERVICE_DEF_FILE_NAME = "servicefoundry.yaml"

ADDITIONAL_PACKAGES = "additional_packages"
COMMAND = "command"
SERVICE_TYPE_MAPPING = {
    "fast_api_build": {
        ADDITIONAL_PACKAGES: ["uvicorn"],
        COMMAND: lambda service, port: f"uvicorn {service}:app --host 0.0.0.0 --port {port}"
    },
    "streamlit_build": {
        ADDITIONAL_PACKAGES: [],
        COMMAND:
            lambda service, port:
            f"streamlit run {service} --server.address 0.0.0.0 --server.port {port }"
    }
}

# Polling during login redirect
MAX_POLLING_RETRY = 100
POLLING_SLEEP_TIME_IN_SEC = 4

# Refresh access token cutoff
REFRESH_ACCESS_TOKEN_IN_MIN = 10 * 60
