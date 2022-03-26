import os
from pathlib import Path

from dotenv import load_dotenv


# load .env file
load_dotenv()

# base config directory
CONFIG_DIRECTORY = Path(
    os.getenv("GEAR_CONFIG_DIRECTORY", "~/.config/gear/")
).expanduser()


# data directory
DATA_DIR = Path(
    os.getenv(
        "GEAR_DATA_DIRECTORY",
        "/tmp/data"
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

# directory where installed templates are located
TEMPLATE_DIR = Path(
    os.getenv(
        "GEAR_TEMPLATE_DIRECTORY",
        DATA_DIR.joinpath("templates/")
    ),
).expanduser()
