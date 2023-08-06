import click
import glob
import os

from typing import List

from .connection.serial import get_connected_hubs, SerialConnection


DIRNAME = os.path.dirname(__file__)


def check_connected_hubs() -> List[str]:
    hubs = get_connected_hubs()
    if not hubs:
        raise click.ClickException("No LEGO hub found. Make sure a hub is connected and powered on.")
    return [f"{hub.device}: {hub.description}" for hub in hubs]


@click.group()
def robrick():
    pass


@robrick.command()
def hello():
    hub = get_connected_hubs()[0]
    conn = SerialConnection(hub.device)
    conn.send_message("scratch.display_text", {"text": "hi"})


@robrick.command()
def install():
    hubs = check_connected_hubs()
    spaceship_dir = os.path.join(DIRNAME, "spaceship")

    click.echo("Copy robrick's spaceship to the selected hub...")
    hub = click.prompt(
        "Chose hub to update...",
        type=click.Choice(hubs, case_sensitive=False),
        default=hubs[0],
    )

    for pyfile in glob.glob("*.py", root_dir=spaceship_dir):
        click.echo(f"Copy {pyfile} to {hub}")
        os.system(f"python -m mpy_cross {os.path.join(spaceship_dir, pyfile)}")


@robrick.command()
def hubs():
    check_connected_hubs()
    click.echo("Conected hubs...")
    for hub in get_connected_hubs():
        click.echo(f"{hub.device}: {hub.description}")


@robrick.command()
def ls():
    check_connected_hubs()
    click.echo("Conected hubs...")
    for hub in get_connected_hubs():
        click.echo(f"{hub.device}: {hub.description}")
