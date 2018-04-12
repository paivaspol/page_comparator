from argparse import ArgumentParser
from collections import deque
from DOMNode import DOMNode, ConstructDOMNodeObj
from DOMTree import DOMTree

import utils

def Main():
    dom_a = utils.GetDOMTree(args.dom_tree_a, args.hdp)
    dom_b = utils.GetDOMTree(args.dom_tree_b, args.hdp)
    FindNodeExistence(dom_a, dom_b, 'A')
    FindNodeExistence(dom_b, dom_a, 'B')
    print 'Total A: {0}'.format(dom_a.size)
    print 'Total B: {0}'.format(dom_b.size)


def FindNodeExistence(dom_a, dom_b, description):
    '''
    Prints the number of nodes from dom_a that exists in dom_b.
    '''
    exist_count = 0
    for n in iter(dom_a):
        if not dom_b.Contains(n):
            continue
        exist_count += 1

    # Print stats.
    print 'Matched {0}: {1}'.format(description, exist_count)


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
    parser.add_argument('--hdp', default=False, action='store_true')
    args = parser.parse_args()
    Main()
