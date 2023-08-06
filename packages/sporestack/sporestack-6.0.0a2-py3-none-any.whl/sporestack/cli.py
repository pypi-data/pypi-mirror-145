"""
SporeStack CLI: `sporestack`
"""

import importlib.util
import json
import logging
import os
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, Dict, Optional

if sys.version_info[:2] >= (3, 8):  # pragma: nocover
    from importlib.metadata import version as importlib_metadata_version
else:  # pragma: nocover
    # Python 3.7 doesn't have this.
    from importlib_metadata import version as importlib_metadata_version

import typer


def lazy_import(name: str) -> ModuleType:
    """
    Lazily import a module. Helps speed up CLI performance.
    """
    spec = importlib.util.find_spec(name)
    assert spec is not None
    assert spec.loader is not None
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


# For mypy
if TYPE_CHECKING:
    from . import api_client
else:
    api_client = lazy_import("sporestack.api_client")

HELP = """
SporeStack Python CLI

Optional environment variables:
SPORESTACK_ENDPOINT
*or*
SPORESTACK_USE_TOR_ENDPOINT

TOR_PROXY (defaults to socks5h://127.0.0.1:9050 which is fine for most)
"""

_home = os.getenv("HOME", None)
assert _home is not None, "Unable to detect $HOME environment variable?"
HOME = Path(_home)

SPORESTACK_DIR = HOME / ".sporestack"

# Try to protect files in ~/.sporestack
os.umask(0o0077)

cli = typer.Typer(help=HELP)

token_cli = typer.Typer()
HOME = Path(_home)
cli.add_typer(token_cli, name="token")
server_cli = typer.Typer()
cli.add_typer(server_cli, name="server")

logging.basicConfig(level=logging.INFO)

DEFAULT_TOKEN = "primary"
DEFAULT_FLAVOR = "vps-1vcpu-1gb"
# Users may have a different key file, but this is the most common.
DEFAULT_SSH_KEY_FILE = HOME / ".ssh" / "id_rsa.pub"

# On disk format
TOKEN_VERSION = 1

WAITING_PAYMENT_TO_PROCESS = "Waiting for payment to process..."


def get_api_endpoint() -> str:
    api_endpoint = os.getenv("SPORESTACK_ENDPOINT", api_client.CLEARNET_ENDPOINT)
    if os.getenv("SPORESTACK_USE_TOR_ENDPOINT", None) is not None:
        api_endpoint = api_client.TOR_ENDPOINT
    return api_endpoint


def make_payment(currency: str, uri: str, usd: str) -> None:
    import segno

    premessage = """Payment URI: {}
Pay *exactly* the specified amount. No more, no less. Pay within
one hour at the very most.
Resize your terminal and try again if QR code above is not readable.
Press ctrl+c to abort."""
    message = premessage.format(uri)
    qr = segno.make(uri)
    # This typer.echos.
    qr.terminal()
    typer.echo(message)
    typer.echo(f"Approximate price in USD: {usd}")
    input("[Press enter once you have made payment.]")


@server_cli.command()
def launch(
    hostname: str,
    days: int = typer.Option(...),
    operating_system: str = typer.Option(...),
    ssh_key_file: Path = DEFAULT_SSH_KEY_FILE,
    flavor: str = DEFAULT_FLAVOR,
    token: str = DEFAULT_TOKEN,
    region: Optional[str] = None,
    quote: bool = typer.Option(True, help="Require manual price confirmation."),
) -> None:
    """
    Launch a server on SporeStack.
    """

    from . import utils

    typer.echo(f"Launching server with token {token}...", err=True)
    _token = load_token(token)

    if machine_exists(hostname):
        typer.echo(f"{hostname} already created.")
        raise typer.Exit(code=1)

    typer.echo(f"Loading SSH key from {ssh_key_file}...")
    if not ssh_key_file.exists():
        msg = f"{ssh_key_file} does not exist. "
        msg += "You can try generating a key file with `ssh-keygen`"
        typer.echo(msg, err=True)
        raise typer.Exit(code=1)

    ssh_key = ssh_key_file.read_text()

    machine_id = utils.random_machine_id()

    if quote:
        response = api_client.launch(
            machine_id=machine_id,
            days=days,
            flavor=flavor,
            operating_system=operating_system,
            ssh_key=ssh_key,
            currency="settlement",
            region=region,
            token=_token,
            api_endpoint=get_api_endpoint(),
            retry=True,
            quote=True,
        )

        msg = f"Is {response.payment.usd} for {days} day(s) of {flavor} okay?"
        typer.echo(msg, err=True)
        input("[Press ctrl+c to cancel, or enter to accept.]")

    tries = 360
    while tries > 0:
        response = api_client.launch(
            machine_id=machine_id,
            days=days,
            flavor=flavor,
            operating_system=operating_system,
            ssh_key=ssh_key,
            currency="settlement",
            region=region,
            token=_token,
            api_endpoint=get_api_endpoint(),
            retry=True,
        )
        if response.created is True:
            break
        typer.echo("Waiting for server to build...", err=True)
        tries = tries + 1
        # Waiting for server to spin up.
        time.sleep(10)

    if response.created is False:
        typer.echo("Server creation failed, tries exceeded.", err=True)
        raise typer.Exit(code=1)

    created_dict = response.dict()
    created_dict["vm_hostname"] = hostname
    save_machine_info(created_dict)
    typer.echo(pretty_machine_info(created_dict), err=True)
    typer.echo(json.dumps(created_dict, indent=4))


