# coding=utf-8
__author__ = 'Dani'

PROP_TRENDS = "trends"
DOWNLOAD_PATH = "C:\\Users\\Dani\\repos_git\\wikidata_exp\\wikidata_exp\\files\\downloads\\g_trends"

import json
import traceback
import time
from os import walk
from os import remove
from os.path import isfile
from os.path import join
from wdexp.wikidata.commands.aliases_properties_API import PROP_LABEL, PROP_ALIASES
from wdexp.g_trends.g_trends_scraper import GTrendsScrapper


class TrackTrendsCommand(object):

    def __init__(self, source_file, out_file):

        self._in_file = source_file
        self._out_file = out_file
        self._trends_cache = {}


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

        #descargar
        #leer e introducir, en bucle
        #borrar

    def _get_trends_of_label(self, a_label):
        if a_label in self._trends_cache:
            return self._trends_cache[a_label]
        self._download_trend_file(a_label)
        target_path, trend_raw_content = self._read_trend_file()
        trend_list = self._parse_trend_content(trend_raw_content)
        self._delete_trend_file(target_path)
        time.sleep(2.5)
        return trend_list

    @staticmethod
    def _download_trend_file(term):
        GTrendsScrapper.download_page_or_term(term)

    @staticmethod
    def _read_trend_file():
        a_path = None
        start_time = time.time()
        while a_path is None:
            current_state = time.time()
            if current_state - start_time > 30:
                raise ValueError("Are we banned? Stop")
            for base_path, ignore_this, the_files_array in walk(DOWNLOAD_PATH):
                if len(the_files_array) > 0:
                    candidate_path = join(base_path, the_files_array[0])
                    if isfile(candidate_path) and candidate_path.endswith(".csv"):
                        a_path = join(base_path, the_files_array[0])
        time.sleep(1)
        in_stream = open(a_path, "r")
        result = in_stream.read()
        in_stream.close()
        return a_path, result


    @staticmethod
    def _parse_trend_content(raw_content):
        result = []
        lines_array = raw_content.split("\n")
        tracking_mode = False
        for a_line in lines_array:
            if tracking_mode:
                if a_line not in ["", "\r"]:
                    result.append((a_line.split(",")[0]).strip())
                else:
                    break
            elif a_line.startswith("Búsquedas principales de"):
                tracking_mode = True
        return result

    @staticmethod
    def _delete_trend_file(target_path):
        remove(target_path)





