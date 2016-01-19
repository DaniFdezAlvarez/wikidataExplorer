__author__ = 'Dani'

import json


def write_json_object(json_object, path, indent=None):
    with open(path, "w") as out_stream:
        json.dump(json_object, out_stream, indent=indent)


def json_to_string(json_object, indent):
    return json.dumps(json_object, indent=indent)

