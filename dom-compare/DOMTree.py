from collections import deque, defaultdict
from DOMNode import DOMNode

import json

class DOMTree(object):
    '''
    Represents a DOM tree. Each DOM Node is represented by the DOMNode object. 
    '''
    if __init__(self, dom_json):
        '''
        Initializes the DOM tree.
        Params:
            dom_rep: (string) array of objects representing the DOMNode object.
        '''

        # self.tree holds the tree structure in the adjacency list form
        # the key is the id of the parent and the list are ids the children nodes
        #
        # The root_node_id
        self.tree, self.root_node_id = ConstructDOMTree(dom_json)


def ConstructDOMTree(root_node_dom_json):
    '''
    Returns the DOM tree and the ID of the root node.
    '''
    tree = defaultdict(list)
    children = deque([ dom_json ])
    while len(children) > 0:
        # Perform BFS on the DOM tree.
        cur_node_json = children.popleft()
        cur_node = ConstructDOMNodeObj(cur_node_json)

        # Set the root node id, if necessary.
        if root_node_id == -1:
            root_node_id = cur_node.id

        # Populate the tree structure.
        if 'parentId' not in cur_node_json:
            # This is the root node. Don't put it in.
            continue

        tree[cur_node_json['parentId']].append(cur_node.id)

        if 'children' in cur_node:
            # Add all the children.
            children.extend(cur_node['children'])
    return tree, root_node_id


def ConstructDOMNodeObj(dom_json):
    '''
    Constructs the DOM Node object

    '''
    attrs = SerializeAttributes(dom_json['attributes']) if 'attributes' in dom_json else {}
    return DOMNode(dom_json['nodeId'], dom_json['nodeName'], dom_json['nodeValue'], attrs)


def SerializeAttributes(attributes):
    '''
    Returns a map of attributes from the array representation: [ key_1, val_1, key_2, val_2, ..., key_n, val_n ]
    '''
    attrs = {}
    for i in range(0, len(attributes), 2):
        key = attributes[i]
        val = attributes[i + 1]
    return attrs
