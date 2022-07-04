# Prescriptions -> data structure
from dict_utils import dict_merge


def is_integer(v):
    try:
        int(v)
        return True
    except Exception:
        return False


def is_decimal(v):
    try:
        float(v)
        return True
    except Exception:
        return False


def guess_type(r_value):
    """
    We *have* to accept string-only prescription and somehow typify them,
    in order to allow for booleans, numeric, strings. Alas.
    This is a delicate piece, as it may make it hard/impossible
    to insert strings such as "true" or "0.123". For now we go the direct way.
    (reminds of https://www.bram.us/2022/01/11/yaml-the-norway-problem/)

    Input to this function is a string.
    """
    if r_value == '':
        return None
    # Booleans, here we are manually stricter than the yaml specs
    if r_value.lower() == 'false':
        return False
    elif r_value.lower() == 'true':
        return True
    # numbers, then fallback to strings
    elif is_integer(r_value):
        return int(r_value)
    elif is_decimal(r_value):
        return float(r_value)
    #
    return r_value


def parse_prescriptions(pr_lines):

    def _parse_path_item(pi):
        if pi == '[]':
            return {
                'type': 'index',
                'value': None,
            }
        elif len(pi) > 2 and pi[0] == '[' and pi[-1] ==']':
            return {
                'type': 'index',
                'value': int(pi[1:-1]),
            }
        else:
            return {
                'type': 'key',
                'value': pi,
            }

    def _parse_line(l):
        pieces = l.strip().split('=')
        assert(len(pieces) == 2)
        kp, raw_v = pieces
        pth = [
            _parse_path_item(k)
            for k in kp.split('.')
        ]
        typed_v = guess_type(raw_v)
        return (pth, typed_v)

    paths_values = [
        _parse_line(pr_line)
        for pr_line in pr_lines
        if pr_line.strip()
    ]

    return paths_values


def paths_values_to_tree(paths_values):

    def _prescription_to_dict(path, value, g_counter):
        if path:
            this_path_item, next_path = path[0], path[1:]
            #
            if this_path_item['type'] == 'index':
                if this_path_item['value'] is None:
                    this_key = g_counter
                    n_counter = g_counter + 1
                else:
                    this_key = this_path_item['value']
                    n_counter = g_counter
            elif this_path_item['type'] == 'key':
                this_key = this_path_item['value']
                n_counter = g_counter
            #
            this_val, n2_counter = _prescription_to_dict(
                next_path,
                value,
                n_counter,
            )
            return {this_key: this_val}, n2_counter
        else:
            return value, g_counter

    def _chain_pathvalues(pvs, tree, g_counter):
        if pvs:
            this_path_val, this_val = pvs[0]
            next_pvs = pvs[1:]
            base_dict, n_counter = _prescription_to_dict(
                this_path_val,
                this_val,
                g_counter,
            )
            return _chain_pathvalues(
                next_pvs,
                dict_merge(
                    base_dict,
                    tree,
                ),
                n_counter,
            )
        else:
            return tree, g_counter


    tree, _ = _chain_pathvalues(paths_values, {}, 100)
    return tree


def raw_to_indexed_tree(r_tree, c_path=[]):
    if isinstance(r_tree, dict):
        # check indexing and apply fixes
        if all(type(k) is str for k in r_tree.keys()):
            # includes empty dict case
            return {
                k: raw_to_indexed_tree(v, c_path + [k])
                for k, v in r_tree.items()
            }
        elif all(type(k) is int for k in r_tree.keys()):
            # we sort items and make a list out of them, then process items
            return [
                raw_to_indexed_tree(v, c_path + ['[%i]' % l_index])
                for l_index, (k, v) in enumerate(sorted(
                    r_tree.items()
                ))
            ]
        else:
            raise ValueError('Mixed-type-tree error at %s' % ('.'.join(c_path)))
    elif isinstance(r_tree, list):
        return [
            raw_to_indexed_tree(l_item, c_path + ['[%i]' % l_index])
            for l_index, l_item in enumerate(r_tree)
        ]
    else:
        return r_tree


def prescriptions_to_tree(pr_lines):
    paths_values = parse_prescriptions(pr_lines)
    raw_tree = paths_values_to_tree(paths_values)
    indexed_tree = raw_to_indexed_tree(raw_tree)
    return indexed_tree


if __name__ == '__main__':
    import sys
    import json
    #
    in_file = sys.argv[1]
    out_json = sys.argv[2]
    pr_lines = [
        l
        for l in open(in_file).readlines()
        if l
        if l[0] != '#'
    ]
    #
    result = prescriptions_to_tree(pr_lines)
    #
    print('=== %s :' % in_file)
    print(json.dumps(result, indent=2, sort_keys=True))
    assert(result == json.load(open(out_json)))
    print('=== MATCH')
