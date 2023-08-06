import click
import glob
import os

from serial.tools.list_ports_common import ListPortInfo
from there.repl_connection import MicroPythonRepl

from .connect.serial import get_connected_hubs, SerialConnection
from .helpers import get_slots


DIRNAME = os.path.dirname(__file__)
HUB_PROJECTS_DIR = "/projects"
robrick_DIR = os.path.join(HUB_PROJECTS_DIR, "robrick")


def get_hub() -> ListPortInfo:
    hubs = get_connected_hubs()

    if not hubs:
        raise click.ClickException(
            "No LEGO hub found. Make sure a hub is connected and powered on."
        )

    if len(hubs) > 1:
        raise click.ClickException(
            "Currently robrick can only manage one LEGO hub at a time. Please disconnect all but one."
        )

    return hubs[0]


@click.group()
def robrick():
    pass


@robrick.command()
def hello():
    hub = get_connected_hubs()[0]
    conn = SerialConnection(hub.device)
    click.echo(conn.send_message("scratch.display_text", {"text": "hi"}))


@robrick.command()
def install():
    """Install robrick Toolkit on the LEGO hub.
    The files are compiled for MicroPython and moved to the hub inside the `projects` folder.
    The toolkit can be then accessed like this in your projects:

    ```
    import robrick

    robrick.light.image_99(51)
    ```
    """

    hub = get_hub()
    toolkit_dir = os.path.join(DIRNAME, "toolkit")

    for pyfile in glob.glob("*.py", root_dir=toolkit_dir):
        os.system(f"python -m mpy_cross {os.path.join(toolkit_dir, pyfile)}")

    try:
        os.system(f"python -m there -p {hub.device} mkdir {robrick_DIR}")
        os.system(f"python -m there -p {hub.device} push {toolkit_dir}/*.mpy {robrick_DIR}")
    except Exception as e:
        raise click.ClickException(f"Could not install robrick files: {e}")


@robrick.command()
def uninstall():
    """Remove all robrick files from the LEGO hub, including user's workshop files."""

    hub = get_hub()
    click.confirm(
        "This will remove all robrick files from the hub. Are you sure?", abort=True
    )
    os.system(f"python -m there -p {hub.device} rm -r {robrick_DIR}")


@robrick.command()
def hub():
    """Show LEGO hub information."""

    hub = get_hub()
    repl = MicroPythonRepl(hub.device)

    try:
        repl.exec("import robrick;")
        robrick_version = None
        robrick_is_installed = True
    except ImportError:
        robrick_version = None
        robrick_is_installed = False

    py_version = repl.exec("import sys; print(sys.version);").strip()
    mpy_version = repl.exec("import os; print(os.uname());").strip()

    click.secho(f"🚀 {hub.description}", fg="green")
    click.echo(f"Port: {hub.device}")
    click.echo(f"Manufacturer: {hub.manufacturer}")
    click.echo(f"Serial number: {hub.serial_number}")
    click.echo(f"Python version: {py_version}")
    click.echo(f"MicroPython version: {mpy_version}")
    click.echo(f"Hub OS version: {hub.serial_number}")

    if robrick_is_installed:
        click.echo(f"robrick version: {robrick_version}")
    else:
        click.secho("robrick is not present. Don't forget to `robrick install`.", fg="blue")


@robrick.command()
def ls():
    """List all projects currently in the LEGO hub."""

    hub = get_hub()
    repl = MicroPythonRepl(hub.device)
    slots = get_slots(repl.read_from_file(f"{HUB_PROJECTS_DIR}/.slots"))

    for slot in slots:
        click.echo(f"[{'%02d' % slot.number}] {slot.id} - {slot.name}")
