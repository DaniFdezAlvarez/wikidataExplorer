__author__ = 'Dani'

from wdexp.communications.input.wikidata.dump_parser import WikidataDumpParser


parser = WikidataDumpParser(source_file="../files/in/wikidata_slice.json")
#
# for triple in parser.yield_entity_triples():
#     print triple
#     print triple.subject.label
#     print triple.subject.description
#     for an_alias in triple.subject.aliases:
#         print ".", an_alias
#     print "--------"


for elem in parser.yield_elements():
    print elem, elem.n_outcoming_properties
    for a_prop in elem.outcoming_properties_id:
        print "----", a_prop
