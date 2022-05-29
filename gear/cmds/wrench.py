from cmath import log
import sys
import logging
import shutil

import click
import luigi
from powerstrip import PluginManager

from gear.utils.config import CONFIG_DIRECTORY, OUTPUT_DIR, PLUGIN_DIR
from gear.evaluator.evaluatorconfigmanager import EvaluatorConfigManager
from gear.utils.utils import guess_filename, get_user
from gear.utils.config import CONFIG_DIRECTORY
from gear.utils.directorymanager import DirectoryManager
from gear.tasks.starttask import StartTask

# add plugin directory to path
sys.path.append(PLUGIN_DIR)

# set logging level
logging.basicConfig(level=logging.WARNING)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    if debug is True:
        # enable DEBUG log level
        logging.basicConfig(level=logging.DEBUG)


@cli.group()
def config():
    """
    config subcommand
    """
    pass


@config.command()
@click.option("--full/--no-full", default=False)
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


@config.command()
@click.argument("name")
def view(name: str):
    """
    view config

    :param name: name of the config file
    :type name: str
    :raises click.ClickException: raised, if config file is not found
    """

    try:
        # ensure that filename is a Path
        fn = guess_filename(name, CONFIG_DIRECTORY, ".yml")

        ec = EvaluatorConfigManager.load_config(fn)
        print(ec.yaml)

    except FileNotFoundError as e:
        raise click.ClickException(e)


@config.command()
@click.argument(
    "name",
)
@click.option(
    "--description",
    help="description of the configuration"
)
@click.option(
    "--author",
    default=get_user(),
    show_default=True,
    help="name of the author of the configuration"
)
def create(name: str, description: str, author: str):
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
@click.argument("configname")
def run(configname):
    try:
        # ensure that filename is a Path
        fn = guess_filename(configname, CONFIG_DIRECTORY, ".yml")

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
@click.argument("configname")
def reset(configname: str):
    """
    reset the output directory

    :param configname: configuration name
    :type configname: str
    :raises click.ClickException: raised, if config does not exist
    """
    try:
        # ensure that filename is a Path
        fn = guess_filename(configname, CONFIG_DIRECTORY, ".yml")

        directory_manager = DirectoryManager(OUTPUT_DIR, configname)
        if directory_manager.temp_directory.exists():
            # remove the output directory
            click.echo(f"removing '{directory_manager.temp_directory}'...")
            shutil.rmtree(directory_manager.temp_directory)

    except FileNotFoundError as e:
        raise click.ClickException(e)



@cli.group()
def plugin():
    """
    plugin subcommand
    """
    pass

@plugin.command()
@click.argument("directory")
def pack(directory):
    pm = PluginManager(PLUGIN_DIR, use_category=True)
    pm.pack(directory)


@plugin.command()
@click.argument("package")
def install(package):
    pm = PluginManager(PLUGIN_DIR, use_category=True)
    pm.install(package)
