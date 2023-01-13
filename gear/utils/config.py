import os
from pathlib import Path

from dotenv import load_dotenv


# load .env file
load_dotenv()

# base config directory
CONFIG_DIR = Path(
    os.getenv("GEAR_CONFIG_DIRECTORY", "~/.config/gear/")
).expanduser()


# data directory
DATA_DIR = Path(
    os.getenv(
        "GEAR_DATA_DIRECTORY",
        "/tmp/gear_data"
    )
).expanduser()


# directory to which output is written
OUTPUT_DIR = DATA_DIR.joinpath("output/")


# directory where installed plugins are located
PLUGIN_DIR = Path(
    os.getenv(
        "GEAR_PLUGIN_DIRECTORY",
        DATA_DIR.joinpath("plugins/")
    ),
).expanduser()


# repository directory where packed plugins are located
PLUGIN_REPOSITORY_DIR = Path(
    os.getenv(
        "GEAR_PLUGIN_REPOSITORY_DIRECTORY",
        "/tmp/gear_pluginsrepo"
    ),
).expanduser()
