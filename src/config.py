from loguru import logger
from variables import *
import sys
import configparser
from functions import debug


def initialise():
    if os.path.exists(CONFIG_PATH):
        debug("Found config file on disk")
        return
    else:
        logger.warning(
            f"Config file not found at {CONFIG_PATH}. Generating config file"
        )

        with open(f"{os.path.dirname(__file__)}/config.ini.tmpl", "r") as f:
            config_template = f.read()

        try:
            with open(CONFIG_PATH, "w") as f:
                f.write(config_template)
        except:
            logger.error("Failed to create config file. Is the path writable? Exiting")
            sys.exit(1)


def load():
    initialise()

    preferences = {}
    collections = configparser.ConfigParser()

    try:
        collections.read(CONFIG_PATH)
    except:
        logger.error("Failed to read config file. Exiting.")
        sys.exit(1)

    for section in collections.sections():
        if section.lower().strip() == "preferences":
            preferences = dict(collections.items(section))
            collections.remove_section(section)
            break

    logger.success(f"Found collections: {', '.join(collections)}")
    debug(f"User config: {preferences}")

    return collections, preferences
