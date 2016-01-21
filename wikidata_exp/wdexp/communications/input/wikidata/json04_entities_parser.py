__author__ = 'Dani'


from wdexp.communications.input.wikidata.interfaces import EntityTracker
from wdexp.model.wikidata import WikidataEntity
import json


MODE_ACCEPTED = 0  # It will yield accepted entities
MODE_DISCARDED = 1  # It will yield discarded entities
MODE_BOTH_MIXED = 2  # It will yield acepted and discarded entities

SOURCE_ACCEPTED_KEY = "acepted"
SOURCE_DISCARDED_KEY = "discarded"


SOURCE_ID = "id"
SOURCE_ALIASES = "aliases"
SOURCE_DESC = "descriptions"
SOURCE_LABEL = "labels"
SOURCE_PG_SCORE = "pg_score"


class Json04EntitiesParser(EntityTracker):


    def __init__(self, source_file=None, mode=MODE_ACCEPTED):
        self._in_file = source_file
        self._mode = mode


    def yield_entities(self):

        with open(self._in_file, "r") as in_stream:
            json_object = json.load(in_stream)
            if self._mode in [MODE_ACCEPTED, MODE_BOTH_MIXED]:
                for a_dict in json_object[SOURCE_ACCEPTED_KEY]:
                    yield self._build_entity_from_dict(a_dict)
            if self._mode in [MODE_DISCARDED, MODE_BOTH_MIXED]:
                for a_dict in json_object[SOURCE_DISCARDED_KEY]:
                    yield self._build_entity_from_dict(a_dict)


    @staticmethod
    def _build_entity_from_dict(a_dict):
        aliases = []
        for elem in a_dict[SOURCE_ALIASES]:
            aliases.append(elem)
        return WikidataEntity(entity_id=a_dict[SOURCE_ID],
                              label=a_dict[SOURCE_LABEL],
                              description=a_dict[SOURCE_DESC],
                              pg_score=a_dict[SOURCE_PG_SCORE],
                              aliases=[elem for elem in a_dict[SOURCE_ALIASES]])
