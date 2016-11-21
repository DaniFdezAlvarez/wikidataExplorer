__author__ = 'Dani'

import json
from wikidata_exp.wdexp.communications.input.wikidata.interfaces import EntityTracker
from wikidata_exp.wdexp.model.wikidata import WikidataEntity


ENTITY_ID = "id"
PG_SCORE = "pg_score"
INCOMING_EDGES = "in_edges"
OUTCOMING_EDGES = "out_edges"
LABEL = "label"
DESCRIPTION = "desc"


class Json02EntitiesParser(EntityTracker):
    """
    FORMAT JSON02

    Summary: Dict that contains dicts about entities. The first key is the entity ID,
    and the value of that key is a new dict with all the corresponding info.
    None oh the fields in the new dict are mandatory, but there could be label,
    description, pg_score, out_edges and in_edges. The example will show the
    expected content of each field.

    The file is processed using the standard json library. This module is NOT ABLE
    to process BIG DATA

    Example:

        "Q55": {
            "desc": "largest constituent country of the Kingdom of the Netherlands, mainly located in Europe",
            "in_edges": {
                "P998": 1
            },
            "label": "Netherlands",
            "out_edges": {
                "P998": 33
            },
            "pg_score": "0.006326884451279281"
        },
        ...
    }


    """


    def __init__(self, source_file):
        self._in_file = source_file

    def _read_entities_dict(self):
        with open(self._in_file, "r") as in_stream:
            base_dict = json.load(in_stream)
            for a_key in base_dict:
                # id = a_key
                desc = None if DESCRIPTION not in base_dict[a_key] else base_dict[a_key][DESCRIPTION]
                label = None if LABEL not in base_dict[a_key] else base_dict[a_key][LABEL]
                pg_score = None if PG_SCORE not in base_dict[a_key] else base_dict[a_key][PG_SCORE]
                in_edges = None if INCOMING_EDGES not in base_dict[a_key] else base_dict[a_key][INCOMING_EDGES]
                out_edges = None if OUTCOMING_EDGES not in base_dict[a_key] else base_dict[a_key][OUTCOMING_EDGES]
                yield WikidataEntity(entity_id=a_key,
                                     label=label,
                                     description=desc,
                                     pg_score=pg_score,
                                     incoming_properties_id=in_edges,
                                     outcoming_properties_id=out_edges)

