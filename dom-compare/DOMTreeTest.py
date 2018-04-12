from DOMTree import DOMTree

import unittest
import json

class TestDOMTree(unittest.TestCase):

    def test_iteration(self):
        '''
        Test iteration
        '''
        node_ids = [ 1, 2 ]
        dom_json = json.loads('{"nodeId":1,"parentId":4,"backendNodeId":12,"nodeType":1,"nodeName":"TITLE","localName":"title","nodeValue":"","childNodeCount":1,"children":[{"nodeId":2,"parentId":5,"backendNodeId":13,"nodeType":3,"nodeName":"#text","localName":"","nodeValue":"LiveScore Soccer : Live Soccer Scores by LiveScore.com"}],"attributes":[]}')
        tree = DOMTree(dom_json)
        for i, n in enumerate(iter(tree)):
            self.assertEqual(node_ids[i], n.id)


if __name__ == '__main__':
    unittest.main()