__author__ = 'Dani'

import re

PATTERN_WHITES = re.compile('[ \t\r\n]+')


class CountNgramsCommand(object):

    def __init__(self, source_file, out_file_pattern, min_n, max_n):
        self._in_file = source_file
        self._out_file_pattern = out_file_pattern
        self._min_n = min_n
        self._max_n = max_n
        self._indexes = {}
        self._initialize_indexes()

    def _initialize_indexes(self):
        for i in range(self._min_n, self._max_n):
            self._indexes[i] = {}


    def exec_command(self, string_return=False):
        self._process_in_file()
        if string_return:
            result = ""
            for an_index in self._indexes:
                relative_result = "\n\nResults for n = {}".format(an_index)
                sorted_list_ngrams = self._dictionary_to_sorted_list_of_keys(self._indexes[an_index])
                for a_ngram in sorted_list_ngrams:
                    relative_result += "{}:{}\n".format(a_ngram, self._indexes[an_index][a_ngram])
                result += relative_result
            return result
        else:
            for an_index in self._indexes:
                self._write_index_to_file(an_index)


    def _process_in_file(self):
        counter = 0
        with open(self._in_file, "r") as in_stream:
            for line in in_stream:
                counter += 1
                if counter % 100000 == 0:
                    print "Llevo", counter
                pieces = line.split("\t")
                frequency = int(pieces[0].strip())
                tokens = self._normalize(pieces[1]).split(" ")
                for ngram_size in range(self._min_n, self._max_n + 1):
                    sequences = self._extract_ngram_sequences(tokens, ngram_size)
                    for sequence in sequences:
                        if sequence not in self._indexes[ngram_size]:
                            self._indexes[ngram_size][sequence] = 0
                        self._indexes[ngram_size][sequence] += frequency

    @staticmethod
    def _extract_ngram_sequences(tokens, ngram_size):

        if ngram_size > len(tokens):
            pass  # Same as empty list, but this method yields
        else:
            for i in range(0, len(tokens) - ngram_size + 1):
                yield " ".join(tokens[0 + i:ngram_size + i])

    @staticmethod
    def _normalize(target_text):
        result = re.sub(PATTERN_WHITES, " ", target_text).strip()  # Remove redundant whites
        return result.lower()

    @staticmethod
    def _dictionary_to_sorted_list_of_keys(an_index):
        return sorted(an_index, key=an_index.get, reverse=True)

    def _write_index_to_file(self, an_index_key):
        target_file = self._build_path_to_out_index_file(an_index_key)
        sorted_list_ngrams = self._dictionary_to_sorted_list_of_keys(self._indexes[an_index_key])
        with open(target_file, "w") as out_stream:
            for a_ngram in sorted_list_ngrams:
                out_stream.write("{}:{}\n".format(a_ngram, self._indexes[an_index_key][a_ngram]))


    def _build_path_to_out_index_file(self, an_index_key):
        if "." not in self._out_file_pattern:
            return self._out_file_pattern + str(an_index_key)
        else:
            last_dot_index = [m.start() for m in re.finditer("\.", self._out_file_pattern)][-1]
            if last_dot_index != 0 and self._out_file_pattern[last_dot_index - 1] != ".":
                return self._out_file_pattern[:last_dot_index] \
                       + str(an_index_key) + self._out_file_pattern[last_dot_index:]
            else:
                return self._out_file_pattern + str(an_index_key)



