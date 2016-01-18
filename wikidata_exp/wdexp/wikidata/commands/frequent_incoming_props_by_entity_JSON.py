__author__ = 'Dani'

import json
from decimal import *


ENTITY_ID = "id"
PG_SCORE = "pg_score"
INCOMING_EDGES = "in_edges"
OUTCOMING_EDGES = "out_edges"
LABEL = "label"
DESCRIPTION = "desc"

PROP_ID = "id"
PROP_COUNT = "count"




class FrequentIncomingPropsByEntityCommand(object):


    def __init__(self, source_file, out_file_entities, out_file_props, relevance_threshold=15):
        self._in_file = source_file
        self._out_file_entities = out_file_entities
        self._out_file_props = out_file_props
        self._entities_edges_list = []
        self._props_count = {}  # Originally, a dict. We will turn in in sorted list for results
        self._threshold = relevance_threshold


    def exec_command(self, string_return=False):
        for a_dict in self._read_entities_dict():
            print a_dict
            self._process_incoming_edges(a_dict)
        self._sort_results()
        if string_return:
            return self._build_string_return()
        else:
            self._write_out_files()


    def _build_string_return(self):
        result = "Entities result:\n\n"
        result += json.dumps(self._entities_edges_list, indent=4)
        result += "\n\n\nProps result:\n"
        result += json.dumps(self._props_count, indent=4)
        return result


    def _write_out_files(self):
        self._write_json_result(self._entities_edges_list, self._out_file_entities)
        self._write_json_result(self._props_count, self._out_file_props)


    def _write_json_result(self, a_dict, a_path):
        with open(a_path, "w") as out_stream:
            json.dump(a_dict, out_stream, indent=4)


    def _sort_results(self):
        self._sort_entities()
        self._sort_props()

    def _sort_entities(self):
        self._entities_edges_list.sort(key=lambda x: Decimal(x[PG_SCORE]), reverse=True)

    def _sort_props(self):
        list_result = []
        for a_prop in self._props_count:
            list_result.append({PROP_ID: a_prop,
                                PROP_COUNT: self._props_count[a_prop]})
        list_result.sort(key=lambda x: x[PROP_COUNT], reverse=True)
        self._props_count = list_result


    def _read_entities_dict(self):
        with open(self._in_file, "r") as in_stream:
            base_dict = json.load(in_stream)
            for a_key in base_dict:
                a_return = base_dict[a_key]
                a_return[ENTITY_ID] = a_key
                yield a_return

    def _process_incoming_edges(self, info_dict):
        # Processing for entity list
        entity_dict = {ENTITY_ID: info_dict[ENTITY_ID],
                       PG_SCORE: info_dict[PG_SCORE],
                       INCOMING_EDGES: []}
        if LABEL in info_dict:
            entity_dict[LABEL] = info_dict[LABEL]
        if DESCRIPTION in info_dict:
            entity_dict[DESCRIPTION] = info_dict[DESCRIPTION]
        for an_incoming in info_dict[INCOMING_EDGES]:
            if info_dict[INCOMING_EDGES][an_incoming] >= self._threshold:
                entity_dict[INCOMING_EDGES].append({PROP_ID: an_incoming,
                                                    PROP_COUNT: info_dict[INCOMING_EDGES][an_incoming]})
                self._increase_prop_count(an_incoming, info_dict[INCOMING_EDGES][an_incoming])  # Processing prop count

        entity_dict[INCOMING_EDGES].sort(key=lambda x: x[PROP_COUNT], reverse=True)
        self._entities_edges_list.append(entity_dict)


    def _increase_prop_count(self, prop_id, value_to_increase):
        if prop_id not in self._props_count:
            self._props_count[prop_id] = 0
        self._props_count[prop_id] += value_to_increase





