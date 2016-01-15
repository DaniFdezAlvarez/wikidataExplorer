__author__ = 'Dani'

from wdexp.communications.input.wikidata.dump_parser import WikidataDumpParser
from wdexp.communications.input.wikidata.api_reader import WikidataApiReader
from wdexp.communications.input.wikidata.sparql_endpoint import WikidataSparqlEndpoint

parser = WikidataDumpParser(source_file="../files/in/wikidata_slice.json")
#
# for triple in parser.yield_entity_triples():
#     print triple
#     print triple.subject.label
#     print triple.subject.description
#     for an_alias in triple.subject.aliases:
#         print ".", an_alias
#     print "--------"


# for elem in parser.yield_elements():
#     print elem, elem.n_outcoming_properties
#     for a_prop in elem.outcoming_properties_id:
#         print "----", a_prop


# api_reader = WikidataApiReader()
# a_prop = api_reader.get_property("P31")
# print a_prop.id
# print a_prop.label
# print a_prop.description
# print "___"
# for b in a_prop.aliases:
#     print b
#
# print "------------"
#
# earth = api_reader.get_entity("Q2")
# print earth
# print earth.label
# print earth.description
# for alias in earth.aliases:
#     print alias


sparql_end = WikidataSparqlEndpoint()
for a_triple in sparql_end.yield_outcoming_triples("Q76665"):
    print a_triple