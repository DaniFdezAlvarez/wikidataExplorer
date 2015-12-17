__author__ = 'Dani'

import requests
from requests.adapters import HTTPAdapter
import json

ENTITY_ID = "id"
ENTITY_ALIASES = "aliases"
ENTITY_LABEL = "labels"
ENTITY_DESCRIPTION = "descriptions"
ENTITY_PG_SCORE = "pg_score"

MARGIN_DISCARDED_WIKI = 400


class EntitiesPropertiesCommand(object):
    def __init__(self, source_file, out_file, number_of_entities):
        self._in_file = source_file
        self._out_file = out_file
        self._top_k = number_of_entities


    def exec_command(self, string_return=False):
        id_tuples = self._read_top_k_ids()
        result = {"acepted" : [],
                  "discarded" : []}
        succeses = 0
        for a_tuple in id_tuples:  # ID, score
            candidate_dict = self._get_entity_properties_dict(a_tuple[0], a_tuple[1])
            print candidate_dict
            if self._is_worthy_entity_dict(candidate_dict):
                result["acepted"].append(candidate_dict)
                succeses += 1
                print succeses
                if succeses >= self._top_k:
                    break
            else:
                result["discarded"].append(candidate_dict)

        if string_return:
            return str(result)
        else:
            with open(self._out_file, "w") as out_stream:
                json.dump(result, out_stream)


    def _is_worthy_entity_dict(self, entity_dict):
        if entity_dict[ENTITY_DESCRIPTION] is not None and (
                        "wiki" in entity_dict[ENTITY_DESCRIPTION] or "Wiki" in entity_dict[ENTITY_DESCRIPTION]):
            return False
        if entity_dict[ENTITY_LABEL] is not None and (
                        "wiki" in entity_dict[ENTITY_LABEL] or "Wiki" in entity_dict[ENTITY_LABEL]):
            return False
        return True


    def _read_top_k_ids(self):
        result = []
        with open(self._in_file, "r") as in_stream:
            for a_key in self._read_keys_in_chunks(in_stream, ",", self._top_k + MARGIN_DISCARDED_WIKI):
                result.append(a_key)

        return result

    def _read_keys_in_chunks(self, in_stream, break_char, top_k):
        yielded = 0
        previous_result = ""
        while yielded < top_k:
            data = in_stream.read(1024)
            if not data:
                break
            last_index = 0
            for i in range(0, len(data)):
                if data[i] == break_char:
                    yield self._extract_key_value_from_substring(previous_result + data[last_index:i + 1])
                    yielded += 1
                    if yielded >= top_k:
                        break
                    previous_result = ""
                    last_index = i + 1
            previous_result += data[last_index:]
        if yielded < top_k:
            yield self._extract_key_value_from_substring(previous_result)


    def _extract_key_value_from_substring(self, target_str):
        first_index = None
        last_index = None
        colon_index = None
        i = 0
        for char in target_str:
            if char == '"':
                if not first_index:
                    first_index = i
                else:
                    last_index = i
            if char == ":":
                colon_index = i
                break
            i += 1
        return target_str[first_index + 1:last_index], target_str[colon_index + 2:-1]


    def _get_entity_properties_dict(self, entity_id, pg_score):
        entity_url = self._build_uri_of_property(entity_id)
        json_entity = self._get_json_of_property(entity_url)
        result = {ENTITY_ID: entity_id,
                  ENTITY_ALIASES: self._get_prop_aliases(entity_id, json_entity),
                  ENTITY_LABEL: self._get_prop_label(entity_id, json_entity),
                  ENTITY_DESCRIPTION: self._get_prop_description(entity_id, json_entity),
                  ENTITY_PG_SCORE: pg_score}
        return result


    @staticmethod
    def _build_uri_of_property(entity_id):
        return "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&languages=en&format=json".format(
            entity_id)

    @staticmethod
    def _get_json_of_property(property_url):
        ses = requests.Session()
        ses.mount(property_url, HTTPAdapter(max_retries=10))
        json_content = requests.get(property_url).json()
        return json_content

    @staticmethod
    def _get_prop_aliases(prop_id, json_property):
        result = []
        target_dict = json_property['entities'][prop_id]['aliases']
        if 'en' in target_dict:
            for elem in target_dict['en']:
                result.append(elem['value'])
        return result

    @staticmethod
    def _get_prop_label(prop_id, json_property):
        result = None
        target_dict = json_property['entities'][prop_id]['labels']
        if 'en' in target_dict:
            result = target_dict['en']['value']
        return result

    @staticmethod
    def _get_prop_description(prop_id, json_property):
        result = None
        target_dict = json_property['entities'][prop_id]['descriptions']
        if 'en' in target_dict:
            result = target_dict['en']['value']
        return result
