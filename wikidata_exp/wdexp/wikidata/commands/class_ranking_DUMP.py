from wikidata_exp.wdexp.communications.input.wikidata.dump_parser import WikidataDumpParser
from wikidata_exp.wdexp.communications.input.wikidata.json01_ids_parser import Json01IdsParser
from wikidata_exp.wdexp.communications.input.wikidata.xslt_class_properties_parser import XsltClassPropertiesParser
from decimal import *
from wikidata_exp.wdexp.communications.output.json.json_out import write_json_object
from wikidata_exp.wdexp.wikidata.commands.page_rank_filter_JSON import MIN_SCORE

KEY_INSTANCES = "i"
KEY_ACCUMULATED = "score"
KEY_NUM_ADDED = "n_a"
KEY_ID = "id"


class ClassRankingCommand(object):

    def __init__(self, source_file_classes, source_file_dump, source_file_scores, out_file=None,
                 security_threshold=25, default_entity_score=MIN_SCORE, direct_class_pointers_input=None):
        """

        Args:
            source_file_classes:
            source_file_dump:
            security_threshold: It indicates how many times should some entity receive
                                certain class pointer to be considered a class (prevent
                                noise)

        Returns:

        """
        self._security_threshold = security_threshold
        self._min_score = default_entity_score

        self._in_file_classes = source_file_classes  # Xslt
        self._in_file_dump = source_file_dump  # JSON dump
        self._in_file_scores = source_file_scores  # huge JSON to parse in chunks
        self._out_file = out_file

        if direct_class_pointers_input is None:
            self._class_pointers = self._read_classes()
        else:
            self._class_pointers = set(direct_class_pointers_input)

        self._candidate_classes = {}
        self._instances_dict = {}



    def _read_classes(self):
        result = set()
        property_parser = XsltClassPropertiesParser(source_file=self._in_file_classes)
        for a_prop_class in property_parser.yield_properties():
            result.add(str(a_prop_class.id))

        # The next lines are for generating a latex table (3 columns, 62 elements)
        # strs = []
        # for i in range(0,21):
        #     strs.append("")
        #     print i
        # i = 0
        # for a_prop_class in property_parser.yield_properties():
        #     strs[i%21] += str(i+1) + ". " + a_prop_class.id + ":" + a_prop_class.label + " &"
        #     i += 1
        # for a_str in strs:
        #     a_str = a_str[:len(a_str) -1] + "\\\\"
        #     print a_str

        return result



    def exec_command(self, string_return=False):
        self._parse_dump_file()
        self._serialize_results(string_return)  # Todo. Check other commands for convention
        print "Done!"



    def _parse_dump_file(self):
        print "Parsing dumping file..."
        count = 0
        for a_triple in WikidataDumpParser(source_file=self._in_file_dump).yield_entity_triples():
            count += 1
            if count % 10000 == 0:
                print "N. triples:", count
            if self._is_a_class_pointer(a_triple.predicate):  # [1] == object of type WikidataProperty (just id)
                self._process_candidate_class(a_triple.subject, a_triple.predicate, a_triple.object)
        self._add_scores_to_candidate_classes()
        self._add_min_scores()
        self._sort_result()


    def _add_min_scores(self):
        for a_class_id in self._candidate_classes:
            self._candidate_classes[a_class_id][KEY_ACCUMULATED] += (self._get_num_of_acepted_instances(a_class_id) - self._candidate_classes[a_class_id][KEY_NUM_ADDED]) * self._min_score


    def _get_num_of_acepted_instances(self, class_id):
        resultset = set()
        for a_prop_id in self._candidate_classes[class_id][KEY_INSTANCES]:
            if len(self._candidate_classes[class_id][KEY_INSTANCES][a_prop_id]) >= self._security_threshold:
                for an_instance in self._candidate_classes[class_id][KEY_INSTANCES][a_prop_id]:
                    resultset.add(an_instance)
        return len(resultset)


    def _sort_result(self):
        result = []
        for a_class_id in self._candidate_classes:
            target_dict = self._candidate_classes[a_class_id]
            target_dict[KEY_ID] = a_class_id
            result.append(target_dict)
            self._candidate_classes[a_class_id] = None  # Free memory. I can't delete the key during the iteration
        self._candidate_classes = result
        result.sort(key=lambda x: x[KEY_ACCUMULATED], reverse=True)
        for a_dict in self._candidate_classes:
            # Turn Decimal objects into string (no precission loss)
            a_dict[KEY_ACCUMULATED] = str(a_dict[KEY_ACCUMULATED])



    def _add_scores_to_candidate_classes(self):
        print "\n\nAdding scores...\n\n"
        count = 0
        for instance_id, instance_score in Json01IdsParser(source_file=self._in_file_scores,
                                                           break_char=",").yield_entity_ids():
            count += 1
            if count % 100000 == 0:
                print "N. scores:", count
            if instance_id in self._instances_dict:
                for a_class_id in self._instances_dict[instance_id]:
                    self._candidate_classes[a_class_id][KEY_ACCUMULATED] += Decimal(instance_score)
                    self._candidate_classes[a_class_id][KEY_NUM_ADDED] += 1
                    print a_class_id



    def _process_candidate_class(self, w_subject, w_property, w_object):
        class_id = w_object.id
        property_id = w_property.id
        instance_id = w_subject.id
        if class_id not in self._candidate_classes:
            self._add_class_candidate_dict(class_id)

        if property_id not in self._candidate_classes[class_id][KEY_INSTANCES]:
            self._add_pointer_to_class(class_id, property_id)

        if self._is_not_enough_used_pointer(class_id, property_id):
            self._add_instance_to_not_yet_class(class_id, property_id, instance_id)
        elif self._is_a_threshold_used_pointer(class_id, property_id):
            self._add_instance_to_new_class(class_id, property_id, instance_id)
        else:
            self._add_instance_to_already_formed_class(class_id, property_id, instance_id)

        # print self._candidate_classes[class_id][_KEY_INSTANCES][property_id], class_id, property_id



    def _is_a_class_pointer(self, w_property):
        if w_property.id in self._class_pointers:
            return True
        return False



    def _add_class_candidate_dict(self, class_id):
        self._candidate_classes[class_id] = {KEY_ACCUMULATED: 0,
                                             KEY_INSTANCES: {},
                                             KEY_NUM_ADDED: 0
                                             }



    def _add_pointer_to_class(self, class_id, property_id):
        self._candidate_classes[class_id][KEY_INSTANCES][property_id] = []



    def _add_instance_to_not_yet_class(self, class_id, property_id, instance_id):
        self._candidate_classes[class_id][KEY_INSTANCES][property_id].append(instance_id)



    def _add_instance_to_new_class(self, class_id, property_id, instance_id):
        self._candidate_classes[class_id][KEY_INSTANCES][property_id].append(instance_id)
        # OJO!!!!! Probable bug in the next loop. Already corrected
        for an_instance in self._candidate_classes[class_id][KEY_INSTANCES][property_id]:
            self._add_confirmed_instance(instance_id=an_instance,
                                         class_id=class_id)



    def _add_instance_to_already_formed_class(self, class_id, property_id, instance_id):
        self._candidate_classes[class_id][KEY_INSTANCES][property_id].append(instance_id)
        self._add_confirmed_instance(instance_id=instance_id,
                                     class_id=class_id)



    def _add_confirmed_instance(self, instance_id, class_id):

        if instance_id not in self._instances_dict:
            self._instances_dict[instance_id] = set()
        self._instances_dict[instance_id].add(class_id)



    def _is_not_enough_used_pointer(self, class_id, property_id):
        return len(self._candidate_classes[class_id][KEY_INSTANCES][property_id]) < self._security_threshold -1



    def _is_a_threshold_used_pointer(self, class_id, property_id):
        return len(self._candidate_classes[class_id][KEY_INSTANCES][property_id]) == self._security_threshold -1



    def _is_more_than_threshold_used_pointer(self, class_id, property_id):
        return len(self._candidate_classes[class_id][KEY_INSTANCES][property_id]) > self._security_threshold -1



    def _serialize_results(self, string_return):
        print "\n\nSerializing results...\n\n"
        write_json_object(json_object=self._candidate_classes,
                          path=self._out_file,
                          indent=4)

        #Todo: consider string_return??
