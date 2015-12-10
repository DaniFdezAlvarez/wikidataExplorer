__author__ = 'Dani'

import networkx as nx
import ijson


class GraphEntitiesCommand(object):
    def __init__(self, source_file, out_file):
        self._in_file = source_file
        self._out_file = out_file


    def exec_command(self, string_return=False, object_return=False):
        if string_return and object_return:
            raise BaseException("You should use just a type of return")
        graph = self._create_nx_graph()
        if object_return:
            return graph


    def _create_nx_graph(self):
        g = nx.DiGraph()
        for origin, target in self._read_edges():
            g.add_edge(origin, target)

        return g

    def _read_edges(self):
        json_stream = open(self._in_file)
        elem_id = None
        elem_type = None
        # desc_en = None
        # label_en = None
        datatype = None
        datavalue_type = None
        current_claim_key = None
        datavalue_num_id = None
        possible_edges = []

        elem_count = 1

        for prefix, event, value in ijson.parse(json_stream):
            if event == 'end_map' and prefix == 'item':
                for triple in possible_edges:
                    if self._is_valid_edge(elem_type, triple[0], triple[1]):  # triple: datatype, datavalue_type, datavalue_num_id
                        yield (elem_id, 'Q' + triple[2])
                        # pass
                elem_id = None
                elem_type = None
                current_claim_key = None
                # label_en = None
                datavalue_num_id = None
                datavalue_type = None
                elem_count += 1
                possible_edges = []
                if elem_count % 10000 == 0:
                    print 'Llevamos ' + str(elem_count) + ' elementos'
            elif event == 'string':
                if prefix == 'item.id':
                    elem_id = value
                elif prefix == 'item.type':
                    elem_type = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datatype':
                    datatype = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datavalue.value.entity-type':
                    datavalue_type = value
                # elif prefix == 'item.labels.en.value':
                #     label_en = value
            elif event == 'map_key' and prefix == 'item.claims':
                current_claim_key = value
            elif event == 'number' and prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datavalue.value.numeric-id':
                datavalue_num_id = value
            elif event == "end_array" and prefix == "item.claims." + str(current_claim_key):
                possible_edges.append((datatype, datavalue_type, str(datavalue_num_id)))


    @staticmethod
    def _is_valid_edge(subj_type, data_nature, data_type):
        # print subj_type, data_nature, data_type
        if subj_type == 'item' and data_nature == 'wikibase-item' and data_type == 'item':
            return True
        return False