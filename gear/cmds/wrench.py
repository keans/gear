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

# set logging level
# logging.basicConfig(level=logging.WARNING)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    if debug is True:
        # enable DEBUG log level
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


from gear.cmds.subcommands.config import config
cli.add_command(config)



@cli.command()
@click.argument("configname")
def run(configname):
    try:
        # ensure that filename is a Path
        fn = guess_filename(
            name=configname,
            directories=CONFIG_DIR.joinpath(configname),
            default_extension=".yml"
        )

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

