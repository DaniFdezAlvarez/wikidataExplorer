__author__ = "Dani"

from wikidata_exp.wdexp.wikidata.commands.class_ranking_DUMP import KEY_ID, KEY_ACCUMULATED, KEY_INSTANCES
from wikidata_exp.wdexp.communications.input.wikidata.api_reader import WikidataApiReader
from wikidata_exp.wdexp.communications.input.json.json_in import read_json_object
from wikidata_exp.wdexp.communications.output.json.json_out import write_json_object

KEY_N_INSTANCES = "n_instances"
KEY_LABEL = "label"
KEY_DESC = "desc"


class AgregatedClassSummaryCommand(object):
    def __init__(self, source_agregated_scores, out_file=None, n_desirable_complete_classes=1000):

        self._in_ag_scores = source_agregated_scores
        self._out_file = out_file
        self._n_desirable = n_desirable_complete_classes
        self._summary_list = []

        # Communications
        self._api_reader = WikidataApiReader()

    def exec_command(self, string_return=False):
        tracked_counter = 0
        raw_classes_list = self._read_raw_classes()
        for a_class_dict in raw_classes_list:
            self._summary_list.append(self._get_summary_dict(a_class_dict, tracked_counter))
            tracked_counter += 1
        print "Total: ", tracked_counter

        self._serialize_results(string_return)

    def _get_summary_dict(self, raw_class_dict, counter):
        result = {KEY_ID: raw_class_dict[KEY_ID],
                  KEY_ACCUMULATED: raw_class_dict[KEY_ACCUMULATED],
                  KEY_N_INSTANCES: self._count_dict_instances(raw_class_dict),
                  KEY_LABEL: None,
                  KEY_DESC: None}

        if counter < self._n_desirable:
            try:
                tracked_entity = self._api_reader.get_entity(raw_class_dict[KEY_ID])
                result[KEY_LABEL] = tracked_entity.label
                result[KEY_DESC] = tracked_entity.description
            except:
                print "Hubo problemas con ", raw_class_dict[KEY_ID]
            print counter
        return result

    def _count_dict_instances(self, raw_class_dict):
        resultset = set()
        for a_prop_key in raw_class_dict[KEY_INSTANCES]:
            for an_entity_id in raw_class_dict[KEY_INSTANCES][a_prop_key]:
                resultset.add(an_entity_id)
        return len(resultset)

    def _read_raw_classes(self):
        # return [{"id": "Q31",
        #          KEY_ACCUMULATED: 8,
        #          KEY_INSTANCES: {"P1" : ["Q5", "Q3"] # 2 instances
        #                          }
        #          },
        #         {"id": "Q35",
        #          KEY_ACCUMULATED: 8,
        #          KEY_INSTANCES:{"P1" : ["Q5", "Q3"],
        #                         "P2" : ["Q3", "Q2", "Q1"]  # 4 instances (Q3 repeated)
        #                          }}]
        return read_json_object(self._in_ag_scores)

    def _serialize_results(self, string_return):
        # TODO: implement string_return mode. Now, we are assuming string_return=False
        write_json_object(json_object=self._summary_list,
                          path=self._out_file,
                          indent=4)
