import yaml

from yaml_manipulate import manipulate_yaml
from prescription_parser import prescriptions_to_tree

if __name__ == '__main__':
    """
    Passing source-yaml and key-value pairs as input, result to STDOUT

    Syntax here:
        python yaml_manipulate2 SOURCE_YAML.yaml KEY1=VALUE1 KEY2=VALUE2 KEY3=VALUE3 ...
    Example:
        python yaml_manipulate2.py example/src1.yaml    \
            keyA=123                                    \
            keyP.keyQ.keyR=False                        \
            listA.[0]=mmm                               \
            listA.[1]=nnn                               \
            objlistA.[0].x=ics                          \
            objlistA.[0].y=ipsilon                      \
            objlistB.[]=bah                             \
            objlistB.[]=beh                             \
            objlistB.[]=bih                             \
            objsublistA.[0].[]=item1                    \
            objsublistA.[0].[]=item2                    \
            objsublistB.[0].attr.[]=item1               \
            objsublistB.[0].attr.[]=item2               \
            sublistA.subkey.[]=1119                     \
            sublistA.subkey.[]=1121.1211                \
            deleted1=                                   \
            deleted2.subdeleted=                        \
            > out/out2.yaml
    """
    import sys
    import os
    in_yaml_file = sys.argv[1]
    raw_prescriptions = sys.argv[2:]
    #
    in_tree = yaml.load(open(in_yaml_file), Loader=yaml.Loader)
    pr_lines = [
        l
        for l in raw_prescriptions
    ]
    #
    pr_tree = prescriptions_to_tree(pr_lines)
    result_tree = manipulate_yaml(in_tree, pr_tree)
    #
    dumped = yaml.dump(result_tree, default_flow_style=False)
    print(dumped)
