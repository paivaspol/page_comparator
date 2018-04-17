from DOMTree import DOMTree

import unittest
import json

class TestDOMTree(unittest.TestCase):

    def test_iteration(self):
        '''
        Test iteration
        '''
        node_ids = [ 1, 2 ]
        dom_json = json.loads('{"nodeId":1,"backendNodeId":12,"nodeType":1,"nodeName":"TITLE","localName":"title","nodeValue":"","childNodeCount":1,"children":[{"nodeId":2,"parentId":5,"backendNodeId":13,"nodeType":3,"nodeName":"#text","localName":"","nodeValue":"LiveScore Soccer : Live Soccer Scores by LiveScore.com"}],"attributes":[]}')
        tree = DOMTree(dom_json)
        for i, n in enumerate(iter(tree)):
            self.assertEqual(node_ids[i], n.id)


    def test_empty_tree(self):
        '''
        Test the degenerate case of empty tree.
        '''
        dom_json = json.loads('{}')
        tree = DOMTree(dom_json)
        self.assertEqual(0, tree.size)


    def test_signature(self):
        '''
        Test iteration
        '''
        dom_json = json.loads('{"nodeId":1,"backendNodeId":12,"nodeType":1,"nodeName":"TITLE","localName":"title","nodeValue":"","childNodeCount":1,"children":[{"nodeId":2,"parentId":5,"backendNodeId":13,"nodeType":3,"nodeName":"div","localName":"","nodeValue":"","attributes":["key","val"]}],"attributes":[]}')
        signatures = [
                '<TITLE>[];',
                '<TITLE>[];<div>["key","val"]'
        ]
        tree = DOMTree(dom_json)
        for i, n in enumerate(iter(tree)):
            self.assertEqual(signatures[i], n.signature)


if __name__ == '__main__':
    unittest.main()
