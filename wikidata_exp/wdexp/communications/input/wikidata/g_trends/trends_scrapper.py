# coding=utf-8
__author__ = 'Dani'

import webbrowser
import urllib2

import time
from os import walk
from os import remove
from os.path import isfile
from os.path import join
import random

DOWNLOAD_PATH = "C:\\Users\\Dani\\repos_git\\wikidata_exp\\wikidata_exp\\files\\downloads\\g_trends"
SLEEP_AVERAGE_TIME = 17

_URL_START = "http://www.google.com/trends/trendsReport?&q="
_URL_END = "&cmpt=q&content=1&export=1"


class GTrendsScrapper(object):

    def __init__(self):
        self._trends_cache = {}


    def complete_property_with_trends(self, a_property):
        for a_trend in self._get_trends_of_label(a_property.label):
            a_property.add_trend(a_trend)
        return a_property  # In fact, we are modifying the received object. Anyway, the return does not disturb


    def _get_trends_of_label(self, a_label):
        if a_label in self._trends_cache:
            return self._trends_cache[a_label]
        GTrendsScrapper._download_trend_file(a_label)
        target_path, trend_raw_content = GTrendsScrapper._read_trend_file()
        trend_list = GTrendsScrapper._parse_trend_content(trend_raw_content)
        self._trends_cache[a_label] = trend_list
        GTrendsScrapper._delete_trend_file(target_path)
        GTrendsScrapper._random_wait()
        return trend_list

    @staticmethod
    def _download_page_of_term(term):
        url = GTrendsScrapper._build_url_to_scrap(term)
        webbrowser.open(url)


    @staticmethod
    def _build_url_to_scrap(term):
        return _URL_START + urllib2.quote(term) + _URL_END


    @staticmethod
    def _random_wait():
        time.sleep(SLEEP_AVERAGE_TIME + random.randint(-10, 10))

    @staticmethod
    def _download_trend_file(term):
        GTrendsScrapper._download_page_of_term(term)

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