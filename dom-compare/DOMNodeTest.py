from DOMNode import DOMNode, ConstructDOMNodeObj

import unittest
import json

class TestDOMNode(unittest.TestCase):

    def test_compare(self):
        """
        Tests the comparison function for the DOMNode object.
        """
        node = DOMNode(1, 'div', 'value', {})
        self.assertEqual(node, node)

        node_1 = DOMNode(1, 'div1', 'value', {})
        self.assertNotEqual(node, node_1)

        node_2 = DOMNode(2, 'div', 'value', { "abbc": "bbcc" })
        self.assertNotEqual(node, node_1)

        node_3 = DOMNode(3, 'div', 'value', { "abbc": "bbcc" })
        self.assertNotEqual(node, node_3)
        self.assertEqual(node_2, node_3)


    def test_construct_node(self):
        '''
        Tests the construction of a node.
        '''
        dom_json = json.loads('{"nodeId":5,"parentId":4,"backendNodeId":12,"nodeType":1,"nodeName":"TITLE","localName":"title","nodeValue":"","childNodeCount":1,"children":[{"nodeId":6,"parentId":5,"backendNodeId":13,"nodeType":3,"nodeName":"#text","localName":"","nodeValue":"LiveScore Soccer : Live Soccer Scores by LiveScore.com"}],"attributes":[]}')
        got = ConstructDOMNodeObj(dom_json)
        expected = DOMNode(5, "title", "LiveScore Soccer : Live Soccer Scores by LiveScore.com", {})
        self.assertEquals(got, expected)


if __name__ == '__main__':
    unittest.main()
