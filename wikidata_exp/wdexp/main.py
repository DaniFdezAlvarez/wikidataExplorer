__author__ = 'Dani'

from wdexp.wikidata.commands.aliases_properties_API import AliasesPropertiesCommand
from wdexp.aol.commands.count_ngrams_DUMP import CountNgramsCommand
from wdexp.g_trends.commads.track_trends_SCRAP import TrackTrendsCommand
from wdexp.wikidata.commands.graph_entities_DUMP import GraphEntitiesCommand
from wdexp.wikidata.commands.page_rank_NETG import PageRankCommand
from wdexp.wikidata.commands.page_rank_filter_JSON import PageRankFilterCommand
from wdexp.wikidata.commands.entities_properties_API import EntitiesPropertiesCommand
from wdexp.wikidata.commands.entity_ranker_JSON import EntityRankerCommand
from wdexp.wikidata.commands.subgraph_entities_SPARQL import SubgraphEntitiesCommand
from wdexp.wikidata.commands.category_detection_SPARQL import CategoryDetectionCommand
from wdexp.wikidata.commands.common_incoming_props_DUMP import CommonIncomingCommand
from wdexp.wikidata.commands.frequent_incoming_props_by_entity_JSON import FrequentIncomingPropsByEntityCommand


# property_counter = FrequencyPropertiesCommand(source_file="../../files/in/wikidata_slice.json",
# out_file="../files/out/brief_pro.txt")
#


# property_counter = FrequencyPropertiesCommand(source_file="C:\Users\Dani\Documents\EII\doctorado\datasets\wikidata\wikidata-all.json",
# out_file="../files/out/complete_fake.txt")
#
# property_counter.exec_command(string_return=False)


# aliases_tracker = AliasesPropertiesCommand(out_file="../files/out/complete_with_alias.txt",
# source_file="../files/out/complete.txt")
#
# aliases_tracker.exec_command(string_return=False)

# trends_tracker = TrackTrendsCommand(out_file="../files/out/complete_with_trends.json",
#                                     source_file="../files/out/complete_with_alias.txt")
# trends_tracker.exec_command()


# aol_counter = CountNgramsCommand(out_file_pattern="../files/out/aol_ngram_index.txt",
#                                  source_file="../files/in/consultas-AOL.txt",
#                                  min_n=1,
#                                  max_n=6)
# aol_counter.exec_command(1)
# aol_counter.exec_command(2)
# aol_counter.exec_command(3)
# aol_counter.exec_command(4)
# aol_counter.exec_command(5)
# aol_counter.exec_command(6)


# graph_builder = GraphEntitiesCommand(out_file="../files/out/complete_with_alias.txt",
#                                      source_file="../files/in/wikidata_slice.json")
# graph = graph_builder.exec_command(object_return=True)
#
# page_ranker = PageRankCommand(networkx_graph=graph, out_file="page_rank.txt")
# page_ranker.exec_command()


# page_rank_filter = PageRankFilterCommand(source_file="",
#                                          out_file="")
# page_rank_filter.exec_command()


# entity_properties_tracker = EntitiesPropertiesCommand(source_file="../files/in/filt_sort_pg_slice.json",
#                                                       out_file="../files/out/complete_top_pg_entities.json",
#                                                       number_of_entities=1000)
# entity_properties_tracker.exec_command()

# entity_pg_ranker = EntityRankerCommand(source_file="C:\\Users\\Dani\\Documents\\EII\\doctorado\\datasets\\filt_sort_page_rank.json",
#                                        out_file="../files/out/complete_top_pg_entities.json")
#
# print entity_pg_ranker._exec_command(string_return=True, entities=["Q319", "Q544", "Q2", "Q308", "Q313", "Q111", "Q193", "Q324", "Q332", "Q525"])



# subgrapher = SubgraphEntitiesCommand(out_file="out_graph.tsv", out_img="out_img.png")
# subgraph = subgrapher.exec_command(object_return=True, entities=['Q111'], file_return=True, img_return=False)


# categorizer = CategoryDetectionCommand(source_file="../files/out/complete_top_pg_entities.json",
#                                        out_file="../files/outcategorized_top_pg_entities.json")
# categorizer._exec_command()


# common_detector = CommonIncomingCommand(source_dump_file="../files/in/wikidata_slice.json",
#                                         source_target_ids_file="../files/in/filt_sort_pg_slice.json",
#                                         out_file="in_out_edges_ooo.json",
#                                         topk_target_entities=1000)
# common_detector._exec_command(string_return=False)


frequent_associations_detector = FrequentIncomingPropsByEntityCommand(source_file="C:\\Users\\Dani\\Documents\\EII\\doctorado\\datasets\\in_out_edges1000.json",
                                                                      out_file_entities="in_entities_500001.json",
                                                                      out_file_props="props_count_50000.json")
frequent_associations_detector.exec_command()


# aliases_tracker = AliasesPropertiesCommand(out_file="props_count_50000_described.json",
#                                            source_file="props_count_50000.json",
#                                            json_input=True)
#
# aliases_tracker.exec_command(string_return=False)





# repeated = {}
# existing = set()
#
# for line in open("out_graph.tsv"):
#     for piece in line[:-1].split("\t"):
#         if piece in existing:
#             if not piece in repeated:
#                 repeated[piece] = 1
#             repeated[piece] += 1
#         else:
#             existing.add(piece)
# print repeated
#
#
#
#
# print "Done!"
#
