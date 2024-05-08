from loguru import logger
import configparser
from variables import *
import sys


def debug(message, debug=DEBUG):
    if debug is True:
        logger.debug(message)


config = configparser.ConfigParser()


def determine_match(item, rule_set):
    match = True
    for key, value in rule_set.items():
        if value not in item[key]:
            match = False

    return match


def determine_rule_type(rule_set):
    rules = {"params": {}, "filters": {}}
    for key, value in rule_set:
        if key.lower() in [item.lower() for item in items_param_rules]:
            rules["params"][key] = value
        else:
            rules["filters"][key] = value

    return rules


def load_config():
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
    try:
        config.read(CONFIG_PATH)
        collection_rule_sets = [section for section in config.sections()]
        logger.success(f"Found collection rule sets: {', '.join(collection_rule_sets)}")

    except:
        logger.error("Failed to read config file. Exiting.")
        sys.exit(1)


def map_content_data(item):

    entry = {}

    # Keys must be in lower case
    # Wrap all items in a list for more simple iterative processing
    entry["name"] = [item.get("Name", "")]
    entry["id"] = item.get("Id", "")
    entry["datecreated"] = [item.get("DateCreated", "")]
    entry["overview"] = [item.get("Overview", "")]
    entry["runtimeticks"] = [item.get("RunTimeTicks", "")]
    entry["isfolder"] = [item.get("IsFolder", "")]
    entry["parentid"] = [item.get("ParentId", "")]
    entry["type"] = [item.get("Type", "")]
    entry["enddate"] = [item.get("EndDate", "")]
    entry["genres"] = [item.get("Genres", "")]
    entry["people"] = [person["Name"] for person in item.get("People", "")]
    entry["studios"] = [person["Name"] for person in item.get("Studios", "")]

    return entry
