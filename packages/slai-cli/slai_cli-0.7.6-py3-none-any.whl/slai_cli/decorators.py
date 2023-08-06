import click
import sys

from pathlib import Path
from slai_cli import log
from slai_cli.profile.configure import get_credentials
from slai.modules.runtime import detect_credentials
from slai.exceptions import NoCredentialsFound
from os import path

def requires_slai_credentials(callback, *outer_args, **outer_kwargs):
    def wrapper(*args, **kwargs):
        profile_name = outer_kwargs.get("profile", "default")

        try:
            detect_credentials(profile_name=profile_name)
        except NoCredentialsFound:
            log.warn("No credentials detected.")

            try:
                has_api_key = click.confirm("Do you have an api key?")
                if has_api_key:
                    get_credentials(profile_name=profile_name)
                else:
                    log.action("Create one at slai.io, then re-run this command.")
                    click.launch("https://slai.io")
                    sys.exit(0)
                    return

            except click.exceptions.Abort:
                log.warn("Aborted.")
                return

        return callback(*args, **kwargs)

    return wrapper
