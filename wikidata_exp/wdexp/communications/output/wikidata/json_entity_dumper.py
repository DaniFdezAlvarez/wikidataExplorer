__author__ = 'Dani'

from wikidata_exp.wdexp.communications.output.wikidata.interfaces import EntityDumper
import json

PERSIST_P_ID = "id"
PERSIST_P_LABEL = "label"
PERSIST_P_DESC = "description"
PERSIST_P_ALIASES = "aliases"
PERSIST_P_OUT_PROPS = "outcoming"
PERSIST_P_IN_PROPS = "incoming"
PERSIST_P_PG_SCORE = "pg_score"

P_ID = 0
P_LABEL = 1
P_DESC = 2
P_ALIASES = 3
P_OUT_PROPS = 4
P_IN_PROPS = 5
P_PG_SCORE = 6

_WHOLE_PROPS = [P_ID, P_LABEL, P_DESC, P_ALIASES, P_OUT_PROPS, P_IN_PROPS, P_PG_SCORE]



class JsonEntityDumper(EntityDumper):

    def __init__(self, out_file=None, needed_fields=None, indent=None, strict_mode=True, string_return=False):
        """
        needed_fields: list showing which fields of the property the dumper should care about.

        strict_mode : if strict mode is active, then if a received prop has none
        as value in some of the fields indicated in needed_fields, it will be
        included anyway in the result with an empty/None value. Otherwise, only
        non-empty / not None values will be persisted.

        :param out_file:
        :param needed_fields:
        :param indent:
        :param strict_mode:
        :return:
        """
        self._out_file = out_file
        self._indent = indent
        if needed_fields is None:
            needed_fields = _WHOLE_PROPS
        self._needed_fields = needed_fields
        self._strict_mode = strict_mode
        self._string_return = string_return


    def persist_entities(self, list_of_entities):
        result = []
        for a_prop in list_of_entities:
            result.append(self.json_of_entity(a_prop))
        if self._string_return:
            return json.dumps(result, indent=self._indent)
        else:
            with open(self._out_file, "w") as out_stream:
                json.dump(result, out_stream, indent=self._indent)


    def json_of_entity(self, an_entity):
        """
        It return a json_object with the representation of the received entity
        :param an_entity:
        :return:
        """
        result = {}
        for a_needed_field in self._needed_fields:
            self._include_field_in_result(result, an_entity, a_needed_field)
        return result


    def _include_field_in_result(self, result_dict, an_elem, a_field):
        if a_field == P_ID:
            self._include_id(result_dict, an_elem)
        elif a_field == P_LABEL:
            self._include_label(result_dict, an_elem)
        elif a_field == P_DESC:
            self._include_description(result_dict, an_elem)
        elif a_field == P_IN_PROPS:
            self._include_in_props(result_dict, an_elem)
        elif a_field == P_OUT_PROPS:
            self._include_out_props(result_dict, an_elem)
        elif a_field == P_ALIASES:
            self._include_aliases(result_dict, an_elem)
        elif a_field == P_PG_SCORE:
            self._include_pg_score(result_dict, an_elem)


    def _include_id(self, result_dict, an_elem):
        target_id = an_elem.id
        if target_id is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_ID] = an_elem.id

    def _include_label(self, result_dict, an_elem):
        target_label = an_elem.label
        if target_label is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_LABEL] = an_elem.label


    def _include_description(self, result_dict, an_elem):
        target_desc = an_elem.label
        if target_desc is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_DESC] = an_elem.description

    def _include_in_props(self, result_dict, an_elem):
        if an_elem.n_incoming_properties == 0 and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_IN_PROPS] = {}
            for an_edge in an_elem.distinct_incoming_properties_id:
                result_dict[PERSIST_P_IN_PROPS][an_edge] = an_elem.n_times_incoming_property(an_edge)

    def _include_out_props(self, result_dict, an_elem):
        if an_elem.n_outcoming_properties == 0 and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_OUT_PROPS] = {}
            for an_edge in an_elem.distinct_outcoming_properties_id:
                result_dict[PERSIST_P_OUT_PROPS][an_edge] = an_elem.n_times_incoming_property(an_edge)

    def _include_aliases(self, result_dict, an_elem):
        if an_elem.n_aliases == 0 and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_ALIASES] = []
            for an_alias in an_elem.aliases:
                result_dict[PERSIST_P_ALIASES].append(an_alias)


    def _include_pg_score(self, result_dict, an_elem):
        target_score = an_elem.pg_score
        if target_score is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_PG_SCORE] = an_elem.pg_score










