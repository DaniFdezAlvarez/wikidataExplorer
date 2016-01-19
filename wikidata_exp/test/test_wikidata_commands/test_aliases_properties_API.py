__author__ = 'Dani'

from wdexp.wikidata.commands.aliases_properties_API import AliasesPropertiesCommand
from wdexp.utils import rel_path_to_file
import unittest
import json



class TestAliasesTracker(unittest.TestCase):

    def test_aliases_slice(self):
        aliases_tracker = AliasesPropertiesCommand(out_file=rel_path_to_file("../files/out/complete_with_alias.txt",
                                                                             __file__),
                                                   source_file=rel_path_to_file("../files/in/complete.txt",
                                                                                __file__))

        result = aliases_tracker.exec_command(string_return=True)
        result_json = json.loads(result)
        self.assertEqual(50, len(result_json))


        self.assertEqual(4, len(result_json[0]))
        self.assertEqual(4, len(result_json[1]))
        self.assertEqual(4, len(result_json[2]))
        self.assertEqual(4, len(result_json[49]))


        self.assertEqual('P31', result_json[0]["id"])
        self.assertEqual("P17", result_json[1]["id"])
        self.assertEqual("P21", result_json[2]["id"])
        self.assertEqual("P685", result_json[49]["id"])

        self.assertEqual("instance of", result_json[0]["label"])
        self.assertEqual("country", result_json[1]["label"])
        self.assertEqual("sex or gender", result_json[2]["label"])
        self.assertEqual("NCBI Taxonomy ID", result_json[49]["label"])
