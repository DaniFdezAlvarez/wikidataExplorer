import unittest
from decimal import *
from wikidata_exp.wdexp.wikidata.commands.class_ranking_DUMP import ClassRankingCommand, \
    KEY_ACCUMULATED, KEY_NUM_ADDED, KEY_ID
from wikidata_exp.wdexp.model.wikidata import WikidataEntity, WikidataProperty, WikidataTriple



__author__ = 'Dani'




class ClassRankDirectInput(ClassRankingCommand):
    def __init__(self, raw_pg_scores, raw_triples, source_file_classes, source_file_dump,
                 source_file_scores, security_threshold, direct_class_pointers_input, default_entity_score):
        super(ClassRankDirectInput, self).__init__(source_file_classes, source_file_dump, source_file_scores,
                                                   security_threshold=security_threshold,
                                                   direct_class_pointers_input=direct_class_pointers_input,
                                                   default_entity_score=default_entity_score)
        # Class-pointers already parsed.
        # self._raw_pg_scores = raw_pg_scores  # A list of tuples (instance_id, score)
        self._raw_triples = raw_triples  # A list of tuples (sub_id, pre_id, obj_id)
        self._raw_pg_scores = []

        for a_score in raw_pg_scores:
            self._raw_pg_scores.append((a_score[0], Decimal(a_score[1])))

    def exec_command(self, string_return=False):
        self._parse_dump_file()
        # self._serialize_results(string_return)  # Todo. Check other commands for convention
        # print "Done!"


    def _add_scores_to_candidate_classes(self):
        for a_tuple in self._raw_pg_scores:
            instance_id = a_tuple[0]
            instance_score = a_tuple[1]
            if instance_id in self._instances_dict:
                for a_class_id in self._instances_dict[instance_id]:
                    self._candidate_classes[a_class_id][KEY_ACCUMULATED] += instance_score
                    self._candidate_classes[a_class_id][KEY_NUM_ADDED] += 1


    def _parse_dump_file(self):
        for a_triple in self._yield_entity_triples_from_raw():
            if self._is_a_class_pointer(a_triple.predicate):  # [1] == object of type WikidataProperty (just id)
                self._process_candidate_class(a_triple.subject, a_triple.predicate, a_triple.object)
        self._add_scores_to_candidate_classes()
        self._add_min_scores()
        self._sort_result()

    def _yield_entity_triples_from_raw(self):
        for a_triple in self._raw_triples:
            yield WikidataTriple(subject=WikidataEntity(entity_id=a_triple[0]),
                                 predicate=WikidataProperty(property_id=a_triple[1]),
                                 target_object=WikidataEntity(entity_id=a_triple[2]))

    def get_classes(self):
        result = []
        for elem in self._candidate_classes:
            result.append(elem[KEY_ID])
        return result

    def get_class_score(self, class_id):
        # return self._candidate_classes[class_id][KEY_ACCUMULATED]
        for a_class_dict in self._candidate_classes:
            if a_class_dict[KEY_ID] == class_id:
                return float(a_class_dict[KEY_ACCUMULATED])
        return None

    def get_accepted_instances(self, target_id):
        result = []
        for an_instance_id in self._instances_dict:
            for a_class_id in self._instances_dict[an_instance_id]:
                if a_class_id == target_id:
                    result.append(an_instance_id)
                    break
        return result

        # def get_num_instances(self, target_id):
        #     for a_dict in self._candidate_classes:
        #         if target_id == a_dict[KEY_ID]:
        #             resultset = set()
        #             for a_prop_id in a_dict[KEY_INSTANCES]:
        #                 if len(a_dict[KEY_INSTANCES][a_prop_id]) >= self._security_threshold:
        #                     for an_instance in a_dict[KEY_INSTANCES][a_prop_id]:
        #                         resultset.add(an_instance)
        #             return len(resultset)
        #     return None


