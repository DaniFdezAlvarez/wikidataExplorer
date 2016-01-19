__author__ = 'Dani'

from wdexp.communications.input.wikidata.interfaces import PropertyTracker
from wdexp.model.wikidata import WikidataProperty


class Ccv01PropertiesParser(PropertyTracker):
    """
    FORMAT csv01

    Summary: lines using semicolon as separator. firts part, an id.
    Second part, count of apparitions (int)

    Exmaple:

    P31:88888
    P556:14
    ....

    """


    def __init__(self, source_file):
        self._in_file = source_file

    def yield_properties(self):
        with open(self._in_file, "r") as in_stream:
            for line in in_stream:
                splitted = line.split(" : ")
                if len(splitted) > 1:
                    yield WikidataProperty(property_id=splitted[0],
                                           n_appearances=int(splitted[0]))


