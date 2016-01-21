__author__ = 'Dani'

from wdexp.wikidata.commands.category_detection_SPARQL import CategoryDetectionCommand
from wdexp.utils import rel_path_to_file
import unittest
import json


class TestCategoryDetectionSparql(unittest.TestCase):

    def test_category_detection_slice(self):
        categorizer = CategoryDetectionCommand(source_file=rel_path_to_file("../files/in/complete_top_pg_entities.json",
                                                                            __file__),
                                               out_file=rel_path_to_file(
                                                   "../files/out/categorized_top_pg_entities.json",
                                                   __file__))
        result = categorizer._exec_command(string_return=True)
        result = json.loads(result)

        print "------"

        # print result

        self.assertEqual(4, len(result))
        self.assertIn("no_taxon", result)
        self.assertIn("both", result)
        self.assertIn("is_instance", result)
        self.assertIn("have_instances", result)


        self.assertEqual(0, len(result["no_taxon"]))
        self.assertEqual(6, len(result["is_instance"]))
        self.assertEqual(18, len(result["both"]))
        self.assertEqual(0, len(result["have_instances"]))

        an_entity = result["is_instance"][0]

        self.assertEqual(5, len(an_entity))
        self.assertEqual("Q148", an_entity["id"])
        self.assertEqual("state in East Asia", an_entity["description"])
        self.assertEqual("People's Republic of China", an_entity["label"])
        self.assertEqual("0.014571185387097224", an_entity["pg_score"])
        self.assertEqual(4, len(an_entity["aliases"]))


