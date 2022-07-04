"""
Test for parsing prescriptions into a tree
"""


import unittest
import yaml

from prescription_parser import prescriptions_to_tree
from yaml_manipulate import manipulate_yaml
from assets import PRESCR_BLOB_1, SRC_YAML_1, RESULT_YAML_1

class TestYamlManipulation(unittest.TestCase):

    def test_manipulate_yaml(self):
        """based on a rich example."""
        in_tree = yaml.load(SRC_YAML_1, Loader=yaml.Loader)
        #
        pr_lines = [
            l
            for l in PRESCR_BLOB_1.split('\n')
            if l
            if l[0] != '#'
        ]
        pr_tree = prescriptions_to_tree(pr_lines)
        result_tree = manipulate_yaml(in_tree, pr_tree)
        #
        check_loaded = yaml.load(RESULT_YAML_1, Loader=yaml.Loader)
        self.assertEqual(result_tree, check_loaded)
