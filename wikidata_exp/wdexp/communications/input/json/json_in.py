__author__ = 'Dani'

import json



def read_json_object(path):
    with open(path, "r") as in_stream:
        return json.load(in_stream)

def string_to_json(target_string):
    return json.loads(target_string)
