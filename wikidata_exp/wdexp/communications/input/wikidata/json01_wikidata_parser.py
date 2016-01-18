__author__ = 'Dani'

from wdexp.communications.input.wikidata.interfaces import IdTracker
from decimal import *



class Json01WikidataParser(IdTracker):
    """
    FORMAT JSON01:

    Summary: It consist of a dict with a depth of 1. The keys are wikidata IDs
    and the values of those keys are numbers (float).

    The strings of the JSON should be quoted with the char " and the JSON
    should be well formated, since this module does not use a JSON library,
    but a faster plain text (structured) processor

    Example:

    {
        "Q4167836": 0.12757293940694778,
	    "Q4167410": 0.048518222496095886,
	    "Q5": 0.04803422148902256,
	    "Q16521": 0.04055021999515414,
	    "Q7432": 0.033999504701633765,
        ...
    }
    

    """

    def __init__(self, source_file, break_char):
        self._in_file = source_file
        self._break_char = break_char


    def yield_entity_ids(self):
        with open(self._in_file, "r") as in_stream:
            previous_result = ""
            while True:
                data = in_stream.read(1024)
                if not data:
                    break
                last_index = 0
                for i in range(0, len(data)):
                    if data[i] == self._break_char:
                        yield self._extract_id_from_substring(previous_result + data[last_index:i + 1])
                        previous_result = ""
                        last_index = i + 1
                previous_result += data[last_index:]


    @staticmethod
    def _extract_id_from_substring(target_str):
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
