import json
from servicefoundry.build.const import SESSION_FILE


class ServiceFoundrySession:
    def __init__(
        self,
        client_id,
        access_token,
        refresh_token,
        session_file_location=SESSION_FILE,
        refresher=None,
    ):
        self.client_id = client_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.session_file_location = session_file_location
        self.refresher = refresher

    def save_session(self):
        with open(self.session_file_location, "w") as file:
            json.dump(
                {
                    "client_id": self.client_id,
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                },
                file,
            )

    def refresh_access_token(self):
        self.access_token, self.refresh_token = self.refresher(self)
        self.save_session()
