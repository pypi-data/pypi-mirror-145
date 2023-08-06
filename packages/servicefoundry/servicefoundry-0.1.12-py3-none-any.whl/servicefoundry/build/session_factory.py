import os
import json
from .const import SESSION_FILE, DEFAULT_TENANT_ID

from servicefoundry.build.model.session import ServiceFoundrySession
from servicefoundry.build.clients.auth_service_client import AuthServiceClient
from .util import BadRequestException


def get_session(session_file=SESSION_FILE):
    if os.getenv("SERVICE_FOUNDRY_API_KEY"):
        auth_client = AuthServiceClient()
        return auth_client.login_with_api_token(
            DEFAULT_TENANT_ID, os.getenv("SERVICE_FOUNDRY_API_KEY")
        )

    if os.path.isfile(session_file):
        with open(session_file, "r") as file:
            data = json.load(file)
            return ServiceFoundrySession(
                **data, refresher=AuthServiceClient().refresh_token
            )
    else:
        raise BadRequestException(403, f"Please loging before running this command.")