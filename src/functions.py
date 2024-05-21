from loguru import logger
from variables import *


def debug(message, debug=DEBUG):
    if debug is True:
        logger.debug(message)


def determine_rule_type(rule_set):
    rules = {"params": {}, "filters": {}, "behaviour": {}}
    for key, value in rule_set:
        if key.lower() in [item.lower() for item in items_param_rules]:
            rules["params"][key] = value
        elif key.lower() in [item.lower() for item in config_behaviour_rules]:
            rules["behaviour"][key] = value
        else:
            rules["filters"][key] = value

    return rules


def map_content_data(item):

    entry = {}

    # Keys must be in lower case
    # Ensure all items are wrapped in a list for more simple iterative processing
    entry["name"] = [item.get("Name", "")]
    entry["id"] = item.get("Id", "")
    entry["datecreated"] = [item.get("DateCreated", "")]
    entry["overview"] = [item.get("Overview", "")]
    entry["runtimeticks"] = [item.get("RunTimeTicks", "")]
    entry["isfolder"] = [item.get("IsFolder", "")]
    entry["parentid"] = [item.get("ParentId", "")]
    entry["type"] = [item.get("Type", "")]
    entry["enddate"] = [item.get("EndDate", "")]
    entry["genres"] = item.get("Genres", "")
    entry["people"] = [person["Name"] for person in item.get("People", "")]
    entry["studios"] = [studio["Name"] for studio in item.get("Studios", [])]

    return entry