class TestCategoryDetectionSparql(unittest.TestCase):
    def test_all_under_threshold(self):
        raw_triples = [
            ("a1", "type", "A"),
            ("a2", "type", "A"),
            ("a3", "type", "A"),
            ("a4", "type", "A"),
            ("a5", "type", "A"),
            ("a6", "type", "A"),
            ("a7", "type", "A"),
            ("a8", "type", "A"),
            ("a9", "type", "A"),
            ("a10", "type", "A"),
            ("a11", "type", "A"),
            ("b1", "type", "B"),
            ("b2", "type", "B"),
            ("b3", "type", "B"),
            ("ab1", "type", "B"),
            ("ab1", "type", "A"),
            ("ab2", "type", "B"),
            ("ab2", "type", "A"),

        ]
        raw_pg_scores = [
            ("a1", 0.1),
            ("a2", 0.2),
            ("a3", 0.1),
            ("a4", 0.2),
            ("a5", 0.1),
            ("a6", 0.2),
            ("a7", 0.1),
            ("a8", 0.2),
            ("a9", 0.1),
            ("a10", 0.2),
            ("a11", 0.1),
            ("b1", 0.3),
            ("b2", 0.4),
            ("b3", 0.5),
            ("ab1", 0.6),
            # ab2 missing
        ]

        raw_classes = ["type"]

        ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                      raw_triples=raw_triples,
                                      source_file_dump="",
                                      source_file_scores="",
                                      source_file_classes="",
                                      direct_class_pointers_input=raw_classes,
                                      security_threshold=15,
                                      default_entity_score=Decimal(0))
        ranker.exec_command()
        self.assertEqual(2, len(ranker.get_classes()))

        self.assertEqual(0, ranker.get_class_score("A"))
        self.assertEqual(0, ranker.get_class_score("B"))

        self.assertAlmostEqual(len(ranker.get_accepted_instances("A")), 0)
        self.assertAlmostEqual(len(ranker.get_accepted_instances("B")), 0)

    def test_one_under_threshold(self):
        raw_triples = [
            ("a1", "type", "A"),
            ("a2", "type", "A"),
            ("a3", "type", "A"),
            ("a4", "type", "A"),
            ("a5", "type", "A"),
            ("a6", "type", "A"),
            ("a7", "type", "A"),
            ("a8", "type", "A"),
            ("a9", "type", "A"),
            ("a10", "type", "A"),
            ("a11", "type", "A"),
            ("b1", "type", "B"),
            ("b2", "type", "B"),
            ("b3", "type", "B"),
            ("ab1", "type", "B"),
            ("ab1", "type", "A"),
            ("ab2", "type", "B"),
            ("ab2", "type", "A"),

        ]
        raw_pg_scores = [
            ("a1", 0.1),
            ("a2", 0.2),
            ("a3", 0.1),
            ("a4", 0.2),
            ("a5", 0.1),
            ("a6", 0.2),
            ("a7", 0.1),
            ("a8", 0.2),
            ("a9", 0.1),
            ("a10", 0.2),
            ("a11", 0.1),
            ("b1", 0.3),
            ("b1", 0.4),
            ("b1", 0.5),
            ("ab1", 0.6),
            # ab2 missing
        ]

        raw_classes = ["type"]

        ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                      raw_triples=raw_triples,
                                      source_file_dump="",
                                      source_file_scores="",
                                      source_file_classes="",
                                      direct_class_pointers_input=raw_classes,
                                      security_threshold=10,
                                      default_entity_score=Decimal(0))
        ranker.exec_command()
        self.assertEqual(2, len(ranker.get_classes()))
        self.assertEqual(0, ranker.get_class_score("B"))
        self.assertAlmostEqual(2.2, ranker.get_class_score("A"))
        self.assertAlmostEqual(len(ranker.get_accepted_instances("A")), 13)
        self.assertAlmostEqual(len(ranker.get_accepted_instances("B")), 0)

    def test_both_above_threshold(self):
        raw_triples = [
            ("a1", "type", "A"),
            ("a2", "type", "A"),
            ("a3", "type", "A"),
            ("a4", "type", "A"),
            ("a5", "type", "A"),
            ("a6", "type", "A"),
            ("a7", "type", "A"),
            ("a8", "type", "A"),
            ("a9", "type", "A"),
            ("a10", "type", "A"),
            ("a11", "type", "A"),
            ("b1", "type", "B"),
            ("b2", "type", "B"),
            ("b3", "type", "B"),
            ("ab1", "type", "B"),
            ("ab1", "type", "A"),
            ("ab2", "type", "B"),
            ("ab2", "type", "A"),

        ]
        raw_pg_scores = [
            ("a1", 0.1),
            ("a2", 0.2),
            ("a3", 0.1),
            ("a4", 0.2),
            ("a5", 0.1),
            ("a6", 0.2),
            ("a7", 0.1),
            ("a8", 0.2),
            ("a9", 0.1),
            ("a10", 0.2),
            ("a11", 0.1),
            ("b1", 0.3),
            ("b2", 0.4),
            ("b3", 0.7),
            ("ab1", 0.6),
            # ab2 missing   -->  MIN_SCORE
        ]

        raw_classes = ["type"]

        ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                      raw_triples=raw_triples,
                                      source_file_dump="",
                                      source_file_scores="",
                                      source_file_classes="",
                                      direct_class_pointers_input=raw_classes,
                                      security_threshold=5,
                                      default_entity_score=Decimal(0.1))
        ranker.exec_command()
        self.assertEqual(2, len(ranker.get_classes()))
        self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
        self.assertEqual(len(ranker.get_accepted_instances("B")), 5)
        self.assertEqual(2.1, ranker.get_class_score("B"))
        self.assertAlmostEqual(2.3, ranker.get_class_score("A"))

    def test_A_with_1_1_B_with_1_0_threshold(self):
        raw_triples = [
            ("a1", "type", "A"),
            ("a2", "type", "A"),
            ("a3", "type", "A"),
            ("a4", "type", "A"),
            ("a5", "type", "A"),
            ("a6", "type", "A"),
            ("a7", "type", "A"),
            ("a8", "type", "A"),
            ("a9", "type", "A"),
            ("a10", "type", "A"),
            ("a11", "type", "A"),
            ("b1", "type", "B"),
            ("b2", "type", "B"),
            ("b3", "type", "B"),
            ("ab1", "type", "B"),
            ("ab1", "type", "A"),
            ("ab2", "type", "B"),
            ("ab2", "type", "A"),
            ("a12", "subclass", "A")

        ]
        raw_pg_scores = [
            ("a1", 0.1),
            ("a2", 0.2),
            ("a3", 0.1),
            ("a4", 0.2),
            ("a5", 0.1),
            ("a6", 0.2),
            ("a7", 0.1),
            ("a8", 0.2),
            ("a9", 0.1),
            ("a10", 0.2),
            ("a11", 0.1),
            ("b1", 0.3),
            ("b2", 0.4),
            ("b3", 0.7),
            ("ab1", 0.6),
            ("a12", 0.5)
            # ab2 missing   -->  MIN_SCORE
        ]

        raw_classes = ["type", "subclass"]

        ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                      raw_triples=raw_triples,
                                      source_file_dump="",
                                      source_file_scores="",
                                      source_file_classes="",
                                      direct_class_pointers_input=raw_classes,
                                      security_threshold=5,
                                      default_entity_score=Decimal(0.1))
        ranker.exec_command()
        self.assertEqual(2, len(ranker.get_classes()))
        self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
        self.assertEqual(len(ranker.get_accepted_instances("B")), 5)
        self.assertEqual(2.1, ranker.get_class_score("B"))
        self.assertAlmostEqual(2.3, ranker.get_class_score("A"))

    def test_A_with_1_1_B_with_2_0_threshold(self):
        raw_triples = [
            ("a1", "type", "A"),
            ("a2", "type", "A"),
            ("a3", "type", "A"),
            ("a4", "type", "A"),
            ("a5", "type", "A"),
            ("a6", "type", "A"),
            ("a7", "type", "A"),
            ("a8", "type", "A"),
            ("a9", "type", "A"),
            ("a10", "type", "A"),
            ("a11", "type", "A"),
            ("b1", "type", "B"),
            ("b2", "type", "B"),
            ("b3", "type", "B"),
            ("ab1", "type", "B"),
            ("ab1", "type", "A"),
            ("ab2", "type", "B"),
            ("ab2", "type", "A"),
            ("a12", "subclass", "A"),
            ("b4", "subclass", "B"),
            ("b5", "subclass", "B"),
            ("b6", "subclass", "B"),
            ("b7", "subclass", "B"),
            ("b8", "subclass", "B"),

        ]
        raw_pg_scores = [
            ("a1", 0.1),
            ("a2", 0.2),
            ("a3", 0.1),
            ("a4", 0.2),
            ("a5", 0.1),
            ("a6", 0.2),
            ("a7", 0.1),
            ("a8", 0.2),
            ("a9", 0.1),
            ("a10", 0.2),
            ("a11", 0.1),
            ("b1", 0.3),
            ("b2", 0.4),
            ("b3", 0.7),
            ("ab1", 0.6),
            ("a12", 0.5),
            ("b4", 0.5),
            ("b4", 0.5),
            ("b6", 0.5),
            ("b7", 0.5),
            ("b8", 0.5)
            # ab2 missing   -->  MIN_SCORE
        ]

        raw_classes = ["type", "subclass"]

        ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                      raw_triples=raw_triples,
                                      source_file_dump="",
                                      source_file_scores="",
                                      source_file_classes="",
                                      direct_class_pointers_input=raw_classes,
                                      security_threshold=5,
                                      default_entity_score=Decimal(0.1))
        ranker.exec_command()
        self.assertEqual(2, len(ranker.get_classes()))
        self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
        self.assertEqual(len(ranker.get_accepted_instances("B")), 10)
        self.assertEqual(4.6, ranker.get_class_score("B"))
        self.assertAlmostEqual(2.3, ranker.get_class_score("A"))

    def test_C_unfrequent_no_class_pointer(self):
        raw_triples = [
            ("a1", "type", "A"),
            ("a2", "type", "A"),
            ("a3", "type", "A"),
            ("a4", "type", "A"),
            ("a5", "type", "A"),
            ("a6", "type", "A"),
            ("a7", "type", "A"),
            ("a8", "type", "A"),
            ("a9", "type", "A"),
            ("a10", "type", "A"),
            ("a11", "type", "A"),
            ("b1", "type", "B"),
            ("b2", "type", "B"),
            ("b3", "type", "B"),
            ("ab1", "type", "B"),
            ("ab1", "type", "A"),
            ("ab2", "type", "B"),
            ("ab2", "type", "A"),
            ("a12", "subclass", "A"),
            ("b4", "subclass", "B"),
            ("b5", "subclass", "B"),
            ("b6", "subclass", "B"),
            ("b7", "subclass", "B"),
            ("b8", "subclass", "B"),
            ("c1", "foo", "C")
        ]
        raw_pg_scores = [
            ("a1", 0.1),
            ("a2", 0.2),
            ("a3", 0.1),
            ("a4", 0.2),
            ("a5", 0.1),
            ("a6", 0.2),
            ("a7", 0.1),
            ("a8", 0.2),
            ("a9", 0.1),
            ("a10", 0.2),
            ("a11", 0.1),
            ("b1", 0.3),
            ("b2", 0.4),
            ("b3", 0.7),
            ("ab1", 0.6),
            ("a12", 0.5),
            ("b4", 0.5),
            ("b4", 0.5),
            ("b6", 0.5),
            ("b7", 0.5),
            ("b8", 0.5)
            # ab2 missing   -->  MIN_SCORE
        ]

        raw_classes = ["type", "subclass"]

        ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                      raw_triples=raw_triples,
                                      source_file_dump="",
                                      source_file_scores="",
                                      source_file_classes="",
                                      direct_class_pointers_input=raw_classes,
                                      security_threshold=5,
                                      default_entity_score=Decimal(0.1))
        ranker.exec_command()
        self.assertEqual(2, len(ranker.get_classes()))
        self.assertNotIn("C", ranker.get_classes())

        self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
        self.assertEqual(len(ranker.get_accepted_instances("B")), 10)
        self.assertEqual(4.6, ranker.get_class_score("B"))
        self.assertAlmostEqual(2.3, ranker.get_class_score("A"))


