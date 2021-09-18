###############################################################################
# Environment
###############################################################################
import platform
import sys
from pathlib import Path

from pydantic import BaseSettings

ROOT_DIR = Path(__file__).parent.absolute()

plt = platform.system()
if plt == "Windows":
    # print("Your system is Windows")
    INTELIJ_CONFIG_DIR = r"%APPDATA%\JetBrains"
elif plt == "Linux":
    # print("Your system is Linux")
    INTELIJ_CONFIG_DIR = r"~/.config/JetBrains/"
elif plt == "Darwin":
    # print("Your system is MacOS")
    INTELIJ_CONFIG_DIR = r"~/Library/Application Support/JetBrains"
else:
    print("Unidentified system")
    sys.exit(1)


class Environment(BaseSettings):
    log_level: str = "INFO"
    twbm_db_url: str = "sqlite:///db/bm.db"

    @property
    def dbfile(self):
        return f"{self.twbm_db_url.split('sqlite:///')[-1]}"


config = Environment()
_ = None
