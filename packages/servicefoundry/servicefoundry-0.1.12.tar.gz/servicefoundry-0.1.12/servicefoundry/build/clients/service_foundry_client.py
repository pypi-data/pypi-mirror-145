import jwt
import time
import os

import requests
import json
import logging
import socketio
import rich

from ..const import SERVICE_FOUNDRY_SERVER, REFRESH_ACCESS_TOKEN_IN_MIN
from ..model.session import ServiceFoundrySession
from ..session_factory import get_session
from ..util import upload_package_to_s3, request_handling

logger = logging.getLogger(__name__)


def _get_or_throw(definition, key, error_message):
    if key not in definition:
        raise RuntimeError(error_message)
    return definition[key]


class ServiceFoundryServiceClient:
    def __init__(self, session: ServiceFoundrySession, host=SERVICE_FOUNDRY_SERVER):
        self.host = host
        self.session = session

    @staticmethod
    def get_client():
        # Would be ok to prefer auth token from API instead of local session file
        session = get_session()
        if session:
            return ServiceFoundryServiceClient(session)

    def check_and_refresh_session(self):
        decoded = jwt.decode(
            self.session.access_token, options={"verify_signature": False}
        )
        expiry_second = decoded["exp"]
        if expiry_second - time.time() < REFRESH_ACCESS_TOKEN_IN_MIN:
            logger.info(
                f"Going to refresh the access token {expiry_second - time.time()}."
            )
            self.session.refresh_access_token()

    def _get_header(self):
        return {"Authorization": f"Bearer {self.session.access_token}"}

    def list_workspace(self):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/workspace"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def create_workspace(self, cluster_name, name):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/workspace"
        res = requests.post(
            url,
            data={"name": name, "clusterId": cluster_name},
            headers=self._get_header(),
        )
        return request_handling(res)

    def remove_workspace(self, workspace_id):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/workspace/{workspace_id}"
        res = requests.delete(url, headers=self._get_header())
        return request_handling(res)

    def get_workspace(self, name):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/workspace/{name}"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def list_service_by_workspace(self, workspace_id):
        self.check_and_refresh_session()
        url = f'{SERVICE_FOUNDRY_SERVER}/service/list-by-workSpace/{workspace_id}'
        res = requests.get(
            url, headers=self._get_header())
        return request_handling(res)

    def remove_service(self, service_id):
        self.check_and_refresh_session()
        url = f'{SERVICE_FOUNDRY_SERVER}/service/{service_id}'
        res = requests.delete(
            url, headers=self._get_header())
        return request_handling(res)

    def get_service(self, service_id):
        self.check_and_refresh_session()
        url = f'{SERVICE_FOUNDRY_SERVER}/service/{service_id}'
        res = requests.get(
            url, headers=self._get_header())
        return request_handling(res)

    def list_deployment(self, service_id):
        self.check_and_refresh_session()
        url = f'{SERVICE_FOUNDRY_SERVER}/deployment/service/{service_id}'
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def remove_deployment(self, deployment_id):
        self.check_and_refresh_session()
        url = f'{SERVICE_FOUNDRY_SERVER}/deployment/{deployment_id}'
        res = requests.delete(
            url, headers=self._get_header())
        return request_handling(res)

    def get_deployment(self, deployment_id):
        self.check_and_refresh_session()
        url = f'{SERVICE_FOUNDRY_SERVER}/deployment/{deployment_id}'
        res = requests.get(
            url, headers=self._get_header())
        return request_handling(res)

    def create_cluster(self, name, region, aws_account_id, cluster_name, ca_data, server_url):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/cluster"
        res = requests.post(
            url,
            data={
                "id": name,
                "region": region,
                "authData": {
                    "awsAccountID": aws_account_id,
                    "clusterName": cluster_name,
                    "caData": ca_data,
                    "serverURL": server_url
                },
            },
            headers=self._get_header(),
        )
        return request_handling(res)

    def list_cluster(self):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/cluster"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def remove_cluster(self, cluster_id):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/cluster/{cluster_id}"
        res = requests.delete(url, headers=self._get_header())
        return request_handling(res)

    def get_presigned_url(self, space_name, service_name, env):
        self.check_and_refresh_session()
        url = f"{SERVICE_FOUNDRY_SERVER}/deployment/generateUploadUrl"
        res = requests.post(
            url,
            data={"workSpaceId": space_name,
                  "serviceName": service_name, "stage": env},
            headers=self._get_header(),
        )
        return request_handling(res)

    def build_and_deploy(self, service_def, package_zip, env):
        self.check_and_refresh_session()
        service_def_dict = json.loads(service_def.get_json())
        deployments = _get_or_throw(
            service_def_dict, "deployments", "Deployments not declared for this service"
        )
        deployment = _get_or_throw(deployments, env, f"Invalid env: {env}")
        space = _get_or_throw(
            deployment,
            "namespace",
            "TrueFoundry Space not specified for this environment",
        )

        http_response = self.get_presigned_url(space, service_def.name, env)
        upload_package_to_s3(http_response, package_zip)

        url = f"{SERVICE_FOUNDRY_SERVER}/deployment"
        data = {
            "sfConfig": {
                "name": service_def.name,
                "build": service_def_dict["build"],
                "deployments": {env: deployment},
            },
            "s3Bucket": http_response["s3Bucket"],
            "s3Key": http_response["s3Key"]
        }

        deploy_response = requests.post(
            url, json=data, headers=self._get_header())
        return request_handling(deploy_response)

    def create_secret_group(self, name):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret-group/"
        res = requests.post(url, headers=self._get_header(), json={
            "name": name
        })
        return request_handling(res)

    def delete_secret_group(self, id):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret-group/{id}"
        res = requests.delete(url, headers=self._get_header())
        return request_handling(res)

    def get_secret_group(self, id):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret-group/{id}"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def create_secret(self, secret_group_id, key, value):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret/"
        res = requests.post(url, headers=self._get_header(), json={
            "secretGroupId": secret_group_id,
            "key": key,
            "value": value
        })
        return request_handling(res)

    def delete_secret(self, id):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret/{id}"
        res = requests.delete(url, headers=self._get_header())
        return request_handling(res)

    def get_secret(self, id):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret/{id}"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def get_secrets_in_group(self, secret_group_id):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret/list-by-secret-group/{secret_group_id}"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def get_secret_groups(self):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/secret-group/findAll"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def tail_logs(self, runId, callback=lambda log_line: rich.print(log_line, end="")):
        self.check_and_refresh_session()
        sio = socketio.Client()

        @sio.event
        def logs(data):
            try:
                log_line = json.loads(data)['body']['log']
                callback(log_line)

                if log_line.startswith(f'PIPELINE_RUN_{runId}_ENDED'):
                    sio.disconnect()
            except:
                pass

        sio.connect(SERVICE_FOUNDRY_SERVER)
        sio.emit('logs', json.dumps({"runId": runId, "startTs": "0"}))

    def fetch_logs(self, runId):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/logs/runs/{runId}?startTs=0&endTs=5000000000&limit=1000&direction=asc"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def get_authorization_for_resource(self, resource_type, resource_id):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/authorize/{resource_type}/{resource_id}"
        res = requests.get(url, headers=self._get_header())
        return request_handling(res)

    def create_authorization(self, resource_id, resource_type, user_id, role):
        # @TODO instead of user_id pass emailID. Need to be done once API is available on auth.
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/authorize"
        res = requests.post(url, headers=self._get_header(), json={
            "resourceId": resource_id,
            "resourceType": resource_type,
            "userId": user_id,
            "userType": "USER",
            "role": role
        })
        return request_handling(res)

    def delete_authorization(self, id):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/authorize/{id}"
        res = requests.delete(url, headers=self._get_header())
        return request_handling(res)

    def update_authorization(self, id, role):
        self.check_and_refresh_session()

        url = f"{SERVICE_FOUNDRY_SERVER}/authorize"
        res = requests.patch(url, headers=self._get_header(), json={
            "id": id,
            "role": role
        })
        return request_handling(res)
