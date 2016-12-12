from wikidata_exp.wdexp.communications.input.wikidata.api_reader import WikidataApiReader
from wikidata_exp.wdexp.communications.input.wikidata.dump_parser import WikidataDumpParser
from wikidata_exp.wdexp.communications.input.wikidata.json05_properties_parser import Json05PropertiesParser
from wikidata_exp.wdexp.communications.input.wikidata.sparql_endpoint import WikidataSparqlEndpoint
from wikidata_exp.wdexp.wikidata.commands.agregated_class_summarizer_API import AgregatedClassSummaryCommand
from wikidata_exp.wdexp.wikidata.commands.aliases_properties_API import AliasesPropertiesCommand
from wikidata_exp.wdexp.wikidata.commands.class_ranking_DUMP import ClassRankingCommand
from wikidata_exp.wdexp.wikidata.props_survey.xslt_processing import XsltSurveyProcessor
from wikidata_exp.wdexp.wikidata.commands.class_instance_counter_JSON import ClassInstanceCounter
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


# processor = XsltSurveyProcessor("C:\Users\Dani\Documents\EII\doctorado\PAPERS_PROPIOS\WikidatavsTwitter\experimentos",
#                                 out_file="experiments.json")
# processor.process_survey()


#
# class_ranker = ClassRankingCommand(source_file_classes="classes_or_not.xlsx",
#                                    source_file_dump="C:\\Users\\Dani\\Documents\\EII\\doctorado\\datasets\\wdexp_datasets\\datasets\\wikidata-all\\wikidata-all.json",  # TODO
#                                    source_file_scores="C:\\Users\\Dani\\Documents\\EII\\doctorado\\datasets\\wdexp_datasets\\datasets\\filt_sort_page_rank.json",
#                                    out_file="agregated_pg_v2.json",
#                                    security_threshold=15)  # TODO

# class_ranker = ClassRankingCommand(source_file_classes="classes_or_not.xlsx",
#                                    source_file_dump="wikidata_slice.json",  # TODO
#                                    source_file_scores="filt_sort_pg_slice.json",
#                                    out_file="agregated_pg_slice.json",
#                                    security_threshold=0)  # TODO
#
# class_ranker.exec_command()


# class_summarizer = AgregatedClassSummaryCommand(source_agregated_scores="C:\\Users\\Dani\\Documents\\EII\\doctorado\\datasets\\resultados_wikidata\\agregated_pg.json",
#                                                 out_file="aggregated_class_summary_all.json",
#                                                 n_desirable_complete_classes=80000)


# class_summarizer = AgregatedClassSummaryCommand(source_agregated_scores="agregated_pg_v2.json",
#                                                 out_file="aggregated_class_summary_all_v2.json",
#                                                 n_desirable_complete_classes=8000)
#
# class_summarizer.exec_command()


# instance_counter = ClassInstanceCounter(source_file_instances="agregated_pg_v2.json",
#                                         out_file="instance_counts_agregated_pg_v2.json")
#
# instance_counter.exec_command()


# class_summarizer = AgregatedClassSummaryCommand(source_agregated_scores="instance_counts_agregated_pg_v2.json",
#                                                 out_file="instance_counts_aggregated_class_summary_all_v2.json",
#                                                 n_desirable_complete_classes=1000,
#                                                 n_instances_already_counted=True)
#
# class_summarizer.exec_command()


###################### Looking for different Pc (class-pointers)


# class_ranker = ClassRankingCommand(source_file_classes="classes_or_not.xlsx",
#                                    source_file_dump="C:\\Users\\Dani\\Documents\\EII\\doctorado\\datasets\\wdexp_datasets\\datasets\\wikidata-all\\wikidata-all.json",  # TODO
#                                    source_file_scores="C:\\Users\\Dani\\Documents\\EII\\doctorado\\datasets\\wdexp_datasets\\datasets\\filt_sort_page_rank.json",
#                                    out_file="agregated_pg_v2_Pc2.json",
#                                    security_threshold=15,
#                                    direct_class_pointers_input=["P31", "P279"])  # TODO
# class_ranker.exec_command()

# class_summarizer = AgregatedClassSummaryCommand(source_agregated_scores="agregated_pg_v2_Pc2.json",
#                                                 out_file="aggregated_class_summary_all_v2_Pc2.json",
#                                                 n_desirable_complete_classes=10000)
#
# class_summarizer.exec_command()

# instance_counter = ClassInstanceCounter(source_file_instances="agregated_pg_v2_Pc2.json",
#                                         out_file="instance_counts_agregated_pg_v2_Pc2.json")
#
# instance_counter.exec_command()
#
class_summarizer = AgregatedClassSummaryCommand(source_agregated_scores="instance_counts_agregated_pg_v2_Pc2.json",
                                                out_file="instance_counts_aggregated_class_summary_all_v2_Pc2.json",
                                                n_desirable_complete_classes=1000,
                                                n_instances_already_counted=True)

class_summarizer.exec_command()






