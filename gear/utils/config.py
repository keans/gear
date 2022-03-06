import os
from pathlib import Path

from dotenv import load_dotenv

# load .env file
load_dotenv()

# base config directory
CONFIG_DIRECTORY = Path(
    os.getenv( "GEAR_CONFIG_DIRECTORY", "~/.config/gear/")
).expanduser()
