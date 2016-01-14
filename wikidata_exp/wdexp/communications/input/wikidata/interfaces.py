__author__ = 'Dani'


class TripleTracker(object):

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



class EntityTracker(object):

    def yield_entities(self):
        """
        Generator that yields WikidataEntity objects
        :return:
        """
        raise NotImplementedError()

    def get_entity(self, entity_id):
        """
        It returns a WikidataEntity object with id entity_id
        :param entity_id:
        :return:
        """
        raise NotImplementedError()



class ElementTracker(object):

    def yield_elements(self):
        """
        Generator that yields WikidataProperty or WikidataEntity objects
        :return:
        """
        raise NotImplementedError()



class PropertyTracker(object):

    def yield_properties(self):
        """
        Generator that yields WikidataProperty objects
        :return:
        """
        raise NotImplementedError()

    def get_property(self, property_id):
        """
        It returns a WikidataProperty object with ID property_id
        :param property_id:
        :return:
        """
        raise NotImplementedError()