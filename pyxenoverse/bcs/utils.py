import re

def get_costume_creator_name(name):
    value = re.match(r'[^0-9]*([0-9]*)[^0-9]*', name).groups()[0]
    if not value or int(value) >= 10000:
        return name
    return name.replace(value, "10000")


