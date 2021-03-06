__author__ = 'Dani'


from decimal import *

MIN_SCORE = Decimal('6.3750384049853736E-9')


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
            # a_str = in_stream.read()
            # a_str = re.sub("(u')|'", '"', a_str)
            # return json.loads(a_str)
            result = {}
            for a_tuple in self._read_key_values_in_chunks(in_stream, ","):
                result[a_tuple[0]] = a_tuple[1]
                print a_tuple[1]
            return result

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

    def _read_key_values_in_chunks(self, in_stream, break_char):
        previous_result = ""
        while True:
            data = in_stream.read(1024)
            if not data:
                break
            last_index = 0
            for i in range(0, len(data)):
                if data[i] == break_char:
                    yield self._extract_key_value_from_substring(previous_result + data[last_index:i + 1])
                    previous_result = ""
                    last_index = i + 1
            previous_result += data[last_index:]
        yield self._extract_key_value_from_substring(previous_result)



    def _extract_key_value_from_substring(self, target_str):
        first_index = None
        last_index = None
        colon_index = None
        i=0
        for char in target_str:
            if char == "'":
                if not first_index:
                    first_index = i
                else:
                    last_index = i
            if char == ":":
                colon_index = i
                break
            i += 1
        return target_str[first_index + 1:last_index], Decimal(target_str[colon_index + 2:-1])





