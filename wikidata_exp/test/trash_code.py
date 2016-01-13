__author__ = 'Dani'

from wdexp.communications.input.wikidata.dump_parser import WikidataDumpParser


parser = WikidataDumpParser(source_file="../files/in/wikidata_slice.json")

for triple in parser.yield_entity_triples():
    print triple
    print triple.subject.label
    print triple.subject.description
    for an_alias in triple.subject.aliases:
        print ".", an_alias
    print "--------"