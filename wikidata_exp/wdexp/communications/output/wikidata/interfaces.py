__author__ = 'Dani'


class EntityDumper(object):

    def persist_entities(self, list_of_entities):
        """
        It receives a list of entities and persist it

        :param list_of_entities:
        :return:
        """
        raise NotImplementedError()


    def persist_entities_callback(self, generator_method):
        """

        It receives a method that will yield entities, and it will persist
        all the generated elements

        :param generator_method:
        :return:
        """
        raise NotImplementedError()


class PropertyDumper(object):

    def persist_properties(self, list_of_properties):
        """
        It receives a list of properties and persist it

        :param list_of_properties:
        :return:
        """
        raise NotImplementedError()


    def persist_properties_callback(self, generator_method):
        """

        It receives a method that will yield properties, and it will persist
        all the generated elements

        :param generator_method:
        :return:
        """
        raise NotImplementedError()