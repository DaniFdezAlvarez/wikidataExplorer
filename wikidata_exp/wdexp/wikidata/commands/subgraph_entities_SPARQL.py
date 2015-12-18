__author__ = 'Dani'

import networkx as nx
import requests
import urllib
import matplotlib.pyplot as plt
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


class SubgraphEntitiesCommand(object):
    def __init__(self, out_file, out_img):
        self._out_file = out_file
        self._out_img = out_img


    def exec_command(self, entities, string_return=False, img_return=False, file_return=True, object_return=False):
        subgraph = nx.DiGraph()
        for entity in entities:
            outcoming = self._get_objects_in_triples(entity)
            for an_outcoming_node in outcoming:
                subgraph.add_edge(entity, an_outcoming_node)
            incoming = self._get_subjects_in_triples(entity)
            for an_incoming_node in incoming:
                subgraph.add_edge(an_incoming_node, entity)
        if file_return:
            self._serialize_graph_text(subgraph)
        if img_return:
            self._serialize_graph_image(subgraph)

        if object_return:
            return subgraph
        else:
            pass  # TODO: implement textual return


    def _serialize_graph_text(self, graph):
        with open(self._out_file, "w") as out_stream:
            for edge in graph.edges():
                out_stream.write(str(edge[0]) + "\t" + str(edge[1]) + "\n")

    def _serialize_graph_image(self, graph):
        pos = nx.random_layout(graph)
        nx.draw_networkx(G=graph, node_size=100, pos=pos, font_color='b')
        plt.savefig(self._out_img)


    def _get_objects_in_triples(self, target_node):
        sparql_query = self._build_query(QUERY_OUTCOMING, target_node)
        json_raw = self._exec_sparql_query(sparql_query)
        return self._get_valid_entities(json_raw, OUTCOMING_QUERY_PROP, OUTCOMING_QUERY_ENTITY)

    def _get_subjects_in_triples(self, target_node):
        sparql_query = self._build_query(QUERY_INCOMING, target_node)
        json_raw = self._exec_sparql_query(sparql_query)
        return self._get_valid_entities(json_raw, INCOMING_QUERY_PROP, INCOMING_QUERY_ENTITY)


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
    def _get_valid_entities(json_raw, prop_param, entity_param):
        result = []
        target_list = json_raw["results"]["bindings"]
        for a_candidate in target_list:
            if a_candidate[prop_param][TYPE_RESULT] == URI_RESULT and \
                    a_candidate[entity_param][TYPE_RESULT] == URI_RESULT and \
                    a_candidate[entity_param][VALUE_RESULT].startswith(BASE_WIKIDATA_ENTITY_URL):
                result.append(str(a_candidate[entity_param][VALUE_RESULT][len(BASE_WIKIDATA_ENTITY_URL)-1:]))
        return result