def test_C_frequent_no_class_pointer(self):
    raw_triples = [
        ("a1", "type", "A"),
        ("a2", "type", "A"),
        ("a3", "type", "A"),
        ("a4", "type", "A"),
        ("a5", "type", "A"),
        ("a6", "type", "A"),
        ("a7", "type", "A"),
        ("a8", "type", "A"),
        ("a9", "type", "A"),
        ("a10", "type", "A"),
        ("a11", "type", "A"),
        ("b1", "type", "B"),
        ("b2", "type", "B"),
        ("b3", "type", "B"),
        ("ab1", "type", "B"),
        ("ab1", "type", "A"),
        ("ab2", "type", "B"),
        ("ab2", "type", "A"),
        ("a12", "subclass", "A"),
        ("b4", "subclass", "B"),
        ("b5", "subclass", "B"),
        ("b6", "subclass", "B"),
        ("b7", "subclass", "B"),
        ("b8", "subclass", "B"),
        ("c1", "foo", "C"),
        ("c2", "foo", "C"),
        ("c3", "foo", "C"),
        ("c4", "foo", "C"),
        ("c5", "foo", "C"),
        ("c6", "foo", "C"),
        ("c7", "foo", "C"),
        ("c8", "foo", "C"),
        ("c9", "foo", "C"),
        ("c10", "foo", "C")
    ]
    raw_pg_scores = [
        ("a1", 0.1),
        ("a2", 0.2),
        ("a3", 0.1),
        ("a4", 0.2),
        ("a5", 0.1),
        ("a6", 0.2),
        ("a7", 0.1),
        ("a8", 0.2),
        ("a9", 0.1),
        ("a10", 0.2),
        ("a11", 0.1),
        ("b1", 0.3),
        ("b2", 0.4),
        ("b3", 0.7),
        ("ab1", 0.6),
        ("a12", 0.5),
        ("b4", 0.5),
        ("b4", 0.5),
        ("b6", 0.5),
        ("b7", 0.5),
        ("b8", 0.5)
        # ab2 missing   -->  MIN_SCORE
    ]

    raw_classes = ["type", "subclass"]

    ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                  raw_triples=raw_triples,
                                  source_file_dump="",
                                  source_file_scores="",
                                  source_file_classes="",
                                  direct_class_pointers_input=raw_classes,
                                  security_threshold=5,
                                  default_entity_score=Decimal(0.1))
    ranker.exec_command()
    self.assertEqual(2, len(ranker.get_classes()))
    self.assertNotIn("C", ranker.get_classes())

    self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
    self.assertEqual(len(ranker.get_accepted_instances("B")), 10)
    self.assertEqual(4.6, ranker.get_class_score("B"))
    self.assertAlmostEqual(2.3, ranker.get_class_score("A"))


