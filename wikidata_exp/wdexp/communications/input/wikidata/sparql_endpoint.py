__author__ = 'Dani'


from wdexp.communications.input.wikidata.interfaces import TripleTracker
import requests
import urllib
from requests.adapters import HTTPAdapter



BASE_ENDPOINT_URL = "https://query.wikidata.org/sparql?format=json&query="

QUERY_INCOMING = 'PREFIX wikibase: <http://wikiba.se/ontology#> ' \
                 'PREFIX wd: <http://www.wikidata.org/entity/>  ' \
                 'SELECT ?prop ?sub WHERE {{?sub ?prop wd:{} . ' \
                 'SERVICE wikibase:label {{bd:serviceParam wikibase:language "en" .}}}}'

QUERY_OUTCOMING = 'PREFIX wikibase: <http://wikiba.se/ontology#> ' \
                  'PREFIX wd: <http://www.wikidata.org/entity/>  ' \
                  'SELECT ?prop ?obj WHERE {{wd:{} ?prop ?obj . ' \
                  'SERVICE wikibase:label {{bd:serviceParam wikibase:language "en" .}}}}'


INCOMING_QUERY_PROP = "prop"
INCOMING_QUERY_ENTITY = "sub"

OUTCOMING_QUERY_PROP = "prop"
OUTCOMING_QUERY_ENTITY = "obj"

TYPE_RESULT = "type"
VALUE_RESULT = "value"
URI_RESULT = "uri"

BASE_WIKIDATA_ENTITY_URL = "http://www.wikidata.org/entity/Q"
BASE_WIKIDATA_PROPERTY_URL = "http://www.wikidata.org/prop/direct/P"



class WikidataSparqlEndpoint(TripleTracker):


    def yield_incoming_triples(self, entity_id, limit=None):
        sparql_query = self._build_query(QUERY_INCOMING, entity_id)
        json_raw = self._exec_sparql_query(sparql_query)
        limit = -1 if limit is None else limit
        yielded = 0
        for a_tuple_2 in self._get_prop_entity_tuples(json_raw, INCOMING_QUERY_PROP, INCOMING_QUERY_ENTITY):
            if yielded == limit:
                break
            yield a_tuple_2[1], a_tuple_2[0], entity_id
            yielded += 1


    def yield_outcoming_triples(self, entity_id, limit=None):
        sparql_query = self._build_query(QUERY_OUTCOMING, entity_id)
        json_raw = self._exec_sparql_query(sparql_query)
        limit = -1 if limit is None else limit
        yielded = 0
        for a_tuple_2 in self._get_prop_entity_tuples(json_raw, OUTCOMING_QUERY_PROP, OUTCOMING_QUERY_ENTITY):
            if yielded == limit:
                break
            yield entity_id, a_tuple_2[0], a_tuple_2[1]
            yielded += 1


    def yield_subgraph_triples(self, entity_id, limit=None):
        yielded = 0
        for a_triple in self.yield_outcoming_triples(entity_id, limit):
            yield a_triple
            yielded += 1
        if limit is not None:
            limit -= yielded
            if limit <= 0:
                return
        for a_triple in self.yield_incoming_triples(entity_id, limit):
            yield a_triple


    @staticmethod
    def _build_query(query_skeleton, target_entity_node):
        return query_skeleton.format(target_entity_node)


    @staticmethod
    def _exec_sparql_query(sparql_query):
        url = BASE_ENDPOINT_URL + urllib.quote(sparql_query)
        ses = requests.Session()
        ses.mount(url, HTTPAdapter(max_retries=10))
        json_content = requests.get(url).json()
        return json_content

    @staticmethod
    def _get_prop_entity_tuples(json_raw, prop_param, entity_param):
        """
        It returns a tuple, being the first position a property and the second one an entity

        :param json_raw:
        :param prop_param:
        :param entity_param:
        :return:
        """
        target_list = json_raw["results"]["bindings"]
        for a_candidate in target_list:
            if a_candidate[prop_param][TYPE_RESULT] == URI_RESULT and \
                    a_candidate[entity_param][TYPE_RESULT] == URI_RESULT and \
                    a_candidate[entity_param][VALUE_RESULT].startswith(BASE_WIKIDATA_ENTITY_URL):
                yield (
                    str(a_candidate[prop_param][VALUE_RESULT][len(BASE_WIKIDATA_PROPERTY_URL) - 1:]),
                    str(a_candidate[entity_param][VALUE_RESULT][len(BASE_WIKIDATA_ENTITY_URL) - 1:])
                )
