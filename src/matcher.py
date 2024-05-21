import fnmatch
from functions import debug


def any(item, rules):
    return None


def all(item, rules):
    matched = []
    for key, value in rules.items():
        for entry in item[key]:
            if fnmatch.fnmatch(entry, value):
                matched.append(key)
                break
    debug(
        "Matched {} of {} rules to {}. Matched rules: {}".format(
            len(matched), len(rules), item["name"][0], matched
        )
    )

    if len(matched) == len(rules):
        return True
    else:
        return False
