__author__ = 'Dani'

import ijson
import json

PG_SCORE = "pg_score"
INCOMING_EDGES = "in_edges"
OUTCOMING_EDGES = "out_edges"
LABEL = "label"
DESCRIPTION = "desc"


class CommonIncomingCommand(object):

    def __init__(self, source_dump_file, out_file, source_target_ids_file, topk_target_entities):
        self._in_dump_file = source_dump_file
        self._in_targets_file = source_target_ids_file
        self._out_file = out_file
        self._topk = topk_target_entities
        self._edges_dict = {}


    def _exec_command(self, string_return=False):
        self._read_target_entities()
        self._parse_dump_file()
        if string_return:
            return str(self._edges_dict)
        else:
            with open(self._out_file, "w") as out_stream:
                json.dump(self._edges_dict, out_stream)



    def _parse_dump_file(self):
        json_stream = open(self._in_dump_file, "r")
        elem_id = None
        elem_type = None
        desc_en = None
        label_en = None
        datatype = None
        datavalue_type = None
        current_claim_key = None
        datavalue_num_id = None
        possible_edges = []

        elem_count = 1

        for prefix, event, value in ijson.parse(json_stream):
            if event == 'end_map':
                if prefix == 'item':
                    for tuple_4 in possible_edges:
                        if self._is_valid_edge(elem_type, tuple_4[0],
                                               tuple_4[1]):  # triple: datatype, datavalue_type, datavalue_num_id
                            self._add_triple_if_proceed(elem_id, tuple_4[2], 'Q' + tuple_4[3], label_en, desc_en)
                            # print elem_id, tuple_4[2], 'Q' + tuple_4[3]
                    elem_id = None
                    elem_type = None
                    current_claim_key = None
                    # label_en = None
                    datavalue_num_id = None
                    datavalue_type = None
                    elem_count += 1
                    possible_edges = []
                    if elem_count % 10000 == 0:
                        print 'Llevamos ' + str(elem_count)
                elif prefix == "item.claims." + str(current_claim_key) + ".item":
                    possible_edges.append((datatype, datavalue_type, current_claim_key, str(datavalue_num_id)))

            elif event == 'string':
                if prefix == 'item.id':
                    elem_id = value
                elif prefix == 'item.type':
                    elem_type = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datatype':
                    datatype = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datavalue.value.entity-type':
                    datavalue_type = value
                elif prefix == 'item.labels.en.value':
                    label_en = value
                elif prefix == 'item.descriptions.en.value':
                    desc_en = value
            elif event == 'map_key' and prefix == 'item.claims':
                current_claim_key = value
            elif event == 'number' and prefix == 'item.claims.' + str(
                    current_claim_key) + '.item.mainsnak.datavalue.value.numeric-id':
                datavalue_num_id = value
            # elif event == "end_array" and prefix == "item.claims." + str(current_claim_key):
            #     possible_edges.append((datatype, datavalue_type, current_claim_key, str(datavalue_num_id)))


    def _read_target_entities(self):
        with open(self._in_targets_file, "r") as in_stream:
            success = 0
            for line in in_stream:  # JSON INDENTED, JUST A DICT
                pieces = self._parse_key_and_rank(line)
                if len(pieces) == 2:
                    self._edges_dict[pieces[0]] = {PG_SCORE: pieces[1],
                                                   INCOMING_EDGES: {},
                                                   OUTCOMING_EDGES: {}}
                    success += 1
                    if success >= self._topk:
                        break

    @staticmethod
    def _parse_key_and_rank(raw_string):
        first_index = None
        last_index = None
        colon_index = None
        i = 0
        for char in raw_string:
            if char == '"':
                if not first_index:
                    first_index = i
                else:
                    last_index = i
            if char == ":":
                colon_index = i
                break
            i += 1
        if None not in [first_index, last_index, colon_index]:
            return str(raw_string[first_index + 1:last_index]), str(raw_string[colon_index + 2:-2])
        else:
            return ()


    @staticmethod
    def _is_valid_edge(subj_type, data_nature, data_type):
        if subj_type == 'item' and data_nature == 'wikibase-item' and data_type == 'item':
            return True
        return False


    def _add_triple_if_proceed(self, origin, property, target, label_origin, desc_origin):
        if origin in self._edges_dict:
            if LABEL not in self._edges_dict[origin]:
                self._edges_dict[origin][LABEL] = label_origin
            if DESCRIPTION not in self._edges_dict[origin]:
                self._edges_dict[origin][DESCRIPTION] = desc_origin
            if property not in self._edges_dict[origin][OUTCOMING_EDGES]:
                self._edges_dict[origin][OUTCOMING_EDGES][property] = 0
            self._edges_dict[origin][OUTCOMING_EDGES][property] += 1
        if target in self._edges_dict:
            if property not in self._edges_dict[target][INCOMING_EDGES]:
                self._edges_dict[target][INCOMING_EDGES][property] = 0
            self._edges_dict[target][INCOMING_EDGES][property] += 1
