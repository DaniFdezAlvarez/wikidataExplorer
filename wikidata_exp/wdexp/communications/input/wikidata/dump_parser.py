__author__ = 'Dani'
import ijson

from wdexp.communications.input.wikidata.interfaces import ElementYielder, TripleYielder
from wdexp.model.wikidata import WikidataEntity, WikidataProperty, WikidataTriple


class WikidataDumpParser(ElementYielder, TripleYielder):
    def __init__(self, source_file):
        self._in_file = source_file


    def yield_entity_triples(self):
        json_stream = open(self._in_file, "r")
        elem_id = None
        elem_type = None
        desc_en = None
        label_en = None
        datatype = None
        datavalue_type = None
        current_claim_key = None
        datavalue_num_id = None
        possible_edges = []
        aliases_en = []

        elem_count = 1

        for prefix, event, value in ijson.parse(json_stream):
            if event == 'end_map':
                if prefix == 'item':
                    for tuple_4 in possible_edges:
                        if self._is_valid_entity_edge(elem_type, tuple_4[0],
                                                      tuple_4[1]):  # triple: datatype, datavalue_type, datavalue_num_id
                            yield WikidataTriple(subject=WikidataEntity(entity_id=elem_id,
                                                                        label=label_en,
                                                                        description=desc_en,
                                                                        aliases=aliases_en),
                                                 predicate=WikidataProperty(property_id=tuple_4[2]),
                                                 target_object=WikidataEntity(entity_id='Q' + tuple_4[3]))
                    elem_id = None
                    elem_type = None
                    current_claim_key = None
                    label_en = None
                    datavalue_num_id = None
                    datavalue_type = None
                    elem_count += 1
                    possible_edges = []
                    aliases_en = []
                    if elem_count % 10000 == 0:
                        print 'Llevamos ' + str(elem_count)
                elif prefix == "item.claims." + str(current_claim_key) + ".item":
                    possible_edges.append((datatype, datavalue_type, current_claim_key, str(datavalue_num_id)))

            elif event == 'string':
                if prefix == 'item.id':
                    elem_id = value
                elif prefix == 'item.type':
                    elem_type = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datatype':
                    datatype = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datavalue.value.entity-type':
                    datavalue_type = value
                elif prefix == 'item.labels.en.value':
                    label_en = value
                elif prefix == 'item.aliases.en.item.value':
                    aliases_en.append(value)
                elif prefix == 'item.descriptions.en.value':
                    desc_en = value
            elif event == 'map_key' and prefix == 'item.claims':
                current_claim_key = value
            elif event == 'number' and prefix == 'item.claims.' + str(
                    current_claim_key) + '.item.mainsnak.datavalue.value.numeric-id':
                datavalue_num_id = value


    def yield_elements(self):
        json_stream = open(self._in_file)

        elem_id = None
        elem_type = None
        desc_en = None
        label_en = None
        properties = []
        current_claim_key = None

        elem_count = 1

        for prefix, event, value in ijson.parse(json_stream):
            if event == 'end_map':
                if prefix == 'item':
                    if elem_type == 'item':
                        yield WikidataEntity(entity_id=elem_id,
                                             label=label_en,
                                             description=desc_en,
                                             outcoming_properties_id=properties)
                    elif elem_type == 'property':
                        yield WikidataProperty(property_id=elem_id,
                                               label=label_en,
                                               description=desc_en,
                                               outcoming_properties_id=properties)
                    elem_id = None
                    elem_type = None
                    desc_en = None
                    current_claim_key = None
                    label_en = None
                    properties = []
                    elem_count += 1
                    if elem_count % 500 == 0:
                        print 'Llevamos ' + str(elem_count) + ' elementos'
                if prefix == 'item.claims.' + str(current_claim_key) + '.item':
                    # print 'item.claims.' + str(current_claim_key) + '.item'
                    properties.append(current_claim_key)
            elif event == 'string':
                if prefix == 'item.id':
                    elem_id = value
                elif prefix == 'item.type':
                    elem_type = value
                elif prefix == 'item.descriptions.en.value':
                    desc_en = value
                elif prefix == 'item.labels.en.value':
                    label_en = value
            elif event == 'map_key' and prefix == 'item.claims':
                current_claim_key = value


    def _process_current_data(self, elem_id, elem_type, desc_en, label_en, properties):
        if elem_type == 'item':
            self._process_item(properties)
        elif elem_type == 'property':
            self._process_property(elem_id, desc_en, label_en, properties)
        else:
            self._err_count_item += 1
            print 'Elemento de tipo desconocido:', elem_type


    @staticmethod
    def _is_valid_entity_edge(subj_type, data_nature, data_type):
        if subj_type == 'item' and data_nature == 'wikibase-item' and data_type == 'item':
            return True
        return False
