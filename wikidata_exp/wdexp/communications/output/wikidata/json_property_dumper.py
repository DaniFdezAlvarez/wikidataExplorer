__author__ = 'Dani'

from wdexp.communications.output.wikidata.interfaces import PropertyDumper
import json

PERSIST_P_ID = "id"
PERSIST_P_LABEL = "label"
PERSIST_P_DESC = "description"
PERSIST_P_TRENDS = "trends"
PERSIST_P_OUT_PROPS = "outcoming"
PERSIST_P_IN_PROPS = "incoming"
PERSIST_P_APPEARANCES = "count"
PERSIST_P_RANK = "rank"

P_ID = 0
P_LABEL = 1
P_DESC = 2
P_TRENDS = 3
P_OUT_PROPS = 4
P_IN_PROPS = 5
P_APPEARANCES = 6
P_RANK = 7

_WHOLE_PROPS = [P_ID, P_LABEL, P_DESC, P_TRENDS, P_OUT_PROPS, P_IN_PROPS, P_APPEARANCES, P_RANK]



class JsonPropertyDumper(PropertyDumper):

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


    def persist_properties(self, list_of_properties):
        result = []
        for a_prop in list_of_properties:
            result.append(self._json_of_property(a_prop))
        if self._string_return:
            return json.dumps(result, indent=self._indent)
        else:
            with open(self._out_file, "w") as out_stream:
                json.dump(result, out_stream, indent=self._indent)


    def _json_of_property(self, a_prop):
        result = {}
        for a_needed_field in self._needed_fields:
            self._include_field_in_result(result, a_prop, a_needed_field)
        return result


    def _include_field_in_result(self, result_dict, a_prop, a_field):
        if a_field == P_ID:
            self._include_id(result_dict, a_prop)
        elif a_field == P_LABEL:
            self._include_label(result_dict, a_prop)
        elif a_field == P_APPEARANCES:
            self._include_appearances(result_dict, a_prop)
        elif a_field == P_DESC:
            self._include_description(result_dict, a_prop)
        elif a_field == P_IN_PROPS:
            self._include_in_props(result_dict, a_prop)
        elif a_field == P_OUT_PROPS:
            self._include_out_props(result_dict, a_prop)
        elif a_field == P_TRENDS:
            self._include_trends(result_dict, a_prop)
        elif a_field == P_RANK:
            self._include_rank(result_dict, a_prop)


    def _include_id(self, result_dict, a_prop):
        target_id = a_prop.id
        if target_id is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_ID] = a_prop.id

    def _include_label(self, result_dict, a_prop):
        target_label = a_prop.label
        if target_label is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_LABEL] = a_prop.label

    def _include_appearances(self, result_dict, a_prop):
        target_apps = a_prop.label
        if target_apps is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_APPEARANCES] = a_prop.n_appearances

    def _include_description(self, result_dict, a_prop):
        target_desc = a_prop.label
        if target_desc is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_DESC] = a_prop.description

    def _include_in_props(self, result_dict, a_prop):
        if a_prop.n_incoming_properties == 0 and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_IN_PROPS] = {}
            for an_edge in a_prop.distinct_incoming_properties_id:
                result_dict[PERSIST_P_IN_PROPS][an_edge] = a_prop.n_times_incoming_property(an_edge)

    def _include_out_props(self, result_dict, a_prop):
        if a_prop.n_outcoming_properties == 0 and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_OUT_PROPS] = {}
            for an_edge in a_prop.distinct_outcoming_properties_id:
                result_dict[PERSIST_P_OUT_PROPS][an_edge] = a_prop.n_times_incoming_property(an_edge)

    def _include_trends(self, result_dict, a_prop):
        pass  # TODO

    def _include_rank(self, result_dict, a_prop):
        target_rank = a_prop.rank
        if target_rank is None and not self._strict_mode:
            return
        else:
            result_dict[PERSIST_P_RANK] = a_prop.rank










