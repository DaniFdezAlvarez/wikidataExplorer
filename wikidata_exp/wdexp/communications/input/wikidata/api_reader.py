__author__ = 'Dani'

from wdexp.communications.input.wikidata.interfaces import EntityTracker, PropertyTracker
from wdexp.model.wikidata import WikidataProperty, WikidataEntity
import requests
from requests.adapters import HTTPAdapter




_BASE_API_PROPERTIES = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&languages=en&format=json"


class WikidataApiReader(EntityTracker, PropertyTracker):


    def get_property(self, property_id):
        property_url = self._build_uri_of_property(property_id)  # Done
        json_property = self._get_json_of_property(property_url)  # Done

        return WikidataProperty(property_id=property_id,
                                label=self._get_prop_label(property_id, json_property),
                                aliases=self._get_prop_aliases(property_id, json_property),
                                description=self._get_prop_description(property_id, json_property))


    def yield_entities(self):
        pass

    @staticmethod
    def _build_uri_of_property(property_id):
        return _BASE_API_PROPERTIES.format(property_id)

    @staticmethod
    def _get_json_of_property(property_url):
        ses = requests.Session()
        ses.mount(property_url, HTTPAdapter(max_retries=10))
        json_content = requests.get(property_url).json()
        return json_content

    @staticmethod
    def _get_prop_aliases(prop_id, json_property):
        result = []
        target_dict = json_property['entities'][prop_id]['aliases']
        if 'en' in target_dict:
            for elem in target_dict['en']:
                result.append(elem['value'])
        return result

    @staticmethod
    def _get_prop_label(prop_id, json_property):
        result = None
        target_dict = json_property['entities'][prop_id]['labels']
        if 'en' in target_dict:
            result = target_dict['en']['value']
        return result

    @staticmethod
    def _get_prop_description(prop_id, json_property):
        result = None
        target_dict = json_property['entities'][prop_id]['descriptions']
        if 'en' in target_dict:
            result = target_dict['en']['value']
        return result
