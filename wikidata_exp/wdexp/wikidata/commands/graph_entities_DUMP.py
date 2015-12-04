__author__ = 'Dani'

import networkx as nx
import ijson



class GraphEntitiesCommand(object):

    def __init__(self, source_file, out_file):
        self._in_file = source_file
        self._out_file = out_file


    def exec_command(self, string_return=False):
        graph = self._create_nx_graph()


    def _create_nx_graph(self):
        g = nx.DiGraph()
        for origin, target in self._read_edges():
            g.add_edge(origin, target)

        return g

    def _read_edges(self):
        json_stream = open(self._in_file)

        elem_id = None
        elem_type = None
        desc_en = None
        label_en = None
        datatype = None
        datavalue_type = None
        current_claim_key = None


        elem_count = 1

        for prefix, event, value in ijson.parse(json_stream):
            if event == 'end_map' and prefix == 'item':
                # self._process_current_data(elem_id, elem_type, desc_en, label_en, properties)
                elem_id = None
                elem_type = None
                current_claim_key = None
                label_en = None
                datavalue_num_id = None
                datavalue_type = None
                edges = []
                elem_count += 1
                if elem_count % 500 == 0:
                    print 'Llevamos ' + str(elem_count) + ' elementos'
            elif event == 'string' and prefix == 'item.id':
                elem_id = value
            elif event == 'string' and prefix == 'item.type':
                elem_type = value
            elif event == 'string' and prefix == 'item.labels.en.value':
                label_en = value
            elif event == 'map_key' and prefix == 'item.claims':
                current_claim_key = value
            elif event == 'string' and prefix == 'item.claims.' + str(current_claim_key) + '.mainsnak.datatype':
                datatype = value
            elif event == 'string' and prefix == 'item.claims.' + str(current_claim_key) + '.mainsnak.datavalue.value.entity-type':
                datavalue_type = value
            elif event == 'string' and prefix == 'item.claims.' + str(current_claim_key) + '.mainsnak.datavalue.value.numeric-id':
                datavalue_num_id = value

            ## DETECTAR EVENTO DE CIERRE DE MAINSAK Y LANZAR ARISTA con yield, si el type es el apropiado

            elif event == 'start_map' and prefix == 'item.claims.' + str(current_claim_key) + '.item':
                # print 'item.claims.' + str(current_claim_key) + '.item'
                # properties[current_claim_key] += 1
                pass  # Este sigue sirviendo??
