from wikidata_exp.wdexp.communications.input.wikidata.api_reader import WikidataApiReader
from wikidata_exp.wdexp.communications.input.wikidata.dump_parser import WikidataDumpParser
from wikidata_exp.wdexp.communications.input.wikidata.json05_properties_parser import Json05PropertiesParser
from wikidata_exp.wdexp.communications.input.wikidata.sparql_endpoint import WikidataSparqlEndpoint
from wikidata_exp.wdexp.wikidata.commands.aliases_properties_API import AliasesPropertiesCommand
from wikidata_exp.wdexp.wikidata.props_survey.xslt_processing import XsltSurveyProcessor

__author__ = 'Dani'



import json




# command = AliasesPropertiesCommand("props_count_100000.json", "complete_props_count_100000.json", True)
# command.exec_command()


# with open("complete_props_count_100000.json") as in_stream:
#     json_object = json.load(in_stream)
#     with open("all_candidate_props.csv", "w")as out_stream:
#         for a_dict in json_object:
#             desc = "" if a_dict["description"] is None else a_dict["description"]
#             print '"' + a_dict["id"] + '";"' + a_dict["label"] + '";"' + desc + '";""'
#             out_stream.write(('"' + a_dict["id"] + '";"' + a_dict["label"] + '";"' + desc + '";""\n').encode("utf-8"))



# parser = WikidataDumpParser(source_file="../files/in/wikidata_slice.json")
#
# for triple in parser.yield_entity_triples():
#     print triple
#     print triple.subject.label
#     print triple.subject.description
#     for an_alias in triple.subject.aliases:
#         print ".", an_alias
#     print "--------"
#
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
#
# sparql_end = WikidataSparqlEndpoint()
# for a_triple in sparql_end.yield_subgraph_triples("Q76665"):
#     print a_triple
#
# print "____"
#
# for an_entity in sparql_end.yield_classes_of_entity("Q5", 5):
#     print an_entity
#
# print "____"
#
# for an_entity in sparql_end.yield_instances_of_entity("Q5", 5):
#     print an_entity


processor = XsltSurveyProcessor("C:\Users\Dani\Documents\EII\doctorado\PAPERS_PROPIOS\WikidatavsTwitter\experimentos",
                                out_file="experiments.json")
processor.process_survey()

