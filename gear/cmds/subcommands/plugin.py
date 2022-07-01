import click
from powerstrip import PluginManager

from gear.utils.config import PLUGIN_DIR


@click.group()
def plugin():
    """
    plugin subcommand
    """


@plugin.command()
@click.argument("directory")
def pack(directory):
    """
    pack directory to create a plugin package
    """
    pm = PluginManager(PLUGIN_DIR, use_category=True)
    pm.pack(directory)


@plugin.command()
@click.argument("package")
def install(package):
    """
    install plugin package
    """
    pm = PluginManager(PLUGIN_DIR, use_category=True)
    pm.install(package)
