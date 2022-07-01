from cmath import log
import sys
import logging
import shutil

import click
import luigi

from gear.utils.config import CONFIG_DIR, OUTPUT_DIR, PLUGIN_DIR
from gear.evaluator.evaluatorconfigmanager import EvaluatorConfigManager
from gear.utils.utils import guess_filename, get_user
from gear.utils.directorymanager import DirectoryManager
from gear.tasks.starttask import StartTask

# add plugin directory to path
sys.path.append(PLUGIN_DIR)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    if debug is True:
        # enable DEBUG log level
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


# add subcommands
from gear.cmds.subcommands.config import config
from gear.cmds.subcommands.plugin import plugin
cli.add_command(config)
cli.add_command(plugin)


@cli.command()
@click.argument("configname")
@click.option(
    "--local/--no-local", default=True, show_default=True,
    help="use local scheduler"
)
@click.option(
    "--workers", default=1, show_default=True,
    help="number of workers"
)
def run(configname, local, workers):
    """
    run given analysis
    """
    try:
        # ensure that filename is a Path
        fn = guess_filename(
            name=configname,
            directories=CONFIG_DIR.joinpath(configname),
            default_extension=".yml"
        )

        # start task
        luigi.build(
            [StartTask(config_filename=fn, src_directory=".")],
            workers=workers,
            local_scheduler=local,
            log_level=logging.getLevelName(logging.INFO)
        )

    except FileNotFoundError as e:
        raise click.ClickException(e)


@cli.command()
@click.argument("configname")
def reset(configname: str):
    """
    reset the analysis' output directory

    :param configname: configuration name
    :type configname: str
    :raises click.ClickException: raised, if config does not exist
    """
    try:
        # ensure that filename is a Path
        _ = guess_filename(
            name=configname,
            directories=CONFIG_DIR.joinpath(configname),
            default_extension=".yml"
        )

        directory_manager = DirectoryManager(
            output_directory=OUTPUT_DIR,
            config_directory=CONFIG_DIR,
            config_name=configname
        )
        if directory_manager.temp_directory.exists():
            # remove the output directory
            click.echo(f"removing '{directory_manager.temp_directory}'...")
            shutil.rmtree(directory_manager.temp_directory)

    except FileNotFoundError as e:
        raise click.ClickException(e)
