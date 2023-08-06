import json

import yaml
from functools import partial
import re
from creationism.registration.utils import Text, chain_functions

def open_json(file_path):
    with open(str(file_path)) as file:
        return json.load(file)


def open_yaml(file_path):
    with open(str(file_path)) as file:
        return yaml.load(file, Loader=yaml.Loader)


def first_lowered(x):
    return chain_functions(
        x, Text.split_capitals, Text.lower, Text.split, partial(Text.get, index=0)
    )
def create_name_from_class_name(name):
    return " ".join(re.findall(".[^A-Z]*", name)[:-1])
