import click
import yaml
import os
import slai
import sys

from pathlib import Path
from slai_cli import log
from slai_cli.exceptions import InvalidApiKey
# from slai.modules.runtime import ValidRuntimes


def get_credentials(
    profile_name="default",
    #runtime=ValidRuntimes.Project,
    client_id=None,
    client_secret=None,
):

    if client_id is None or client_secret is None:
        client_id = click.prompt("Client ID", type=str, default=client_id)
        client_secret = click.prompt("Client Secret", type=str, default=client_secret)

    try:
        store_credentials(
            profile_name=profile_name,
            client_id=client_id,
            client_secret=client_secret
        )
    except InvalidApiKey:
        log.warn("Invalid credentials.")
        return

    log.action("Credentials configured.")


def store_credentials(*, profile_name, client_id, client_secret):
    new_profile = {
        "client_id": client_id,
        "client_secret": client_secret,
    }

    try:
        slai.login(client_id=client_id, client_secret=client_secret, key_type="USER")
    except slai.exceptions.InvalidCredentials:
        log.warn("Invalid credentials")
        sys.exit(1)

    credentials_path = f"{Path.home()}/.slai"
    if not os.path.exists(credentials_path):
        os.makedirs(credentials_path)

    try:
        with open(f"{credentials_path}/credentials.yml", "r") as f_in:
            try:
                credentials = yaml.safe_load(f_in)
            except yaml.YAMLError:
                pass
    except:
        credentials = {}

    # save new profile
    if credentials.get("default") is None:
        credentials["default"] = new_profile

    credentials[profile_name] = new_profile

    noalias_dumper = yaml.dumper.SafeDumper
    noalias_dumper.ignore_aliases = lambda self, data: True

    with open(f"{credentials_path}/credentials.yml", "w") as f_out:
        yaml.dump(credentials, f_out, default_flow_style=False, Dumper=noalias_dumper)
