__author__ = 'Dani'

import ijson


class FrequencyPropertiesCommand(object):

    def __init__(self, source_file, out_file):
        self._in_file = source_file
        self._out_file = out_file
        self._property_counter_dict = {}
        self._property_name_dict = {}
        self._err_count_prop = 0
        self._err_count_item = 0


    def exec_command(self, string_return=False):
        """

        :param string_return: if true, returns a string summary. Otherwise, writes to out_file
        :return:
        """

        json_stream = open(self._in_file)

        elem_id = None
        elem_type = None
        desc_en = None
        label_en = None
        properties = {}
        current_claim_key = None

        elem_count = 1

        for prefix, event, value in ijson.parse(json_stream):
            if event == 'end_map':
                if prefix == 'item':
                    self._process_current_data(elem_id, elem_type, desc_en, label_en, properties)
                    elem_id = None
                    elem_type = None
                    desc_en = None
                    current_claim_key = None
                    label_en = None
                    properties = {}
                    elem_count += 1
                    if elem_count % 500 == 0:
                        print 'Llevamos ' + str(elem_count) + ' elementos'
                if prefix == 'item.claims.' + str(current_claim_key) + '.item':
                    # print 'item.claims.' + str(current_claim_key) + '.item'
                    properties[current_claim_key] += 1
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
                properties[value] = 0
                current_claim_key = value



        print 'Errores en propiedades: ', self._err_count_prop
        print 'Errores en items: ', self._err_count_item

        if not string_return:
            self._write_to_file()
        else:
            return self._get_string_return()


    def _write_to_file(self):
        with open(self._out_file, "w") as result_file:
                result_file.write(self._get_string_return())


    def _get_string_return(self):
        list_count = sorted(self._property_counter_dict, key=self._property_counter_dict.get, reverse=True)
        result = ""
        for elem in list_count:
            to_write = elem + " : " + str(self._property_counter_dict[elem])
            if elem in self._property_name_dict:
                to_write += " : " + self._property_name_dict[elem]
            to_write += "\n"
            result += to_write
        return result.encode('utf-8')


    def _process_current_data(self, elem_id, elem_type, desc_en, label_en, properties):
        if elem_type == 'item':
            self._process_item(properties)
        elif elem_type == 'property':
            self._process_property(elem_id, desc_en, label_en, properties)
        else:
            self._err_count_item += 1
            print 'Elemento de tipo desconocido:', elem_type


    def _process_item(self, properties):
        try:
            for a_claim_key in properties:
                if a_claim_key not in self._property_counter_dict:
                    self._property_counter_dict[a_claim_key] = 0
                self._property_counter_dict[a_claim_key] += properties[a_claim_key]
        except:
            self._err_count_item += 1
            print "Fallo en item"


    def _process_property(self, elem_id, desc_en, label_en, properties):
        try:

            if elem_id not in self._property_name_dict:
                prop_description = 'unavaibale in english'
                if desc_en is not None and label_en is not None:
                    prop_description = desc_en + " : " + label_en
                elif desc_en is not None:
                    prop_description = desc_en + " : "
                elif label_en is not None:
                    prop_description = " : " + label_en
                self._property_name_dict[elem_id] = prop_description
            for a_claim_key in properties:
                if a_claim_key not in self._property_counter_dict:
                    self._property_counter_dict[a_claim_key] = 0
                self._property_counter_dict[a_claim_key] += properties[a_claim_key]
        except:
            self._err_count_prop += 1
            print "Fallo en propiedad"


