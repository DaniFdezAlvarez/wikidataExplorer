__author__ = 'Dani'

import requests
from requests.adapters import HTTPAdapter
import json


PROP_ID = "id"
PROP_ALIASES = "aliases"
PROP_LABEL = "label"
PROP_DESCRIPTION = "description"
PROP_COUNT = "count"

# ###


class AliasesPropertiesCommand(object):
    def __init__(self, source_file, out_file, json_input=False):
        self._in_file = source_file
        self._out_file = out_file
        self._is_json_input = json_input


    def exec_command(self, string_return=False):
        target_properties = self._get_target_properties_from_input_file()
        sorted_result_list = []
        for a_property_dict in target_properties:
            try:
                sorted_result_list.append(self._get_info_of_property(a_property_dict))
            except:
                print "Error with property " + a_property_dict[PROP_ID]
        if string_return:
            return json.dumps(sorted_result_list, indent=4, encoding='utf-8')
        else:
            with open(self._out_file, "w") as out_stream:
                json.dump(sorted_result_list, out_stream, indent=4, encoding='utf-8')


    def _get_target_properties_from_input_file(self):

        result = []
        with open(self._in_file, "r") as in_stream:
            if self._is_json_input:
                return json.load(in_stream)
            else:
                for line in in_stream:
                    splitted = line.split(" : ")
                    if len(splitted) > 1:
                        result.append({PROP_ID: splitted[0],
                                       PROP_COUNT: int(splitted[1])})
        return result


    def _get_info_of_property(self, a_property_dict):
        property_url = self._build_uri_of_property(a_property_dict[PROP_ID])  # Done
        json_property = self._get_json_of_property(property_url)  # Done

        result = {PROP_ID: a_property_dict[PROP_ID],
                  PROP_COUNT: a_property_dict[PROP_COUNT],
                  # PROP_ALIASES: self._get_prop_aliases(a_property_dict[PROP_ID], json_property),
                  PROP_LABEL: self._get_prop_label(a_property_dict[PROP_ID], json_property),
                  PROP_DESCRIPTION: self._get_prop_description(a_property_dict[PROP_ID], json_property)}
        return result

    @staticmethod
    def _build_uri_of_property(a_property):
        return "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&languages=en&format=json".format(
            a_property)

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


