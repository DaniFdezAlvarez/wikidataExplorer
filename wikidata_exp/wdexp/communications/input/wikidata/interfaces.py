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


    def yield_incoming_triples(self, entity_id, limit=None):
        """
        Yields the triples that has entity_id as object.
        If limit is None, it yields every existing triple.
        Otherwise, yields triples until the number specified
        in limit is reached.
        :param entity_id:
        :return:
        """
        raise NotImplementedError()

    def yield_outcoming_triples(self, entity_id, limit=None):
        """
        Yields the triples that has entity_id as subject.
        If limit is None, it yields every existing triple.
        Otherwise, yields triples until the number specified
        in limit is reached.
        :param entity_id:
        :return:
        """
        raise NotImplementedError()

    def yield_subgraph_triples(self, entity_id, limit=None):
        """
        Yields the triples that has entity_id as object.
        If limit is None, it yields every existing triple.
        Otherwise, yields triples until the number specified
        in limit is reached.
        :param entity_id:
        :return:
        """
        raise NotImplementedError()


    def yield_instances_of_entity(self, entity_id, limit=None):
        """
        It yields entity ids that are subjects in triples such as
        (result instanceof entity_id)
        :param entity_id:
        :param limit:
        :return:
        """
        raise NotImplementedError()

    def yield_classes_of_entity(self, entity_id, limit=None):
        """
        It yields entity ids that are objects in triples such as
        (entity_id instanceof result)

        :param entity_id:
        :param limit:
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


class IdTracker(object):

    def yield_entity_ids(self):
        """
        It yields string ids of wikidata entities
        :return:
        """
        raise NotImplementedError()

    def yield_property_ids(self):
        """
        It yields string ids of wikidata properties
        :return:
        """
        raise NotImplementedError()