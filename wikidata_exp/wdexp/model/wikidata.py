__author__ = 'Dani'



class WikidataEntity(object):

    def __init__(self, entity_id, label=None, description=None, aliases=None,
                 outcoming_properties_id=None, incoming_properties_id=None, pg_score=None):
        self._id = entity_id
        self._label = label
        self._description = description
        if aliases is None:
            aliases = []
        self._aliases = aliases
        if outcoming_properties_id is None:  # Dict with key (id_property) and id (number of times)
            outcoming_properties_id = {}
        self._out_prop = outcoming_properties_id
        if incoming_properties_id is None:
            incoming_properties_id = {}
        self._in_prop = incoming_properties_id
        self._pg_score = pg_score


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
            for i in range(0, self._out_prop):
                yield a_prop

    @property
    def n_outcoming_properties(self):
        result = 0
        for a_prop in self._out_prop:
            result += self._out_prop[a_prop]
        return result

    @property
    def distinct_outcoming_properties_id(self):
        for a_prop in self._out_prop:
            yield a_prop

    @property
    def n_distinct_outcoming_properties_id(self):
        return len(self._out_prop)


    @property
    def incoming_properties_id(self):
        for a_prop in self._in_prop:
            for i in range(0, self._in_prop):
                yield a_prop

    @property
    def n_incoming_properties(self):
        result = 0
        for a_prop in self._in_prop:
            result += self._in_prop[a_prop]
        return result

    @property
    def distinct_incoming_properties_id(self):
        for a_prop in self._in_prop:
            yield a_prop

    @property
    def n_distinct_incoming_properties_id(self):
        return len(self._in_prop)

    @property
    def pg_score(self):
        return self._pg_score

    @pg_score.setter
    def pg_score(self, value):
        self._pg_score = value


    def n_times_incoming_property(self, a_prop):
        if a_prop in self._in_prop:
            return self._in_prop[a_prop]
        else:
            return 0

    def n_times_outcoming_prop(self, a_prop):
        if a_prop in self._out_prop:
            return self._out_prop[a_prop]
        else:
            return 0




class WikidataProperty(object):

    def __init__(self, property_id, label=None, description=None, aliases=None, trends=None,
                 outcoming_properties_id=None, incoming_properties_id=None, n_appearances=None, rank=None):
        self._id = property_id
        self._label = label
        self._description = description
        if aliases is None:
            aliases = []
        self._aliases = aliases
        if trends is None:
            trends = []
        self._trends = trends
        if outcoming_properties_id is None:  # Dict with key (id_property) and id (number of times)
            outcoming_properties_id = {}
        self._out_prop = outcoming_properties_id
        if incoming_properties_id is None:
            incoming_properties_id = {}
        self._in_prop = incoming_properties_id
        self._n_appearances = n_appearances
        self._rank = rank


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

    def add_trend(self, a_trend):
        self._trends.append(a_trend)

    @property
    def n_trends(self):
        return len(self._trends)


    @property
    def outcoming_properties_id(self):
        for a_prop in self._out_prop:
            for i in range(0, self._out_prop):
                yield a_prop

    @property
    def n_outcoming_properties(self):
        result = 0
        for a_prop in self._out_prop:
            result += self._out_prop[a_prop]
        return result

    @property
    def distinct_outcoming_properties_id(self):
        for a_prop in self._out_prop:
            yield a_prop

    @property
    def n_distinct_outcoming_properties_id(self):
        return len(self._out_prop)


    @property
    def incoming_properties_id(self):
        for a_prop in self._in_prop:
            for i in range(0, self._in_prop):
                yield a_prop

    @property
    def n_incoming_properties(self):
        result = 0
        for a_prop in self._in_prop:
            result += self._in_prop[a_prop]
        return result

    @property
    def distinct_incoming_properties_id(self):
        for a_prop in self._in_prop:
            yield a_prop

    @property
    def n_distinct_incoming_properties_id(self):
        return len(self._in_prop)


    @property
    def n_appearances(self):
        return self._n_appearances

    @n_appearances.setter
    def n_appearances(self, value):
        self._n_appearances = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = value


    def n_times_incoming_property(self, a_prop):
        if a_prop in self._in_prop:
            return self._in_prop[a_prop]
        else:
            return 0

    def n_times_outcoming_prop(self, a_prop):
        if a_prop in self._out_prop:
            return self._out_prop[a_prop]
        else:
            return 0


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


