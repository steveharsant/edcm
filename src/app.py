import configparser
import os
import sys
from loguru import logger
import time
from api import *
import os

__version__ = "0.1.0-Alpha1"


def app():

    def load_config():
        try:
            config.read(CONFIG_PATH)
            collection_rule_sets = [section for section in config.sections()]
            logger.success(
                f"Found collection rule sets: {', '.join(collection_rule_sets)}"
            )
        except:
            logger.error("Failed to read config file.")
            sys.exit(1)

    logger.info("Starting EDCM")

    CONFIG_PATH = os.getenv("EDCM_CONFIG_PATH", "/config/config.ini")
    EMBY_ADDRESS = os.getenv("EMBY_ADDRESS")
    EMBY_PORT = int(os.getenv("EMBY_PORT", 8096))
    EMBY_TOKEN = os.getenv("EMBY_TOKEN")
    SCAN_INTERVAL = int(os.getenv("EDCM_SCAN_INTERVAL", 600))  # seconds
    USE_SSL = os.getenv("EDCM_USE_SSL", False)
    HTTPS = "https" if USE_SSL != False else "http"

    logger.success("Imported environment variables")

    if not os.path.exists(CONFIG_PATH):
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

    config = configparser.ConfigParser()
    load_config()

    emby_api = api(
        base_url=f"{HTTPS}://{EMBY_ADDRESS}:{EMBY_PORT}", api_token=EMBY_TOKEN
    )

    libraries = emby_api.Libraries()
    library_names = [library["Name"] for library in libraries]
    logger.success(f"Found libraries: {', '.join(library_names)}")

    for section in config.sections():
        logger.info(f"Processing '{section}' collection rule set")

        params = {}
        results = []

        for key, value in config.items(section):
            params[key] = value

        for library in libraries:
            params["ParentId"] = library["Id"]
            response = emby_api.Items(params=params)
            results.extend(response)

            logger.info(f"Found {len(response)} matching items in {library['Name']}")

        start_index = 0
        batch_counter = 1
        batch_size = 50
        ids = [result["Id"] for result in results]
        total_batches = max(1, len(ids) // batch_size)

        while start_index < len(ids):
            end_index = min(start_index + batch_size, len(ids))
            batch = ",".join(ids[start_index:end_index])

            logger.info(f"Processing batch {batch_counter} of {total_batches}")
            emby_api.Collections(params={"Name": section, "Ids": batch})

            start_index += batch_size
            batch_counter += 1

        logger.success(f"Updated {section} collection")

    logger.success(f"Collection update complete")
    logger.info(f"Next run in {SCAN_INTERVAL} seconds")
    time.sleep(SCAN_INTERVAL)
    load_config()


if __name__ == "__main__":
    while True:
        app()
