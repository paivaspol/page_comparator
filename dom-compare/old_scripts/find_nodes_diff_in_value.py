from argparse import ArgumentParser
from collections import defaultdict
from DOMNode import DOMNode, ConstructDOMNodeObj
from DOMTree import DOMTree

import utils

def Main():
    dom_a = utils.GetDOMTree(args.dom_tree_a, args.hdp)
    dom_b = utils.GetDOMTree(args.dom_tree_b, args.hdp)
    dom_b_structure = ConstructStructureMap(dom_b)

    # Counters
    value_diff = 0

    # Go through DOM Tree A and find nodes that do not match.
    # When the node does not match, try to see whether it is
    # just the value or something else.
    for n in iter(dom_a):
        if dom_b.Contains(n):
            # Ignore ones that matches
            continue
        n_hash_val = n.ComputeStructureHash()

        # ComputeStructureHash() is computed from n.type and n.attrs.
        if n_hash_val in dom_b_structure:
            print n
            print '============================='
            value_diff +=1  

        # for other_n in nodes:
        #     if not (n.type == other_n.type and n.attributes == other_n.attributes):
        #         # The structure does not match
        #         continue
        #     
        #     if n.value == other_n.value:
        #         # The value matches.
        #         continue
        #     
        #     print 'A:'
        #     print n
        #     print 'B:'
        #     print other_n
        #     print '================================='
        #     value_diff += 1

    print '{0} {1}'.format(value_diff, dom_a.size)


def ConstructStructureMap(dom_tree):
    '''
    Returns a hashtable of the DOM nodes.

    This is for finding the number of nodes that have the same structure,
    but different values.
    '''
    structure_map = defaultdict(list)
    for n in iter(dom_tree):
        # Note: not using the actual hash because we want only
        # the structure to match
        structure_map[n.ComputeStructureHash()].append(n)
    return structure_map


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dom_tree_a')
    parser.add_argument('dom_tree_b')
    parser.add_argument('--hdp', default=False, action='store_true')
    args = parser.parse_args()
    Main()
