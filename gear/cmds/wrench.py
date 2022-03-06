import getpass
import socket

import click

from gear.utils.config import CONFIG_DIRECTORY
from gear.evaluator.evaluatorconfigmanager import EvaluatorConfigManager
from gear.utils.utils import ensure_path, guess_filename
from gear.utils.config import CONFIG_DIRECTORY


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.argument(
    "name",
)
@click.option(
    "--description",
    help="description of the configuration"
)
@click.option(
    "--author",
    default=(
        f"{getpass.getuser()} <{getpass.getuser()}@{socket.gethostname()}>"
    ),
    show_default=True,
    help="name of the author of the configuration"
)
def create_config(name: str, description: str, author: str):
    """
    create a new configuration file

    :param name: name of the configuration
    :type name: str
    :param description: description of configuration
    :type description: str
    :param author: author of the configuration
    :type author: str
    """
    if not description:
        # add default description, if not provided
        description = f"Configuration '{name}'."

    click.echo("creating config...")
    ecm = EvaluatorConfigManager(CONFIG_DIRECTORY)
    try:
        fn = ecm.create_config(
            name=name,
            description=description,
            author=author
        )
        click.echo(f"created config '{fn}'.")

    except FileExistsError as e:
        raise click.ClickException(e)


@cli.command()
def test():
    print("DA")
    from gear.utils.utils import get_classes
    from gear.filetypes.basefiletype import BaseFileType

    print(get_classes("gear/filetypes", BaseFileType))


@cli.command()
@click.argument("name")
def run(name):
    try:
        # ensure that filename is a Path
        fn = guess_filename(name, CONFIG_DIRECTORY, ".yml")

        ecm = EvaluatorConfigManager(CONFIG_DIRECTORY)
        ec = ecm.load_config(fn)
        print(ec)

    except FileNotFoundError as e:
        raise click.ClickException(e)

