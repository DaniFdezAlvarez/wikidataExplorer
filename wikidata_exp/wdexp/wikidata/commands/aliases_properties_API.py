__author__ = 'Dani'

from wdexp.communications.input.wikidata.csv01_property_parser import Ccv01PropertiesParser
from wdexp.communications.input.wikidata.json03_properties_parser import Json03PropertyParser
from wdexp.communications.input.wikidata.api_reader import WikidataApiReader
from wdexp.communications.output.wikidata.json_property_dumper import JsonPropertyDumper, P_ID, P_LABEL, P_APPEARANCES, P_DESC


class AliasesPropertiesCommand(object):
    def __init__(self, source_file, out_file, json_input=False):
        self._in_file = source_file
        self._out_file = out_file
        self._is_json_input = json_input
        self._api_reader = WikidataApiReader()


    def exec_command(self, string_return=False):
        sorted_result_list = []
        for a_property in self._read_target_properties():
            try:
                sorted_result_list.append(self._get_complete_property(a_property))
            except:
                print "Error with property " + str(a_property)
        return JsonPropertyDumper(out_file=self._out_file,
                                  indent=4,
                                  strict_mode=True,
                                  string_return=string_return,
                                  needed_fields=[P_ID, P_LABEL, P_APPEARANCES, P_DESC]).\
            persist_properties(sorted_result_list)


    def _read_target_properties(self):
        if not self._is_json_input:
            for a_prop in Ccv01PropertiesParser(source_file=self._in_file).yield_properties():
                yield a_prop
        else:
            for a_prop in Json03PropertyParser(source_file=self._in_file).yield_properties():
                yield a_prop


    def _get_complete_property(self, anemic_property):
        return self._api_reader.get_property(anemic_property.id)




