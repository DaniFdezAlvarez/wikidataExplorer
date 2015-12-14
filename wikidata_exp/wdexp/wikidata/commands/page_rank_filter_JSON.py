__author__ = 'Dani'

import json

MIN_SCORE = 6.37503840499e-09


class PageRankFilterCommand(object):


    def __init__(self, source_file, out_file):
        self._in_file = source_file
        self._out_file = out_file


    def exec_command(self, string_return=False):
        target_dict = self._read_in_file()
        result_tuples = self._filter_and_sort_dcit(target_dict)
        target_dict = None  # Free memory
        str_result = self._turn_list_tuples_into_str_json(result_tuples)
        if string_return:
            return str_result
        else:
            with open(self._out_file, "w") as out_stream:
                out_stream.write(str_result)


    def _read_in_file(self):
        with open(self._in_file, "r") as in_stream:
            return json.load(in_stream)

    def _filter_and_sort_dcit(self, a_dict):
        result = []
        for a_key in a_dict:
            if a_dict[a_key] > MIN_SCORE:
                result.append((a_key, a_dict[a_key]))
        print len(a_dict), len(result)
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def _turn_list_tuples_into_str_json(self, list_tuples):
        result = "{"
        result += "\n\t\"" + list_tuples[0][0] + "\": " + str(list_tuples[0][1])
        for a_tuple in list_tuples[1:]:
            result += ",\n\t\"" + a_tuple[0] + "\": " + str(a_tuple[1])
        result += "\n}"
        return result



