import click
import sys
import os
import yaml
from functools import update_wrapper
from packaging import version as ver
from requests.exceptions import HTTPError

from slai.clients.cli import get_cli_client
from slai_cli import log
from slai_cli.cli import SlaiClient
from slai_cli.profile import commands as profile
from slai_cli.decorators import requires_slai_credentials
from slai_cli.errors import handle_error
from slai_cli import get_version, version, bundle

from slai.modules.runtime import detect_credentials
from slai.exceptions import NoCredentialsFound


def project_yaml():
    filepath = os.path.join(os.getcwd(), "slai.yml")
    if not os.path.exists(filepath):
        click.echo(
            click.style("ERROR: could not find slai.yaml. Are you in your project root?", fg="red")
        )
        sys.exit(1)
    else:
        return yaml.safe_load(open(filepath))


def with_profile(f):
    @click.pass_context
    def run(ctx, *args, **kwargs):

        if ctx.invoked_subcommand != "profile":
            _f = requires_slai_credentials(f, **kwargs)
            return ctx.invoke(_f, *args, **kwargs)

    return update_wrapper(run, f)


@click.group()
@click.option("--profile", required=False, default="default", help="Profile to use")
@with_profile
def entry_point(profile):
    cli_client = get_cli_client()
    cli_requirements = cli_client.get_cli_version()

    minimum_required_cli_version = ver.parse(cli_requirements["minimum_required_version"])
    current_cli_version = ver.parse(get_version())
    if current_cli_version < minimum_required_cli_version:
        log.info(f"Current CLI version: {current_cli_version}")
        log.info(f"Minimum required CLI version: {minimum_required_cli_version}")
        log.warn(
            "This version of the CLI is out of date, please update with: `pipx upgrade slai-cli` to continue."  # noqa
        )
        sys.exit(1)


@click.command()
@click.argument("sandbox_url", required=False)
@click.option("--profile", default="default", help="Profile to use")
def sync(sandbox_url, profile=None):
    try:
        credentials = detect_credentials()
    except NoCredentialsFound:
        log.warn("Invalid credentials.")
        return
    current_directory = os.getcwd()
    if not sandbox_url:
        config = project_yaml()
        sandbox_url = config["sandbox_url"]

    sandbox_id = sandbox_url.split("/")[-1]
    base_url = sandbox_url.split("/sandbox/")[0]
    cli_client = SlaiClient(**credentials, base_url=base_url)
    cli_client.sync_sandbox(current_directory, sandbox_id)


def main():
    entry_point.add_command(sync)
    # entry_point.add_command(model.model)
    entry_point.add_command(profile.profile)
    entry_point.add_command(version)
    #    entry_point.add_command(bundle)

    try:
        entry_point()
    except HTTPError as e:
        print(e)
        handle_error(error_msg="unknown_http_error")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
