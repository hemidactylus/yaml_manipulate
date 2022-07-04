"""
Test for parsing prescriptions into a tree
"""

import unittest
import json

from prescription_parser import prescriptions_to_tree
from assets import PRESCR_BLOB_1, PRESCR_RESULT_TREE_JSON_1


class TestPrescriptionParsing(unittest.TestCase):

    def test_parse_prescriptions(self):
        """based on a rich example."""
        pr_lines = [
            l
            for l in PRESCR_BLOB_1.split('\n')
            if l
            if l[0] != '#'
        ]
        #
        result = prescriptions_to_tree(pr_lines)
        #
        self.assertEqual(result, json.loads(PRESCR_RESULT_TREE_JSON_1))
