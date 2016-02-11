__author__ = 'Dani'

from wdexp.communications.input.wikidata.interfaces import PropertyTracker
from wdexp.model.wikidata import WikidataProperty
import json

PROP_ID = "id"
PROP_COUNT = "count"
PROP_LABEL = "label"
PROP_DESC = "description"


class Json05PropertiesParser(PropertyTracker):
    """

    FORMAT JSON05


    Summary: a list containing dicts of 2 elements: "id" and "count"

    Example:

    [
        {
            "count": 5382797,
            "id": "P31",
        },
        {
            "count": 813806,
            "id": "P106",
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
                                       n_appearances=a_dict[PROP_COUNT])