@server_cli.command()
def topup(
    hostname: str,
    days: int = typer.Option(...),
    token: str = DEFAULT_TOKEN,
    quote: bool = typer.Option(True, help="Require manual price confirmation."),
) -> None:
    """
    Extend an existing SporeStack server's lifetime.
    """

    if not machine_exists(hostname):
        typer.echo(f"{hostname} does not exist.")
        raise typer.Exit(code=1)

    _token = load_token(token)

    machine_info = get_machine_info(hostname)
    machine_id = machine_info["machine_id"]

    if quote:
        response = api_client.topup(
            machine_id=machine_id,
            days=days,
            currency="settlement",
            api_endpoint=get_api_endpoint(),
            token=_token,
            retry=True,
            quote=True,
        )

        typer.echo(f"Is {response.payment.usd} for {days} day(s) okay?", err=True)
        input("[Press ctrl+c to cancel, or enter to accept.]")

    response = api_client.topup(
        machine_id=machine_id,
        days=days,
        currency="settlement",
        api_endpoint=get_api_endpoint(),
        token=_token,
        retry=True,
    )
    assert response.payment.paid is True

    machine_info["expiration"] = response.expiration
    save_machine_info(machine_info, overwrite=True)
    typer.echo(machine_info["expiration"])


def server_info_path() -> Path:
    # Put servers in a subdirectory
    servers_dir = SPORESTACK_DIR / "servers"

    # Migrate existing server.json files into servers subdirectory
    if SPORESTACK_DIR.exists() and not servers_dir.exists():
        typer.echo(
            f"Migrating server profiles found in {SPORESTACK_DIR} to {servers_dir}.",
            err=True,
        )
        servers_dir.mkdir()
        for json_file in SPORESTACK_DIR.glob("*.json"):
            json_file.rename(servers_dir / json_file.name)

    # Make it, if it doesn't exist already.
    SPORESTACK_DIR.mkdir(exist_ok=True)
    servers_dir.mkdir(exist_ok=True)

    return servers_dir


def token_path() -> Path:
    token_dir = SPORESTACK_DIR / "tokens"

    # Make it, if it doesn't exist already.
    token_dir.mkdir(exist_ok=True, parents=True)

    return token_dir


def save_machine_info(machine_info: Dict[str, Any], overwrite: bool = False) -> None:
    """
    Save info to disk.
    """
    directory = server_info_path()
    hostname = machine_info["vm_hostname"]
    json_file = directory / f"{hostname}.json"
    if overwrite is False:
        assert json_file.exists() is False, f"{json_file} already exists."
    json_file.write_text(json.dumps(machine_info))


def get_machine_info(hostname: str) -> Dict[str, Any]:
    """
    Get info from disk.
    """
    directory = server_info_path()
    json_file = directory / f"{hostname}.json"
    if not json_file.exists():
        raise ValueError(f"{hostname} does not exist in {directory} as {json_file}")
    machine_info = json.loads(json_file.read_bytes())
    assert isinstance(machine_info, dict)
    if machine_info["vm_hostname"] != hostname:
        raise ValueError("hostname does not match filename.")
    return machine_info


