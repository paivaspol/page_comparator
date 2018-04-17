from collections import deque, defaultdict
from DOMNode import DOMNode, ConstructDOMNodeObj, ConstructSignature

import json

# Skip these tags.
TAGS_TO_SKIP = { '#comment', '#text' }

class DOMTree(object):
    '''
    Represents a DOM tree. Each DOM Node is represented by the DOMNode object. 
    '''
    def __init__(self, dom_json, for_hdp=False):
        '''
        Initializes the DOM tree.
        Params:
            dom_rep: (string) array of objects representing the DOMNode object.
        '''
        if for_hdp:
            TAGS_TO_SKIP.add('script')

        # self.tree holds the tree structure in the adjacency list form
        # the key is the id of the parent and the list are ids the children nodes
        #
        # The root_node_id
        self.tree, self.root_node, self.size, self._nodes_set = ConstructDOMTree(dom_json, for_hdp)

        self.children = deque([ self.root_node ])


    def Contains(self, node):
        '''
        Returns whether the given node exists in this tree.
        '''
        return node in self._nodes_set


    def GetChildren(self, node_id):
        '''
        Returns the children of the given node_id.
        '''
        if node_id not in self.tree:
            return []
        return self.tree[node_id]


    def AddNode(self, parent_id, node):
        '''
        Adds a node to the DOM tree.

        Params:
            parent_id: the id of the parent.
            node: the node object to be added.
        '''
        if self.size == 0:
            # The tree is empty assume that this is the root node.
            self.root_node = node
            self.children = deque([ self.root_node ])
            self.size += 1
            return
        # Populate the tree.
        self.tree[parent_id].append(node)
        self.size += 1


    def Serialize(self):
        '''
        Serializes the tree into dictionary so that it can be serialized into JSON.
        '''
        return self.serialize_helper(self.root_node)


    def serialize_helper(self, cur_node):
        '''
        Recursive helper method for serializing the tree.
        '''
        serialized_cur_node = cur_node.Serialize()
        if cur_node.id in self.tree:
            children = self.tree[cur_node.id]
            for child in children:
                serialized_cur_node['children'].append(self.serialize_helper(child))
        return serialized_cur_node


    ############################################
    # Iterator implementation
    ############################################
    def __iter__(self):
        return self

    def next(self):
        '''
        Returns the next node in the breadth-first order.
        '''
        if len(self.children) == 0:
            # Nothing left to iterate over.
            raise StopIteration
        node = self.children.popleft()
        # Add more children
        if node.id in self.tree:
            self.children.extend(self.tree[node.id])
        return node


def ConstructDOMTree(root_node_dom_json, for_hdp):
    '''
    Returns the DOM tree and the ID of the root node.
    '''
    tree = defaultdict(list)
    node_count = 0
    root_node = None
    node_set = set()
    needs_processing = len(root_node_dom_json) > 0
    children = deque([ root_node_dom_json ])
    node_signature_map = defaultdict(lambda: '')

    while needs_processing and len(children) > 0:
        # Perform BFS on the DOM tree.
        cur_node_json = children.popleft()
        parent_signature = node_signature_map[cur_node_json['parentId']] if 'parentId' in cur_node_json else ''
        # Node signatures are delimited by ;
        node_signature = parent_signature + ConstructSignature(cur_node_json) + ';'
        cur_node = ConstructDOMNodeObj(cur_node_json, node_signature, for_hdp)

        # In HDP, we want to ignore all nodes that are not visible.
        if ShouldSkipNode(cur_node, for_hdp):
            continue

        # Start processing this node.
        node_count += 1

        if root_node is None:
            root_node = cur_node

        if 'children' in cur_node_json:
            # Add all the children.
            children.extend(cur_node_json['children'])

        node_set.add(cur_node)

        # Populate the tree structure.
        if 'parentId' not in cur_node_json:
            # This is the root node. Don't put it in.
            continue

        tree[cur_node_json['parentId']].append(cur_node)

    return tree, root_node, node_count, node_set


def ShouldSkipNode(node, for_hdp):
    '''
    Returns whether the given node should be skipped based on the tag name or 
    the visibility of the node.
    '''
    return node.type in TAGS_TO_SKIP or (for_hdp and not node.IsVisible())
