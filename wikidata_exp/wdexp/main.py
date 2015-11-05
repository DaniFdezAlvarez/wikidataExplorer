__author__ = 'Dani'

from commands.frequency_properties import FrequencyProperties

# property_counter = FrequencyProperties(source_file="../files/in/wikidata_slice.json",
#                                        out_file="../files/out/brief_pro.txt")
#
property_counter = FrequencyProperties(source_file="C:\Users\Dani\Documents\EII\doctorado\datasets\wikidata\wikidata-all.json",
                                       out_file="../files/out/complete_fake.txt")

property_counter.exec_command(string_return=False)