import configparser
import os
import sys
from loguru import logger
import time
from api import *
from variables import *
from functions import *
import os


__version__ = "0.1.0-Alpha1"


def main():

    if len(config.sections()) < 1:
        logger.warning("No rule sets found")
        return

    logger.info("Requesting library information")
    libraries = emby_api.Libraries()
    libraries = [i for i in libraries if i.get("Name") != "Collections"]

    for rule_set in config.sections():
        logger.info(f"Processing '{rule_set}' collection rule set")

        if len(config.items(rule_set)) < 1:
            logger.warning(f"No rules found in rule set '{rule_set}'")
            continue

        rules = determine_rule_type(config.items(rule_set))
        results = []

        for library in libraries:
            response = emby_api.LibraryContent(
                library_id=library["Id"], params=rules["params"]
            )

            content = []
            for item in response:
                content.append(map_content_data(item))

            for item in content:
                if determine_match(item, rule_set, rules["filters"]):
                    results.append(item)

        logger.success(f"Processed matches. {len(results)} matches found")

        ids = [result["id"] for result in results]
        if emby_api.update_collection(rule_set, ids):
            logger.success(f"Updated '{rule_set}' collection")

    logger.success(f"Collection update complete")


if __name__ == "__main__":
    logger.info("Starting EDCM")

    while True:
        load_config()
        main()
        logger.info(f"Next run in {SCAN_INTERVAL} seconds")
        time.sleep(SCAN_INTERVAL)
