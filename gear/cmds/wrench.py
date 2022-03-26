from cmath import log
import sys
import getpass
import socket
import logging

import click
import luigi
from powerstrip import PluginManager

from gear.utils.config import CONFIG_DIRECTORY, PLUGIN_DIR
from gear.evaluator.evaluatorconfigmanager import EvaluatorConfigManager
from gear.utils.utils import ensure_path, guess_filename
from gear.utils.config import CONFIG_DIRECTORY
from gear.utils.utils import get_classes
from gear.tasks.starttask import StartTask

# add plugin directory to path
sys.path.append(PLUGIN_DIR)

# set logging level
logging.basicConfig(level=logging.WARNING)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    pass
    #click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.option('--full/--no-full', default=False)
def list(full):
    """
    list all existing configurations
    """
    ecm = EvaluatorConfigManager(CONFIG_DIRECTORY)
    for conf in ecm.configurations:
        if full is True:
            # show full path
            click.echo(conf)
        else:
            # show only filename without full path
            click.echo(conf.name)


@cli.command()
@click.argument("name")
def view(name):
    try:
        # ensure that filename is a Path
        fn = guess_filename(name, CONFIG_DIRECTORY, ".yml")

        ec = EvaluatorConfigManager.load_config(fn)
        print(ec.yaml)

    except FileNotFoundError as e:
        raise click.ClickException(e)


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
@click.argument("name")
def run(name):
    try:
        # ensure that filename is a Path
        fn = guess_filename(name, CONFIG_DIRECTORY, ".yml")

        src_directory = "."

        # start task
        luigi.build(
            [StartTask(config_filename=fn, src_directory=src_directory)],
            workers=1,
            local_scheduler=True,
            log_level=logging.getLevelName(logging.INFO)
        )

    except FileNotFoundError as e:
        raise click.ClickException(e)


@cli.command()
@click.argument("directory")
def pack(directory):
    pm = PluginManager(PLUGIN_DIR, use_category=True)
    pm.pack(directory)


@cli.command()
@click.argument("package")
def install(package):
    pm = PluginManager(PLUGIN_DIR, use_category=True)
    pm.install(package)
