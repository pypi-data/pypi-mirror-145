import requests

from requests.auth import HTTPBasicAuth
from importlib import import_module

import os
from slai.config import get_api_base_urls
from slai.modules.parameters import from_config
from slai.modules.runtime import detect_credentials

import slai_cli.syncer
from slai_cli.syncer import SandboxSyncer
import importlib

REQUESTS_TIMEOUT = 15


class SlaiClient:
    BACKEND_BASE_URL, _ = get_api_base_urls()

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        user_agent_header="Slai CLI 0.2.0",
        profile_name="default",
        base_url=BACKEND_BASE_URL,
    ):

        if client_id is None or client_secret is None:
            credentials = detect_credentials(profile_name=profile_name)
            self.client_id = credentials["client_id"]
            self.client_secret = credentials["client_secret"]
        else:
            self.client_id = client_id
            self.client_secret = client_secret

        self.user_agent_header = user_agent_header
        self.base_url = base_url

    def _post(self, url, body):
        res = requests.post(
            f"{self.BACKEND_BASE_URL}/{url}",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                "User-Agent": self.user_agent_header,
            },
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def retrieve_model(self, *, name, org_name):
        body = {"action": "retrieve", "name": name, "org_name": org_name}
        body = {k: v for k, v in body.items() if v is not None}
        return self._post("cli/model", body)

    def create_model_version(self, *, model_id, name):
        body = {"action": "create", "model_id": model_id, "name": name}
        return self._post("cli/model-version", body)

    def retrieve_model_version_by_name(self, *, model_id, model_version_name):
        body = {
            "action": "retrieve",
            "model_id": model_id,
            "model_version_name": model_version_name,
        }
        return self._post("cli/model-version", body)

    def retrieve_model_version_by_id(self, *, model_version_id):
        body = {
            "action": "retrieve",
            "model_version_id": model_version_id,
        }
        return self._post("cli/model_version", body)

    def list_model_versions(self, *, model_id):
        body = {"action": "list", "model_id": model_id}
        return self._post("cli/model_version", body)

    def list_model_artifacts(self, *, model_version_id):
        body = {
            "action": "list",
            "model_version_id": model_version_id,
        }
        return self._post("cli/model-artifact", body)

    def retrieve_model_artifact(self, *, model_version_id, model_artifact_id):
        body = {
            "action": "retrieve",
            "model_version_id": model_version_id,
            "model_artifact_id": model_artifact_id,
        }

        body = {k: v for k, v in body.items() if v is not None}

        return self._post("cli/model-artifact", body)

    def get_user(self):
        body = {"action": "retrieve"}

        return self._post("cli/user", body)

    def update_user(self, email=None, gauth_creds=None):
        body = {"action": "update", "email": email, "gauth_creds": gauth_creds}

        body = {k: v for k, v in body.items() if v is not None}
        return self._post("cli/user", body)

    def get_cli_version(self):
        return self._post("cli/cli-version", {})

    def get_sandboxes(self):
        body = {"action": "list"}
        return self._post("sandbox/sandbox", body)

    def fork_sandbox(self):
        return self._post("sandbox/fork_sandbox", {"action": None})

    def get_sandbox(self, id):
        body = {"action": "retrieve", "sandbox_id": id}
        return self._post("sandbox/sandbox", body)

    def get_sandbox_summary(self, id):
        body = {"action": "retrieve", "sandbox_id": id, "summarize": True}
        return self._post("sandbox/sandbox", body)

    def update_sandbox_file(self, sandbox_id, path, contents):
        body = {"action": "update", "sandbox_id": sandbox_id, "path": path, "contents": contents}
        return self._post("sandbox/sandbox_file", body)

    def create_sandbox_file(self, sandbox_id, path, contents):
        body = {"action": "create", "sandbox_id": sandbox_id, "path": path, "contents": contents}
        return self._post("sandbox/sandbox_file", body)

    def delete_sandbox_file(self, sandbox_id, path):
        body = {"action": "delete", "sandbox_id": sandbox_id, "path": path}
        return self._post("sandbox/sandbox_file", body)

    def sync_sandbox(self, path, sandbox_id=None, sandbox=None, sandbox_url=None):
        if not sandbox:
            if not sandbox_id and sandbox_url:
                sandbox_id = sandbox_url.split("/")[-1]
            sandbox = self.get_sandbox(sandbox_id)

        syncer = SandboxSyncer(self, sandbox, path)
        syncer.start()


if __name__ == "__main__":
    slai = SlaiClient(profile_name="local")
    print("\nSLAI REPL")
    email = slai.get_user()["identity_user"]["email"]
    version = slai.get_cli_version()["latest_version"]
    print(f"Latest SDK Version:  {version}")
    print(f"User:                {email}")
    print(f"API Server:          {slai.BACKEND_BASE_URL}\n")
    print("Try `slai.get_cli_version()`\n")
