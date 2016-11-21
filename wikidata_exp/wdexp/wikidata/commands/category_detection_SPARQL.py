__author__ = 'Dani'

from wikidata_exp.wdexp.communications.input.wikidata.json04_entities_parser import Json04EntitiesParser
from wikidata_exp.wdexp.communications.input.wikidata.sparql_endpoint import WikidataSparqlEndpoint
from wikidata_exp.wdexp.communications.output.wikidata.json_entity_dumper import *
from wikidata_exp.wdexp.communications.output.json.json_out import write_json_object, json_to_string
# import requests
# import urllib
# from requests.adapters import HTTPAdapter


IS_INSTANCE = "is_instance"
HAS_INSTANCES = "have_instances"
BOTH = "both"
NO_TAXON = "no_taxon"

TYPE_RESULT = "type"
VALUE_RESULT = "value"
URI_RESULT = "uri"



class CategoryDetectionCommand(object):


    def __init__(self, source_file, out_file):

        self._in_file = source_file
        self._out_file = out_file
        self._endpoint = WikidataSparqlEndpoint()
        self._json_dumper = JsonEntityDumper(needed_fields=[P_ALIASES, P_ID, P_LABEL, P_DESC, P_PG_SCORE])


    def _exec_command(self, string_return=False):
        result = {IS_INSTANCE: [],
                  HAS_INSTANCES: [],
                  BOTH: [],
                  NO_TAXON: []}
        target_entities = self._read_target_entities()
        targeted = 0
        for an_entity in target_entities:
            print an_entity
            type_relation = self._decide_type_relation(an_entity)
            if type_relation == IS_INSTANCE:
                result[IS_INSTANCE].append(self._json_dumper.json_of_entity(an_entity))
            elif type_relation == HAS_INSTANCES:
                result[HAS_INSTANCES].append(self._json_dumper.json_of_entity(an_entity))
            elif type_relation == BOTH:
                result[BOTH].append(self._json_dumper.json_of_entity(an_entity))
            else:
                result[NO_TAXON].append(self._json_dumper.json_of_entity(an_entity))
            targeted += 1
        if string_return:
            return json_to_string(result, indent=4)
        else:
            write_json_object(result, self._out_file, indent=4)


    def _read_target_entities(self):
        for an_entity in Json04EntitiesParser(source_file=self._in_file).yield_entities():
            yield an_entity


    def _decide_type_relation(self, an_entity):
        target_id = an_entity.id
        has_instances = [triple for triple in self._endpoint.yield_instances_of_entity(target_id, 5)]
        is_instance_of = [triple for triple in self._endpoint.yield_classes_of_entity(target_id, 5)]
        if len(has_instances) != 0 and len(is_instance_of) != 0:
            return BOTH
        elif len(has_instances) != 0:
            return HAS_INSTANCES
        elif len(is_instance_of) != 0:
            return IS_INSTANCE
        else:  # 0 and 0, not in this kind of relations
            return NO_TAXON


