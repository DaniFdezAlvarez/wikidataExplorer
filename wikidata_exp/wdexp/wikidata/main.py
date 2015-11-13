__author__ = 'Dani'

from wdexp.wikidata.commands.aliases_properties_API import AliasesPropertiesCommand
from wdexp.g_trends.commads.track_trends_SCRAP import TrackTrendsCommand

# property_counter = FrequencyPropertiesCommand(source_file="../../files/in/wikidata_slice.json",
#                                        out_file="../../files/out/brief_pro.txt")
#


# property_counter = FrequencyPropertiesCommand(source_file="C:\Users\Dani\Documents\EII\doctorado\datasets\wikidata\wikidata-all.json",
#                                        out_file="../../files/out/complete_fake.txt")
#
# property_counter.exec_command(string_return=False)


# aliases_tracker = AliasesPropertiesCommand(out_file="../../files/out/complete_with_alias.txt",
#                                            source_file="../../files/out/complete.txt")
#
# aliases_tracker.exec_command(string_return=False)

trends_tracker = TrackTrendsCommand(out_file="../../files/out/complete_with_trends.json",
                                    source_file="../../files/out/complete_with_alias.txt")
trends_tracker.exec_command()

print "Done!"