def test_C_frequent_no_class_pointer_A_1_no_class_pointer(self):
    raw_triples = [
        ("a1", "type", "A"),
        ("a2", "type", "A"),
        ("a3", "type", "A"),
        ("a4", "type", "A"),
        ("a5", "type", "A"),
        ("a6", "type", "A"),
        ("a7", "type", "A"),
        ("a8", "type", "A"),
        ("a9", "type", "A"),
        ("a10", "type", "A"),
        ("a11", "type", "A"),
        ("b1", "type", "B"),
        ("b2", "type", "B"),
        ("b3", "type", "B"),
        ("ab1", "type", "B"),
        ("ab1", "type", "A"),
        ("ab2", "type", "B"),
        ("ab2", "type", "A"),
        ("a12", "subclass", "A"),
        ("b4", "subclass", "B"),
        ("b5", "subclass", "B"),
        ("b6", "subclass", "B"),
        ("b7", "subclass", "B"),
        ("b8", "subclass", "B"),
        ("c1", "foo", "C"),
        ("c2", "foo", "C"),
        ("c3", "foo", "C"),
        ("c4", "foo", "C"),
        ("c5", "foo", "C"),
        ("c6", "foo", "C"),
        ("c7", "foo", "C"),
        ("c8", "foo", "C"),
        ("c9", "foo", "C"),
        ("c10", "foo", "C"),
        ("a12", "foo", "A")

    ]
    raw_pg_scores = [
        ("a1", 0.1),
        ("a2", 0.2),
        ("a3", 0.1),
        ("a4", 0.2),
        ("a5", 0.1),
        ("a6", 0.2),
        ("a7", 0.1),
        ("a8", 0.2),
        ("a9", 0.1),
        ("a10", 0.2),
        ("a11", 0.1),
        ("b1", 0.3),
        ("b2", 0.4),
        ("b3", 0.7),
        ("ab1", 0.6),
        ("a12", 0.5),
        ("b4", 0.5),
        ("b4", 0.5),
        ("b6", 0.5),
        ("b7", 0.5),
        ("b8", 0.5),
        ("c1", 10),
        ("a12", 10)
        # ab2 missing   -->  MIN_SCORE
    ]

    raw_classes = ["type", "subclass"]

    ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                  raw_triples=raw_triples,
                                  source_file_dump="",
                                  source_file_scores="",
                                  source_file_classes="",
                                  direct_class_pointers_input=raw_classes,
                                  security_threshold=5,
                                  default_entity_score=Decimal(0.1))
    ranker.exec_command()
    self.assertEqual(2, len(ranker.get_classes()))
    self.assertNotIn("C", ranker.get_classes())

    self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
    self.assertEqual(len(ranker.get_accepted_instances("B")), 10)
    self.assertEqual(4.6, ranker.get_class_score("B"))
    self.assertAlmostEqual(2.3, ranker.get_class_score("A"))


