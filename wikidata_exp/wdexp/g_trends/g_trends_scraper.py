__author__ = 'Dani'

import webbrowser
import urllib2

_URL_START = "http://www.google.com/trends/trendsReport?&q="
_URL_END = "&cmpt=q&content=1&export=1"


class GTrendsScrapper:
    def __init__(self):
        pass

    @staticmethod
    def download_page_or_term(term):
        url = GTrendsScrapper._build_url_to_scrap(term)
        webbrowser.open(url)


    @staticmethod
    def _build_url_to_scrap(term):
        return _URL_START + urllib2.quote(term) + _URL_END
