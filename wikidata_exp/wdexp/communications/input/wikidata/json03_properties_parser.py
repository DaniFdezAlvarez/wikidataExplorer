__author__ = 'Dani'

from wikidata_exp.wdexp.communications.input.wikidata.interfaces import PropertyTracker
from wikidata_exp.wdexp.model.wikidata import WikidataProperty
import json

PROP_ID = "id"
PROP_COUNT = "count"
PROP_LABEL = "label"
PROP_DESC = "description"


class Json03PropertyParser(PropertyTracker):
    """

    FORMAT JSON03


    Summary: a list containing dicts of 4 elements: "id", "count", "label" and "description"

    Example:

    [
        {
            "count": 5382797,
            "description": "this item is a specific example and a member of that class. Not to be confused with Property:P279 (subclass of).",
            "id": "P31",
            "label": "instance of"
        },
        {
            "count": 813806,
            "description": "occupation of a person; see also \"field of work\" (Property:P101)",
            "id": "P106",
            "label": "occupation"
        },
         ...
    ]


    """

    def __init__(self, source_file):
        self._in_file = source_file

    def yield_properties(self):
        with open(self._in_file, "r") as in_stream:
            json_obj = json.load(in_stream)
            for a_dict in json_obj:
                yield WikidataProperty(property_id=a_dict[PROP_ID],
                                       n_appearances=a_dict[PROP_COUNT],
                                       label=a_dict[PROP_LABEL],
                                       description=a_dict[PROP_DESC])