def test_C_unfrequent_no_class_pointer_C_1_0_threshold_A_1_no_class_pointer(self):
    raw_triples = [
        ("a1", "type", "A"),
        ("a2", "type", "A"),
        ("a3", "type", "A"),
        ("a4", "type", "A"),
        ("a5", "type", "A"),
        ("a6", "type", "A"),
        ("a7", "type", "A"),
        ("a8", "type", "A"),
        ("a9", "type", "A"),
        ("a10", "type", "A"),
        ("a11", "type", "A"),
        ("b1", "type", "B"),
        ("b2", "type", "B"),
        ("b3", "type", "B"),
        ("ab1", "type", "B"),
        ("ab1", "type", "A"),
        ("ab2", "type", "B"),
        ("ab2", "type", "A"),
        ("a12", "subclass", "A"),
        ("b4", "subclass", "B"),
        ("b5", "subclass", "B"),
        ("b6", "subclass", "B"),
        ("b7", "subclass", "B"),
        ("b8", "subclass", "B"),
        ("c1", "type", "C"),
        ("c2", "type", "C"),
        ("c3", "type", "C"),
        ("c4", "type", "C"),
        ("c5", "type", "C"),
        ("c6", "type", "C"),
        ("c7", "type", "C"),
        ("c8", "type", "C"),
        ("c9", "type", "C"),
        ("c10", "type", "C"),
        ("c11", "foo", "C"),
        ("a12", "foo", "A")

    ]
    raw_pg_scores = [
        ("a1", 0.1),
        ("a2", 0.2),
        ("a3", 0.1),
        ("a4", 0.2),
        ("a5", 0.1),
        ("a6", 0.2),
        ("a7", 0.1),
        ("a8", 0.2),
        ("a9", 0.1),
        ("a10", 0.2),
        ("a11", 0.1),
        ("b1", 0.3),
        ("b2", 0.4),
        ("b3", 0.7),
        ("ab1", 0.6),
        ("a12", 0.5),
        ("b4", 0.5),
        ("b4", 0.5),
        ("b6", 0.5),
        ("b7", 0.5),
        ("b8", 0.5),
        ("c1", 0.6),
        ("c11", 10),
        ("a12", 10)
        # ab2 missing   -->  MIN_SCORE
        # cX except c1 and c11 missing
    ]

    raw_classes = ["type", "subclass"]

    ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                  raw_triples=raw_triples,
                                  source_file_dump="",
                                  source_file_scores="",
                                  source_file_classes="",
                                  direct_class_pointers_input=raw_classes,
                                  security_threshold=5,
                                  default_entity_score=Decimal(0.1))
    ranker.exec_command()
    self.assertEqual(3, len(ranker.get_classes()))
    self.assertIn("C", ranker.get_classes())

    self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
    self.assertEqual(len(ranker.get_accepted_instances("B")), 10)
    self.assertEqual(len(ranker.get_accepted_instances("C")), 10)

    self.assertEqual(4.6, ranker.get_class_score("B"))
    self.assertAlmostEqual(2.3, ranker.get_class_score("A"))
    self.assertAlmostEqual(1.5, ranker.get_class_score("C"))


