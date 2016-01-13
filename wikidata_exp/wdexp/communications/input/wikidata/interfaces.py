__author__ = 'Dani'


class TripleYielder(object):

    def yield_triples(self):
        """
        Generator that yields WikidataTriple objects
        :return:
        """
        raise NotImplementedError()

    def yield_entity_triples(self):
        """
        Generator that yields WikidataTriple objects where the object
        is always an entity
        :return:
        """
        raise NotImplementedError()

    def yield_literal_triples(self):
        """
        Generator that yields WikidataTriple objects where the object
        is always a literal
        :return:
        """
        raise NotImplementedError()



class EntityYielder(object):
    def yield_entities(self):
        """
        Generator that yields WikidataEntity objects
        :return:
        """
        raise NotImplementedError()



class PropertyYielder(object):
    def yield_properties(self):
        """
        Generator that yields WikidataProperty objects
        :return:
        """
        raise NotImplementedError()