from argparse import ArgumentParser
from collections import deque
from DOMNode import DOMNode, ConstructDOMNodeObj
from DOMTree import DOMTree

import utils

def Main():
    # Flags to keep track of the state of the matching.
    matched = True

    dom_a = utils.GetDOMTree(args.dom_tree_a, args.hdp)
    dom_b = utils.GetDOMTree(args.dom_tree_b, args.hdp)

    iters = min(dom_a.size, dom_b.size)
    try:
        for i in range(0, iters):
            cur_node_a = dom_a.next()
            cur_node_b = dom_b.next()
            if not CompareNodes(cur_node_a, cur_node_b):
                 matched = False
                 PrintUnmatchedNodes(cur_node_a, cur_node_b)
    except Exception:
        pass

    if matched:
        print 'MATCHED'
    else:
        print 'NOT MATCHED'

    # Print stats.
    print 'DOM A count: {0}'.format(dom_a.size)
    print 'DOM B count: {0}'.format(dom_b.size)


def CompareNodes(node_a, node_b):
    '''
    Returns true if node_a and node_b are equal in some way: structurally or the whole node.
    '''
    if args.only_structure:
        return node_a.CompareStructure(node_b)
    return node_a == node_b


def PrintUnmatchedNodes(node_a, node_b):
    if args.mute_output:
        return
    print 'Nodes not matching:\n{0}{1}'.format(node_a, node_b)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dom_tree_a')
    parser.add_argument('dom_tree_b')
    parser.add_argument('--only-structure', default=False, action='store_true')
    parser.add_argument('--hdp', default=False, action='store_true')
    parser.add_argument('--mute-output', default=False, action='store_true')
    args = parser.parse_args()
    Main()
