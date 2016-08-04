import requests
from requests.adapters import HTTPAdapter

from wikidata_exp.wdexp.communications.input.wikidata.interfaces import EntityTracker, PropertyTracker
from wikidata_exp.wdexp.model.wikidata import WikidataEntity, WikidataProperty

__author__ = 'Dani'




_BASE_API = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids={}&languages=en&format=json"


class WikidataApiReader(EntityTracker, PropertyTracker):
    def get_entity(self, entity_id):
        entity_url = self._build_uri_of_elem(entity_id)
        json_entity = self._get_json_of_elem(entity_url)
        return WikidataEntity(entity_id=entity_id,
                              label=self._get_elem_label(entity_id, json_entity),
                              aliases=self._get_elem_aliases(entity_id, json_entity),
                              description=self._get_elem_description(entity_id, json_entity))



    def get_property(self, property_id):
        property_url = self._build_uri_of_elem(property_id)  # Done
        json_property = self._get_json_of_elem(property_url)  # Done

        return WikidataProperty(property_id=property_id,
                                label=self._get_elem_label(property_id, json_property),
                                aliases=self._get_elem_aliases(property_id, json_property),
                                description=self._get_elem_description(property_id, json_property))


    @staticmethod
    def _build_uri_of_elem(property_id):
        return _BASE_API.format(property_id)

    @staticmethod
    def _get_json_of_elem(property_url):
        ses = requests.Session()
        ses.mount(property_url, HTTPAdapter(max_retries=10))
        json_content = requests.get(property_url).json()
        return json_content

    @staticmethod
    def _get_elem_aliases(prop_id, json_property):
        result = []
        target_dict = json_property['entities'][prop_id]['aliases']
        if 'en' in target_dict:
            for elem in target_dict['en']:
                result.append(elem['value'])
        return result

    @staticmethod
    def _get_elem_label(prop_id, json_property):
        result = None
        target_dict = json_property['entities'][prop_id]['labels']
        if 'en' in target_dict:
            result = target_dict['en']['value']
        return result

    @staticmethod
    def _get_elem_description(prop_id, json_property):
        result = None
        target_dict = json_property['entities'][prop_id]['descriptions']
        if 'en' in target_dict:
            result = target_dict['en']['value']
        return result