def test_all_no_class_pointers(self):
    raw_triples = [
        ("a1", "foo", "A"),
        ("a2", "foo", "A"),
        ("a3", "foo", "A"),
        ("a4", "foo", "A"),
        ("b1", "foo", "B"),
        ("b2", "foo", "B"),
        ("b3", "foo", "B"),
        ("ab1", "foo", "B"),
        ("ab1", "foo", "A"),
        ("ab2", "foo", "B"),
        ("ab2", "foo", "A"),
        ("a12", "foo", "A"),
        ("c1", "foo", "C")
    ]
    raw_pg_scores = [
        ("a1", 0.1),
        ("a2", 0.2),
        ("a3", 0.1),
        ("a4", 0.2),
        ("a5", 0.1),
        ("a6", 0.2),
        ("a7", 0.1),
        ("a8", 0.2),
        ("a9", 0.1),
        ("a10", 0.2),
        ("a11", 0.1),
        ("b1", 0.3),
        ("b2", 0.4),
        ("b3", 0.7),
        ("ab1", 0.6),
        ("a12", 0.5),
        ("b4", 0.5),
        ("b4", 0.5),
        ("b6", 0.5),
        ("b7", 0.5),
        ("b8", 0.5),
        ("c1", 0.6),
        ("c11", 10),
        ("a12", 10)
        # ab2 missing   -->  MIN_SCORE
        # cX except c1 and c11 missing
    ]

    raw_classes = ["type", "subclass"]

    ranker = ClassRankDirectInput(raw_pg_scores=raw_pg_scores,
                                  raw_triples=raw_triples,
                                  source_file_dump="",
                                  source_file_scores="",
                                  source_file_classes="",
                                  direct_class_pointers_input=raw_classes,
                                  security_threshold=5,
                                  default_entity_score=Decimal(0.1))
    ranker.exec_command()
    self.assertEqual(0, len(ranker.get_classes()))
    # self.assertIn("C", ranker.get_classes())
    #
    # self.assertEqual(len(ranker.get_accepted_instances("A")), 13)
    # self.assertEqual(len(ranker.get_accepted_instances("B")), 10)
    # self.assertEqual(len(ranker.get_accepted_instances("C")), 10)
    #
    # self.assertEqual(4.6, ranker.get_class_score("B"))
    # self.assertAlmostEqual(2.3, ranker.get_class_score("A"))
    # self.assertAlmostEqual(1.5, ranker.get_class_score("C"))
