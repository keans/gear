import click
from powerstrip import PluginManager
from powerstrip.exceptions import PluginPackageException

from gear.utils.utils import ensure_path
from gear.utils.config import PLUGIN_DIR, PLUGIN_REPOSITORY_DIR
from gear.plugins.readerplugin import ReaderPlugin
from gear.plugins.extractorplugin import ExtractorPlugin
from gear.plugins.transformerplugin import TransformerPlugin
from gear.plugins.reportplugin import ReportPlugin
from gear.plugins.reportaggregatorplugin import ReportAggregatorPlugin


def _get_plugin_manager() -> PluginManager:
    """
    helper function to obtain a plugin manager instance
    with prepared settings

    :return: plugin manager
    :rtype: PluginManager
    """
    return PluginManager(
        plugins_directory=PLUGIN_DIR,
        use_category=True,
        plugins_repo_directory=PLUGIN_REPOSITORY_DIR
    )


@click.group()
def plugin():
    """
    plugin subcommand
    """


@plugin.command()
def list():
    """
    list all installed plugins
    """
    # get plugin manager instance
    pm = _get_plugin_manager()

    # go through all plugin types and print them grouped
    for pt, plugin_type in (
        (ReaderPlugin, "ReaderPlugin"),
        (ExtractorPlugin, "ExtractorPlugin"),
        (TransformerPlugin, "TransformerPlugin"),
        (ReportPlugin, "ReportPlugin"),
        (ReportAggregatorPlugin, "ReportAggregatorPlugin")
    ):
        # get all classes of corresponding type
        plugin_classes = pm.get_plugin_classes(subclass=pt)

        for pc in plugin_classes.values():
            for cls in pc.values():
                # create class instance to obtain its metadata
                p = cls()

                # print plugin details
                click.echo(
                    f"{p.metadata.name:45s} {plugin_type:25s} "
                    f"{p.metadata.version}"
                )


@plugin.command()
@click.argument("pattern", required=False)
def search(pattern=None):
    """
    search plugin by given pattern in plugin repository directory
    """
    # get plugin manager instance
    pm = _get_plugin_manager()
    for fn in PLUGIN_REPOSITORY_DIR.glob(f"*{pm.plugin_ext}"):
        # apply pattern check on plugin package files
        if (pattern is None) or (pattern.lower() in fn.name.lower()):
            # either not pattern given or match found
            click.echo(f"{fn.name}")


@plugin.command()
@click.argument("directory")
@click.option("--force/--no-force", default=False)
def pack(directory: str, force: bool):
    """
    pack directory to create a plugin package
    """
    # get plugin manager instance
    pm = _get_plugin_manager()

    try:
        # pack the directory into a plugin package
        click.echo(f"packing directory '{directory}'...")
        fn = pm.pack(
            directory=directory,
            target_directory=PLUGIN_REPOSITORY_DIR,
            force=force
        )
        click.echo(f"stored plugin package to repo '{fn}'.")

    except PluginPackageException as e:
        click.echo(e)


@plugin.command()
@click.argument("package")
@click.option("--force/--no-force", default=False)
def install(package: str, force: bool):
    """
    install plugin package
    """
    # get plugin manager instance
    pm = _get_plugin_manager()

    try:
        # install the plugin
        click.echo(f"installing package '{package}'...")
        pm.install(package, force=force)

    except (ValueError, PluginPackageException) as e:
        click.echo(e)


@plugin.command()
@click.argument("package")
@click.argument("category")
def uninstall(package, category):
    """
    uninstall plugin package
    """
    # get plugin manager instance
    pm = _get_plugin_manager()

    try:
        # install the plugin
        click.echo(f"uninstalling package '{package}'...")
        pm.uninstall(
            plugin_name=package,
            category=category
        )

    except (ValueError, PluginPackageException) as e:
        click.echo(e)
