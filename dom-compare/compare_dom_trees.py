from argparse import ArgumentParser
from collections import deque
from DOMNode import DOMNode, ConstructDOMNodeObj

import json

# Skip these tags.
TAGS_TO_SKIP = [ 'head', '#comment', '#text', 'noscript' ]

def Main():
    # Flags to keep track of the state of the matching.
    matched = True
    a_greater = False
    b_greater = False

    dom_a = GetDOMTree(args.dom_tree_a)
    dom_b = GetDOMTree(args.dom_tree_b)

    children_a = deque([ dom_a ])
    children_b = deque([ dom_b ])
    a_nodes_count = 1
    b_nodes_count = 1
    while len(children_a) > 0 and len(children_b) > 0:
        # Perform BFS on the DOM tree.
        cur_node_a_json = children_a.popleft()
        while ShouldSkipNode(cur_node_a_json):
            cur_node_a_json = children_a.popleft()

        cur_node_b_json = children_b.popleft()
        while ShouldSkipNode(cur_node_b_json):
            cur_node_b_json = children_b.popleft()

        cur_node_a = ConstructDOMNodeObj(cur_node_a_json)
        cur_node_b = ConstructDOMNodeObj(cur_node_b_json)

        if not CompareNodes(cur_node_a, cur_node_b):
            matched = False
            PrintUnmatchedNodes(cur_node_a, cur_node_b)

        # Add all children of A and B
        if 'children' in cur_node_a_json:
            children_a.extend(cur_node_a_json['children'])
            a_nodes_count += len(cur_node_a_json['children'])
        if 'children' in cur_node_b_json:
            children_b.extend(cur_node_b_json['children'])
            b_nodes_count += len(cur_node_b_json['children'])

    if matched:
        print 'Comparison DONE. The DOM Trees matched!'

    # Print stats.
    print 'DOM A count: {0}'.format(a_nodes_count)
    print 'DOM B count: {0}'.format(b_nodes_count)


def ShouldSkipNode(node_json):
    '''
    Returns whether the given node should be skipped based on the tag name.
    '''
    for tag in TAGS_TO_SKIP:
        if node_json['nodeName'].lower() == tag.lower():
            return True
    return False


def CompareNodes(node_a, node_b):
    '''
    Returns true if node_a and node_b are equal in some way: structurally or the whole node.
    '''
    if args.only_structure:
        return node_a.CompareStructure(node_b)
    return node_a == node_b


def PrintNodes(nodes):
    '''
    Print all given nodes.
    '''
    for i, n in enumerate(nodes):
        print '{0} {1}'.format(i, ConstructDOMNodeObj(n))


def AdvanceToNextMatch(node_should_exists, remaining_nodes):
    '''
    Removes nodes until the first node matches node_should_exists.
    '''
    while ConstructDOMNodeObj(remaining_nodes[0]) != node_should_exists:
        remaining_nodes.popleft()


def PrintUnmatchedNodes(node_a, node_b):
    print 'Nodes not matching:\n{0}{1}'.format(node_a, node_b)


def GetDOMTree(dom_tree_filename):
    '''
    Parses the dom tree file and returns the DOM tree representation.
    '''
    with open(dom_tree_filename, 'r') as input_file:
        dom_json = json.loads(input_file.read())
        return dom_json['result']['root']


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dom_tree_a')
    parser.add_argument('dom_tree_b')
    parser.add_argument('--only-structure', default=False, action='store_true')
    parser.add_argument('--hdp', default=False, action='store_true')
    args = parser.parse_args()

    if args.hdp:
        TAGS_TO_SKIP.append('script')
    Main()
