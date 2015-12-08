__author__ = 'Dani'
from networkx.algorithms import pagerank



class PageRankCommand(object):

    def __init__(self, networkx_graph, out_file):
        self._grpah = networkx_graph
        self._out_file = out_file

    def exec_command(self, string_return=False):
        result = pagerank(self._grpah, alpha=0.9)
        if string_return:
            return str(result)
        else:
            with open(self._out_file, 'w') as out_stream:
                out_stream.write(str(result))