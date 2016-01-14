__author__ = 'Dani'



class WikidataEntity(object):

    def __init__(self, entity_id, label=None, description=None, aliases=None, outcoming_properties_id=None):
        self._id = entity_id
        self._label = label
        self._description = description
        if aliases is None:
            aliases = []
        self._aliases = aliases
        if outcoming_properties_id is None:
            outcoming_properties_id = []
        self._out_prop = outcoming_properties_id


    def __str__(self):
        return self._id

    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label

    @property
    def description(self):
        return self._description

    @property
    def aliases(self):
        for an_alias in self._aliases:
            yield an_alias

    @property
    def n_aliases(self):
        return len(self._aliases)

    @property
    def outcoming_properties_id(self):
        for a_prop in self._out_prop:
            yield a_prop

    @property
    def n_outcoming_properties(self):
        return len(self._out_prop)




class WikidataProperty(object):

    def __init__(self, property_id, label=None, description=None, aliases=None, trends=None,
                 outcoming_properties_id=None, n_appearances=None):
        self._id = property_id
        self._label = label
        self._description = description
        if aliases is None:
            aliases = []
        self._aliases = aliases
        if trends is None:
            trends = []
        self._trends = trends
        if outcoming_properties_id is None:
            outcoming_properties_id = []
        self._out_prop = outcoming_properties_id
        self._n_appearances = n_appearances


    def __str__(self):
        return self._id


    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label

    @property
    def description(self):
        return self._description

    @property
    def aliases(self):
        for an_alias in self._aliases:
            yield an_alias

    @property
    def n_aliases(self):
        return len(self._aliases)


    @property
    def trends(self):
        for a_trend in self._trends:
            yield a_trend

    @property
    def n_trends(self):
        return len(self._trends)


    @property
    def outcoming_properties_id(self):
        for a_prop in self._out_prop:
            yield a_prop

    @property
    def n_outcoming_properties(self):
        return len(self._out_prop)

    @property
    def n_appearances(self):
        return self._n_appearances


##### LITERAL_TYPES

TYPE_UNKOWN = -1
TYPE_NUMBER = 0
TYPE_STRING = 1


class WikidataLiteral(object):

    def __init__(self, value, literal_type=None):
        self._value = value
        self._type = literal_type

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    def __str__(self):
        return str(self._value)



class WikidataTriple(object):

    def __init__(self, subject, predicate, target_object):
        self._subject = subject
        self._predicate = predicate
        self._object = target_object


    @property
    def subject(self):
        return self._subject


    @property
    def predicate(self):
        return self._predicate

    @property
    def object(self):
        return self._object

    def __str__(self):
        return str(self.subject) + ", " + str(self._predicate) + ", " + str(self.object)


