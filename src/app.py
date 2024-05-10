from loguru import logger
import time
from api import *
from variables import *
from functions import *
from watcher import *

__version__ = "0.2.1"


def main(config):

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

        logger.success(f"Processed items. {len(results)} matches found")

        if rules["behaviour"].get("dryrun", "false").lower() == "true":
            logger.warning(f"Dry run enabled for '{rule_set}' rule set. Match results:")
            for result in results:
                logger.info(result["name"][0])
        else:
            ids = [result["id"] for result in results]
            if emby_api.update_collection(rule_set, ids):
                logger.success(f"Updated '{rule_set}' collection")

    logger.success(f"Collection update complete")


if __name__ == "__main__":
    logger.info("Starting EDCM")

    file_changed_event = register_config_watcher()
    logger.success("Config watcher registered")

    try:
        while True:
            file_changed_event.clear()

            config = load_config()
            main(config)

            logger.info(f"Next run in {SCAN_INTERVAL} seconds")

            for i in range(SCAN_INTERVAL // 3):
                if file_changed_event.is_set():
                    logger.info(
                        "Collections rule set change detected. Processing rules"
                    )

                    break

                time.sleep(3)
    except KeyboardInterrupt:
        logger.info("EDCM has been requested to exit. Exiting")
        sys.exit(0)
