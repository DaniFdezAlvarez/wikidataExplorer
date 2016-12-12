__author__ = "Dani"





from wikidata_exp.wdexp.communications.input.json.json_in import read_json_object
from wikidata_exp.wdexp.communications.output.json.json_out import write_json_object
from wikidata_exp.wdexp.wikidata.commands.class_ranking_DUMP import KEY_INSTANCES
from wikidata_exp.wdexp.wikidata.commands.agregated_class_summarizer_API import KEY_POS_CLASSRANK, \
    KEY_POS_INSTANCE_COUNTING, KEY_N_INSTANCES


class ClassInstanceCounter(object):
    def __init__(self, source_file_instances, out_file=None):
        """

        Args:
            source_file_instances:
            out_file:

        Returns:

        """

        self._in_file = source_file_instances
        self._out_file = out_file

    def exec_command(self, string_return=False):
        target_classes = read_json_object(self._in_file)
        self._count_instances(target_classes)
        self._erase_instance_lists(target_classes)
        self._add_current_rank(target_classes, KEY_POS_CLASSRANK)
        self._sort_by_instances(target_classes)
        self._add_current_rank(target_classes, KEY_POS_INSTANCE_COUNTING)
        self._serialize_results(target_classes, string_return)

    def _erase_instance_lists(self, target_classes):
        for a_dict in target_classes:
            del a_dict[KEY_INSTANCES]

    def _add_current_rank(self, target_classes, new_key):
        i = 1
        for a_dict in target_classes:
            a_dict[new_key] = i
            i += 1

    def _sort_by_instances(self, target_classes):
        target_classes.sort(key=lambda x: x[KEY_N_INSTANCES], reverse=True)


    def _count_instances(self, target_classes):
        for a_dict in target_classes:
            resultset = set()
            for a_prop_key in a_dict[KEY_INSTANCES]:
                for an_entity_id in a_dict[KEY_INSTANCES][a_prop_key]:
                    resultset.add(an_entity_id)
            a_dict[KEY_N_INSTANCES] = len(resultset)


    def _serialize_results(self, target_classes, string_return):
        # TODO: consider string_return??
        write_json_object(json_object=target_classes,
                          path=self._out_file,
                          indent=4)
