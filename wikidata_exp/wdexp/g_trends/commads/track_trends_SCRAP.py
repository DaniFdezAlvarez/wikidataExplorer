# coding=utf-8
__author__ = 'Dani'

PROP_TRENDS = "trends"



import json
import traceback

from wdexp.wikidata.commands.aliases_properties_API import PROP_LABEL, PROP_ALIASES
from wdexp.g_trends.g_trends_scraper import GTrendsScrapper


class TrackTrendsCommand(object):

    def __init__(self, source_file, out_file):

        self._in_file = source_file
        self._out_file = out_file
        self._scraper = GTrendsScrapper()


    def exec_command(self, string_return=False):
        whole_json_source = self._read_in_json()
        count = 0
        try:
            for a_dict in whole_json_source:
                count += 1
                print "Procesing", a_dict[PROP_LABEL], "...............", count
                self._complete_json_with_trends(a_dict)
        except:
            traceback.print_exc()
        if string_return:
            return json.dumps(whole_json_source, indent=4, encoding='utf-8')
        else:
            with open(self._out_file, "w") as out_stream:
                json.dump(whole_json_source, out_stream, indent=4, encoding='utf-8')


    def _read_in_json(self):
        with open(self._in_file, 'r') as in_stream:
            return json.load(in_stream)


    def _complete_json_with_trends(self, a_dict):
        a_dict[PROP_TRENDS] = {}
        a_dict[PROP_TRENDS][a_dict[PROP_LABEL]] = self._get_trends_of_label(a_dict[PROP_LABEL])
        print "Label done..."
        for an_alias in a_dict[PROP_ALIASES]:
            a_dict[PROP_TRENDS][an_alias] = self._get_trends_of_label(an_alias)
            print "An alias done...", an_alias
        return a_dict  # In fact, not necessary. im modifying the received one


    def _get_trends_of_label(self, a_label):
        return self._scraper.get_trends_of_label(a_label)








