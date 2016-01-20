__author__ = 'Dani'

import json
import requests
import urllib
from requests.adapters import HTTPAdapter

BASE_ENDPOINT_URL = "https://query.wikidata.org/sparql?format=json&query="

SOURCE_ACCEPTED_KEY = "acepted"
SOURCE_ID_KEY = "id"


IS_INSTANCE = "is_instance"
HAS_INSTANCES = "have_instances"
BOTH = "both"
NO_TAXON = "no_taxon"

SPARQL_IS_INSTANCE = 'PREFIX wikibase: <http://wikiba.se/ontology#> ' \
                      'PREFIX wd: <http://www.wikidata.org/entity/> ' \
                      'PREFIX wdt: <http://www.wikidata.org/prop/direct/> ' \
                      'SELECT ?obj ?a_prop WHERE {{ wd:{} ?a_prop ?obj . ' \
                      'FILTER (?a_prop IN (wdt:P31)) ' \
                      'SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}}}LIMIT 5'


SPARQL_HAS_INSTANCES = 'PREFIX wikibase: <http://wikiba.se/ontology#> ' \
                      'PREFIX wd: <http://www.wikidata.org/entity/> ' \
                      'PREFIX wdt: <http://www.wikidata.org/prop/direct/> ' \
                      'SELECT ?sub ?a_prop WHERE {{ ?sub ?a_prop wd:{} . ' \
                      'FILTER (?a_prop IN (wdt:P31, wdt:P279 )) ' \
                      'SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}}}LIMIT 5'

PARAM_ENTITY_HAS_INSTANCES = "sub"
PARAM_ENTITY_IS_INSTANCE = "obj"

TYPE_RESULT = "type"
VALUE_RESULT = "value"
URI_RESULT = "uri"

BASE_WIKIDATA_ENTITY_URL = "http://www.wikidata.org/entity/Q"


class CategoryDetectionCommand(object):


    def __init__(self, source_file, out_file):

        self._in_file = source_file
        self._out_file = out_file


    def _exec_command(self, string_return=False):
        result = {IS_INSTANCE: [],
                  HAS_INSTANCES: [],
                  BOTH: [],
                  NO_TAXON: []}
        target_dicts = self._read_dicts()
        targeted = 0
        for a_dict in target_dicts:
            print a_dict
            type_relation = self._decide_type_relation(a_dict)
            if type_relation == IS_INSTANCE:
                result[IS_INSTANCE].append(a_dict)
            elif type_relation == HAS_INSTANCES:
                result[HAS_INSTANCES].append(a_dict)
            elif type_relation == BOTH:
                result[BOTH].append(a_dict)
            else:
                result[NO_TAXON].append(a_dict)
            targeted += 1
            print targeted
        if string_return:
            return json.dumps(result, indent=4)
        else:
            with open(self._out_file, "w") as out_stream:
                json.dump(result, out_stream, indent=4)


    def _read_dicts(self):
        with open(self._in_file, "r") as in_stream:
            json_object = json.load(in_stream)
            for a_dict in json_object[SOURCE_ACCEPTED_KEY]:
                yield a_dict


    def _decide_type_relation(self, a_dict):
        target_id = a_dict[SOURCE_ID_KEY]
        has_instances = self._build_and_execute_query(SPARQL_HAS_INSTANCES, target_id, PARAM_ENTITY_HAS_INSTANCES)
        is_instance_of = self._build_and_execute_query(SPARQL_IS_INSTANCE, target_id, PARAM_ENTITY_IS_INSTANCE)
        if len(has_instances) != 0 and len(is_instance_of) != 0:
            return BOTH
        elif len(has_instances) != 0:
            return HAS_INSTANCES
        elif len(is_instance_of) != 0:
            return IS_INSTANCE
        else:  # 0 and 0, not in this kind of relations
            return NO_TAXON



    def _build_and_execute_query(self, query, target_id, entity_param):
        sparql_query = self._build_query(query, target_id)
        json_query_result = self._exec_query(sparql_query)
        return self._get_entities(json_query_result, entity_param)



    @staticmethod
    def _build_query(query_skeleton, target_entity_node):
        return query_skeleton.format(target_entity_node)


    @staticmethod
    def _exec_query(sparql_query):
        url = BASE_ENDPOINT_URL + urllib.quote(sparql_query)
        ses = requests.Session()
        ses.mount(url, HTTPAdapter(max_retries=10))
        json_content = requests.get(url).json()
        return json_content

    @staticmethod
    def _get_entities(json_raw, entity_param):
        result = []
        target_list = json_raw["results"]["bindings"]
        for a_candidate in target_list:
            if a_candidate[entity_param][TYPE_RESULT] == URI_RESULT and \
                    a_candidate[entity_param][VALUE_RESULT].startswith(BASE_WIKIDATA_ENTITY_URL):
                result.append(str(a_candidate[entity_param][VALUE_RESULT][len(BASE_WIKIDATA_ENTITY_URL)-1:]))
        return result








