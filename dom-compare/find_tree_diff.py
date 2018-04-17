from argparse import ArgumentParser
from collections import deque
from DOMNode import DOMNode, ConstructDOMNodeObj
from DOMTree import DOMTree

import json
import utils

def Main():
    dom_a = utils.GetDOMTree(args.dom_tree_a, args.hdp)
    dom_b = utils.GetDOMTree(args.dom_tree_b, args.hdp)

    # Assume that DOM B is the corrent DOM Tree.
    correct_dom = dom_b
    testing_dom = dom_a

    queued_correct_common_nodes = deque([ correct_dom.root_node ])
    queued_testing_common_nodes = deque([ testing_dom.root_node ])
    
    # Check root_node. degenerative case:
    if correct_dom.root_node != testing_dom.root_node:
        print 'NOTHING MATCHED!'

    # Populate the root node.
    common_dom_tree = DOMTree({})
    common_dom_tree.AddNode(-1, correct_dom.root_node)
    all_missing_nodes = []
    while len(queued_correct_common_nodes) > 0 and len(queued_testing_common_nodes) > 0:
        correct_front = queued_correct_common_nodes.popleft()
        correct_nodes_children = correct_dom.GetChildren(correct_front.id)

        testing_front = queued_testing_common_nodes.popleft()
        testing_nodes_children = testing_dom.GetChildren(testing_front.id)

        if args.debug:
            print 'COMPARING:'
            print '\tcorrect: ' + str(len(correct_nodes_children))
            PrintNodeList(correct_nodes_children, indent='\t')
            print '\ttesting: ' + str(len(testing_nodes_children))
            PrintNodeList(testing_nodes_children, indent='\t')

        correct_common_nodes, testing_common_nodes, missing_nodes = FindCommonNodes(correct_nodes_children, testing_nodes_children, args.debug)
        queued_correct_common_nodes.extend(correct_common_nodes)
        queued_testing_common_nodes.extend(testing_common_nodes)
        all_missing_nodes.extend(missing_nodes)

        for n in correct_common_nodes:
            common_dom_tree.AddNode(correct_front.id, n)

        if args.debug:
            # print 'correct: ' + str(len(correct_common_nodes))
            # PrintNodeList(correct_common_nodes)
            # print 'queued: ' 
            # PrintNodeList(queued_correct_common_nodes)
            # print '================================================='
            pass
        
        if None in correct_common_nodes:
            break
    print '{0} {1}'.format(common_dom_tree.size, dom_a.size)
    if args.dump_common_tree is not None:
        with open(args.dump_common_tree, 'w') as output_file:
            output_file.write(json.dumps({ 'result': { 'root': common_dom_tree.Serialize() } }))

    if args.dump_missing_nodes is not None:
        with open(args.dump_missing_nodes, 'w') as output_file:
            for n in all_missing_nodes:
                output_file.write(n.signature + '\n')


def PrintNodeList(node_list, indent=''):
    for n in node_list:
        print indent + str(n)


def FindCommonNodes(correct_nodes, testing_nodes, debug=False):
    '''
    FindCommonNodes uses LCS to find the common nodes between the 
    same level of the DOM tree.

    Returns the longest commond DOM nodes for this level and the diffs of the nodes.
    '''
    c = SetupLCS(correct_nodes, testing_nodes, debug)
    correct_common_nodes = deque()
    testing_common_nodes = deque()
    missing_nodes = deque()

    # Find the missing nodes when there are common nodes.
    GetCommonAndMissingNodes(c, correct_nodes, testing_nodes, len(correct_nodes) - 1, len(testing_nodes) - 1, correct_common_nodes, testing_common_nodes, missing_nodes, debug)
    return correct_common_nodes, testing_common_nodes, missing_nodes


def SetupLCS(correct_nodes, testing_nodes, debug):
    '''
    Computes and returns the LCS 2-D array.
    '''
    # Setup the LCS array
    c = [[ 0 for x in range(len(testing_nodes) + 1) ] for y in range(len(correct_nodes) + 1) ]

    # Compute LCS
    # for i, correct_node in enumerate(correct_nodes):
    #     for j, testing_node in enumerate(testing_nodes):
    #         if NodesEqual(correct_node, testing_node):
    #             c[i + 1][j + 1] = c[i][j] + 1
    #         else:
    #             c[i + 1][j + 1] = max(c[i + 1][j], c[i][j + 1])
    for i, correct_node in enumerate(correct_nodes):
        for j, testing_node in enumerate(testing_nodes):
            if NodesEqual(correct_node, testing_node):
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i][j - 1], c[i - 1][j])
    
    if debug:
        PrintLCSArray(c)
    return c


def PrintLCSArray(c):
    print ''
    for i in xrange(len(c)):
        line = ''
        for j in xrange(len(c[i])):
            line += str(c[i][j]) + ' '
        print line


def GetCommonAndMissingNodes(lcs_arr, correct_nodes, testing_nodes, i, j, correct_common_nodes, testing_common_nodes, missing_nodes, debug):
    '''
    Returns the nodes that are missing from the correct nodes.
    '''
    if i < 0 and j < 0:
        pass
    elif i < 0:
        # print_diff(c, x, y, i, j-1)
        GetCommonAndMissingNodes(lcs_arr, correct_nodes, testing_nodes, i, j - 1, correct_common_nodes, testing_common_nodes, missing_nodes, debug)
    elif j < 0:
        missing_nodes.appendleft(correct_nodes[i])
        GetCommonAndMissingNodes(lcs_arr, correct_nodes, testing_nodes, i - 1, j, correct_common_nodes, testing_common_nodes,  missing_nodes, debug)
    elif NodesEqual(correct_nodes[i], testing_nodes[j]):
        correct_common_nodes.appendleft(correct_nodes[i])
        testing_common_nodes.appendleft(testing_nodes[j])
        GetCommonAndMissingNodes(lcs_arr, correct_nodes, testing_nodes, i - 1, j - 1, correct_common_nodes, testing_common_nodes, missing_nodes, debug)
    elif lcs_arr[i][j-1] >= lcs_arr[i-1][j]:
        GetCommonAndMissingNodes(lcs_arr, correct_nodes, testing_nodes, i, j - 1, correct_common_nodes, testing_common_nodes, missing_nodes, debug)
        # print("+ " + y[j])
    elif lcs_arr[i][j-1] < lcs_arr[i-1][j]:
        missing_nodes.appendleft(correct_nodes[i])
        GetCommonAndMissingNodes(lcs_arr, correct_nodes, testing_nodes, i - 1, j, correct_common_nodes, testing_common_nodes, missing_nodes, debug)


def NodesEqual(node_a, node_b):
    '''
    Returns true if node_a and node_b are equal in some way: structurally or the whole node.
    '''
    try:
        if args.only_structure:
            return node_a.CompareStructure(node_b)
    except:
        pass
    return node_a == node_b


def FindNodeIndex(target, nodes):
    '''
    Returns whether target is in the nodes list
    '''
    for i, n in enumerate(nodes):
        if n == target:
            return i
    return -1


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dom_tree_a')
    parser.add_argument('dom_tree_b')
    parser.add_argument('--hdp', default=False, action='store_true')
    parser.add_argument('--only-structure', default=False, action='store_true')
    parser.add_argument('--dump-common-tree', default=None)
    parser.add_argument('--dump-missing-nodes', default=None)
    parser.add_argument('--debug', default=False, action='store_true')
    args = parser.parse_args()
    Main()
