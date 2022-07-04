# convert a base-yaml + prescription to a destination yaml
import yaml

from prescription_parser import prescriptions_to_tree
from dict_utils import dict_merge, dict_prune_nulls


def manipulate_yaml(base_tree, alteration_tree):
    """
    Merge alterations onto the base tree,
    and also take care of pruning resulting nulls
    to effect key deletions.
    """
    merged = dict_merge(alteration_tree, default=base_tree)
    pruned = dict_prune_nulls(merged)
    return pruned


if __name__ == '__main__':
    #
    # usage so far:
    #   python yaml_manipulate [src_yaml] [prescription_file] [out_file_must_not_exist]
    # e.g.:
    #   python yaml_manipulate.py example/src1.yaml example/prescr1.txt out/out1.yaml
    #
    import sys
    import os
    in_yaml_file = sys.argv[1]
    prescriptions_file = sys.argv[2]
    out_yaml_file = sys.argv[3]
    in_tree = yaml.load(open(in_yaml_file), Loader=yaml.Loader)
    pr_lines = [
        l
        for l in open(prescriptions_file).readlines()
        if l
        if l[0] != '#'
    ]
    #
    pr_tree = prescriptions_to_tree(pr_lines)
    result_tree = manipulate_yaml(in_tree, pr_tree)
    #
    dumped = yaml.dump(result_tree, default_flow_style=False)
    if os.path.isfile(out_yaml_file):
        print('** OUT FILE EXISTS, DUMPING TO STDOUT **')
        print(dumped)
    else:
        with open(out_yaml_file, 'w') as of:
            of.write('%s\n' % dumped)
