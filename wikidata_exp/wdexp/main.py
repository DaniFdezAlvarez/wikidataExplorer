__author__ = 'Dani'

from wdexp.wikidata.commands.aliases_properties_API import AliasesPropertiesCommand
from wdexp.aol.commands.count_ngrams_DUMP import CountNgramsCommand
from wdexp.g_trends.commads.track_trends_SCRAP import TrackTrendsCommand
from wdexp.wikidata.commands.graph_entities_DUMP import GraphEntitiesCommand
from wdexp.wikidata.commands.page_rank_NETG import PageRankCommand

# property_counter = FrequencyPropertiesCommand(source_file="../../files/in/wikidata_slice.json",
# out_file="../files/out/brief_pro.txt")
#


# property_counter = FrequencyPropertiesCommand(source_file="C:\Users\Dani\Documents\EII\doctorado\datasets\wikidata\wikidata-all.json",
# out_file="../files/out/complete_fake.txt")
#
# property_counter.exec_command(string_return=False)


# aliases_tracker = AliasesPropertiesCommand(out_file="../files/out/complete_with_alias.txt",
#                                            source_file="../files/out/complete.txt")
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


graph_builder = GraphEntitiesCommand(out_file="../files/out/complete_with_alias.txt",
                                     source_file="../files/in/wikidata_slice.json")
graph = graph_builder.exec_command(object_return=True)

page_ranker = PageRankCommand(networkx_graph=graph, out_file="page_rank.txt")
page_ranker.exec_command()

print "Done!"

