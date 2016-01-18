__author__ = 'Dani'
from decimal import *


class EntityRankerCommand(object):
    """
    Source file format: json01_wikidata

    """

    def __init__(self, source_file, out_file):
        self._in_file = source_file
        self._out_file = out_file

    def _exec_command(self, entities, string_return=False):
        rank = 0
        result = {}
        with open(self._in_file, "r") as in_stream:
            for an_id in self._read_ids_in_chunks(in_stream, ","):
                rank += 1
                if an_id[0] in entities:
                    result[an_id] = rank
                    entities.remove(an_id[0])
                    if len(entities) == 0:
                        break
        if string_return:
            return str(result)
        else:
            with open(self._out_file, "w") as out_stream:
                out_stream.write(str(result))


    def _read_ids_in_chunks(self, in_stream, break_char):
        previous_result = ""
        while True:
            data = in_stream.read(1024)
            if not data:
                break
            last_index = 0
            for i in range(0, len(data)):
                if data[i] == break_char:
                    yield self._extract_id_from_substring(previous_result + data[last_index:i + 1])
                    previous_result = ""
                    last_index = i + 1
            previous_result += data[last_index:]
        # yield self._extract_key_value_from_substring(previous_result)


    def _extract_id_from_substring(self, target_str):
        first_index = None
        last_index = None
        colon_index = None
        i = 0
        for char in target_str:
            if char == '"':

                if not first_index:
                    first_index = i
                else:
                    last_index = i
            if char == ":":
                colon_index = i
                break
            i += 1
        return target_str[first_index + 1:last_index], str(Decimal(target_str[colon_index + 2:-1]))