def pretty_machine_info(info: Dict[str, Any]) -> str:
    msg = "Hostname: {}\n".format(info["vm_hostname"])
    msg += "Machine ID (keep this secret!): {}\n".format(info["machine_id"])
    if "ipv6" in info["network_interfaces"][0]:
        msg += "IPv6: {}\n".format(info["network_interfaces"][0]["ipv6"])
    if "ipv4" in info["network_interfaces"][0]:
        msg += "IPv4: {}\n".format(info["network_interfaces"][0]["ipv4"])
    expiration = info["expiration"]
    human_expiration = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(expiration))
    if "running" in info:
        msg += "Running: {}\n".format(info["running"])
    msg += f"Expiration: {expiration} ({human_expiration})\n"
    time_to_live = expiration - int(time.time())
    hours = time_to_live // 3600
    msg += f"Server will be deleted in {hours} hours."
    return msg


@server_cli.command(name="list")
def server_list() -> None:
    """
    List all locally known servers.
    """
    from .exceptions import SporeStackUserError

    directory = server_info_path()
    infos = []
    for hostname_json in os.listdir(directory):
        hostname = hostname_json.split(".")[0]
        saved_vm_info = get_machine_info(hostname)
        try:
            upstream_vm_info = api_client.info(
                machine_id=saved_vm_info["machine_id"],
            )
            saved_vm_info["expiration"] = upstream_vm_info.expiration
            saved_vm_info["running"] = upstream_vm_info.running
            infos.append(saved_vm_info)
        except SporeStackUserError as e:
            expiration = saved_vm_info["expiration"]
            human_expiration = time.strftime(
                "%Y-%m-%d %H:%M:%S %z", time.localtime(expiration)
            )
            msg = hostname
            msg += f" expired ({expiration} {human_expiration}): "
            msg += str(e)
            typer.echo(msg)

    for info in infos:
        typer.echo()
        typer.echo(pretty_machine_info(info))

    typer.echo()


def machine_exists(hostname: str) -> bool:
    """
    Check if the VM's JSON exists locally.
    """
    return server_info_path().joinpath(f"{hostname}.json").exists()


@server_cli.command()
def get_attribute(hostname: str, attribute: str) -> None:
    """
    Returns an attribute about the VM.
    """
    machine_info = get_machine_info(hostname)
    typer.echo(machine_info[attribute])


@server_cli.command()
def info(hostname: str) -> None:
    """
    Info on the VM
    """
    machine_info = get_machine_info(hostname)
    machine_id = machine_info["machine_id"]
    typer.echo(
        api_client.info(machine_id=machine_id, api_endpoint=get_api_endpoint()).json()
    )


