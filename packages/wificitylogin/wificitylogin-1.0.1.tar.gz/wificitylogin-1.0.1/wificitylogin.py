import logging
import sys
from configparser import ConfigParser
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# The configuration file format is
# [default]
# username = ...
# password = ...

CONFIG = Path.home() / ".wificity"
DETECT_URL = "http://detectportal.firefox.com"
TIMEOUT = 1

logger = logging.getLogger("wificitylogin")
__version__ = "1.0.1"


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Version %s", __version__)

    if not CONFIG.exists():
        logger.error("%s not found", CONFIG)
        sys.exit(1)

    config = ConfigParser()
    config.read(CONFIG)

    res = requests.get(DETECT_URL, timeout=TIMEOUT)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    magic = soup.select("input[name=magic]")
    if not magic:
        logger.warning("Magic value not found, this is probably not the captive portal")
        return

    data = {
        "4Tredir": DETECT_URL,
        "magic": magic[0]["value"],
        "username": config["default"]["username"],
        "password": config["default"]["password"],
    }

    res = requests.post(res.url, data=data, timeout=TIMEOUT)
    res.raise_for_status()


if __name__ == "__main__":
    main()
