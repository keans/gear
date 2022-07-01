import click

from gear.utils.config import CONFIG_DIR
from gear.utils.utils import guess_filename, get_user
from gear.evaluator.evaluatorconfigmanager import EvaluatorConfigManager


@click.group()
def config():
    """
    config subcommand
    """


@config.command()
@click.option("--full/--no-full", default=False)
def list(full):
    """
    list all existing configurations
    """
    ecm = EvaluatorConfigManager(CONFIG_DIR)
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
        fn = guess_filename(
            name=name,
            directories=CONFIG_DIR.joinpath(name),
            default_extension=".yml"
        )

        print(f"{fn}\n")
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
    ecm = EvaluatorConfigManager(CONFIG_DIR)
    try:
        fn = ecm.create_config(
            name=name,
            description=description,
            author=author
        )
        click.echo(f"created config '{fn}'.")

    except FileExistsError as e:
        raise click.ClickException(e)