@server_cli.command()
def start(hostname: str) -> None:
    """
    Boots the VM.
    """
    machine_info = get_machine_info(hostname)
    machine_id = machine_info["machine_id"]
    api_client.start(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo(f"{hostname} started.")


@server_cli.command()
def stop(hostname: str) -> None:
    """
    Immediately kills the VM.
    """
    machine_info = get_machine_info(hostname)
    machine_id = machine_info["machine_id"]
    api_client.stop(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo(f"{hostname} stopped.")


@server_cli.command()
def delete(hostname: str) -> None:
    """
    Deletes the VM before expiration (no refunds/credits)
    """
    machine_info = get_machine_info(hostname)
    machine_id = machine_info["machine_id"]
    api_client.delete(machine_id=machine_id, api_endpoint=get_api_endpoint())
    # Also remove the .json file
    server_info_path().joinpath(f"{hostname}.json").unlink()
    typer.echo(f"{hostname} was deleted.")


@server_cli.command()
def rebuild(hostname: str) -> None:
    """
    Rebuilds the VM with the operating system and SSH key given at launch time.

    Will take a couple minutes to complete after the request is made.
    """
    machine_info = get_machine_info(hostname)
    machine_id = machine_info["machine_id"]
    api_client.rebuild(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo(f"{hostname} rebuilding.")


def load_token(token: str) -> str:
    token_file = token_path().joinpath(f"{token}.json")
    if not token_file.exists():
        msg = f"Token '{token}' ({token_file}) does not exist. Create it with:\n"
        msg += f"sporestack token create {token} --dollars 20 --currency xmr\n"
        msg += "(Can do more than $20, or a different currency, like btc.)\n"
        msg += (
            "With the token credited, you can launch servers, renew existing ones, etc."
        )
        typer.echo(msg, err=True)
        raise typer.Exit(code=1)

    token_data = json.loads(token_file.read_text())
    assert token_data["version"] == 1
    assert isinstance(token_data["key"], str)
    return token_data["key"]


def save_token(token: str, key: str) -> None:
    token_file = token_path().joinpath(f"{token}.json")
    if token_file.exists():
        msg = f"Token '{token}' already exists in {token_file}. Aborting!"
        typer.echo(msg, err=True)
        raise typer.Exit(code=1)

    token_data = {"version": TOKEN_VERSION, "name": token, "key": key}
    token_file.write_text(json.dumps(token_data))


@token_cli.command(name="create")
def token_create(
    token: str = typer.Argument(DEFAULT_TOKEN),
    dollars: int = typer.Option(...),
    currency: str = typer.Option(...),
) -> None:
    """
    Enables a new settlement token.

    Dollars is starting balance.
    """
    from . import utils

    _token = utils.random_token()

    typer.echo(f"Generated key {_token} for use with token {token}", err=True)

    if Path(SPORESTACK_DIR / "tokens" / f"{token}.json").exists():
        typer.echo("Token already created! Did you mean to `topup`?", err=True)
        raise typer.Exit(1)

    response = api_client.token_enable(
        token=_token,
        dollars=dollars,
        currency=currency,
        api_endpoint=get_api_endpoint(),
        retry=True,
    )

    uri = response.payment.uri
    assert uri is not None
    usd = response.payment.usd

    make_payment(currency=currency, uri=uri, usd=usd)

    tries = 360 * 2
    while tries > 0:
        typer.echo(WAITING_PAYMENT_TO_PROCESS, err=True)
        tries = tries - 1
        # FIXME: Wait two hours in a smarter way.
        # Waiting for payment to set in.
        time.sleep(10)
        response = api_client.token_enable(
            token=_token,
            dollars=dollars,
            currency=currency,
            api_endpoint=get_api_endpoint(),
            retry=True,
        )
        if response.payment.paid is True:
            typer.echo(f"{token} has been enabled with ${dollars}.")
            typer.echo(f"{token}'s key is {_token}.")
            typer.echo("Save it, don't share it, and don't lose it!")
            save_token(token, _token)
            return
    raise ValueError(f"{token} did not get enabled in time.")


@token_cli.command(name="import")
def token_import(
    name: str = typer.Argument(DEFAULT_TOKEN),
    key: str = typer.Option(...),
) -> None:
    """
    Imports a token from a key.
    """
    save_token(name, key)


@token_cli.command(name="topup")
def token_topup(
    token: str = typer.Argument(DEFAULT_TOKEN),
    dollars: int = typer.Option(...),
    currency: str = typer.Option(...),
) -> None:
    """
    Adds balance to an existing settlement token.
    """
    token = load_token(token)

    response = api_client.token_add(
        token,
        dollars,
        currency=currency,
        api_endpoint=get_api_endpoint(),
        retry=True,
    )

    uri = response.payment.uri
    assert uri is not None
    usd = response.payment.usd

    make_payment(currency=currency, uri=uri, usd=usd)

    tries = 360 * 2
    while tries > 0:
        typer.echo(WAITING_PAYMENT_TO_PROCESS, err=True)
        tries = tries - 1
        # FIXME: Wait two hours in a smarter way.
        response = api_client.token_add(
            token,
            dollars,
            currency=currency,
            api_endpoint=get_api_endpoint(),
            retry=True,
        )
        # Waiting for payment to set in.
        time.sleep(10)
        if response.payment.paid is True:
            typer.echo(f"Added {dollars} dollars to {token}")
            return
    raise ValueError(f"{token} did not get enabled in time.")


@token_cli.command()
def balance(token: str = typer.Argument(DEFAULT_TOKEN)) -> None:
    """
    Gets balance for a settlement token.
    """
    _token = load_token(token)

    typer.echo(
        api_client.token_balance(token=_token, api_endpoint=get_api_endpoint()).usd
    )


@token_cli.command(name="list")
def token_list() -> None:
    """
    Gets balance for a settlement token.
    """
    token_dir = token_path()
    typer.echo(f"SporeStack tokens present in {token_dir}:", err=True)
    typer.echo("(Name): (Key)", err=True)
    for token_file in token_dir.glob("*.json"):
        token = token_file.stem
        key = load_token(token)
        typer.echo(f"{token}: {key}")


@cli.command()
def version() -> None:
    """
    Returns the installed version.
    """
    typer.echo(importlib_metadata_version(__package__))


@cli.command()
def api_endpoint() -> None:
    """
    Prints the selected API endpoint: Env var: SPORESTACK_ENDPOINT,
    or, SPORESTACK_USE_TOR=1
    """
    endpoint = get_api_endpoint()
    if ".onion" in endpoint:
        typer.echo(f"{endpoint} using {api_client._get_tor_proxy()}")
        return
    else:
        typer.echo(endpoint)
        return


if __name__ == "__main__":
    cli()
