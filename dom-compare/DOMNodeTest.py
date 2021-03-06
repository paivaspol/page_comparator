from DOMNode import DOMNode, ConstructDOMNodeObj, ConstructSignature

import unittest
import json

class TestDOMNode(unittest.TestCase):

    def test_compare(self):
        """
        Tests the comparison function for the DOMNode object.
        """
        node = DOMNode(1, 'div', 'value', {}, 1, '')
        self.assertEqual(node, node)

        node_1 = DOMNode(1, 'div1', 'value', {}, 1, '')
        self.assertNotEqual(node, node_1)

        node_2 = DOMNode(2, 'div', 'value', { "abbc": "bbcc" }, 1, '')
        self.assertNotEqual(node, node_1)

        node_3 = DOMNode(3, 'div', 'value', { "abbc": "bbcc" }, 1, '')
        self.assertNotEqual(node, node_3)
        self.assertEqual(node_2, node_3)


    def test_construct_node(self):
        '''
        Tests the construction of a node.
        '''
        dom_json = json.loads('{"nodeId":5,"parentId":4,"backendNodeId":12,"nodeType":1,"nodeName":"TITLE","localName":"title","nodeValue":"","childNodeCount":1,"children":[{"nodeId":6,"parentId":5,"backendNodeId":13,"nodeType":3,"nodeName":"#text","localName":"","nodeValue":"LiveScore Soccer : Live Soccer Scores by LiveScore.com"}],"attributes":[]}')
        got = ConstructDOMNodeObj(dom_json, '')
        expected = DOMNode(5, "title", "LiveScore Soccer : Live Soccer Scores by LiveScore.com", {}, 1, '')
        self.assertEquals(got, expected)


    def test_serialize(self):
        '''
        Test serializing the node.
        '''
        dom_str = '{"nodeId":5,"parentId":4,"backendNodeId":12,"nodeType":1,"nodeName":"title","localName":"title","nodeValue":"","childNodeCount":1,"children":[],"attributes":[]}'
        dom_json = json.loads(dom_str)
        node_obj = ConstructDOMNodeObj(dom_json, '')
        expected = '{"nodeId":5,"parentId":4,"nodeName":"title","nodeValue":"","children":[],"attributes":[]}'
        got = json.dumps(node_obj.Serialize())
        self.assertEquals(json.loads(got), json.loads(expected))


    def test_construct_signature(self):
        '''
        Test constructing the signature of the node.
        '''
        dom_json = json.loads('{"nodeId":5,"parentId":4,"backendNodeId":12,"nodeType":1,"nodeName":"title","localName":"title","nodeValue":"","childNodeCount":1,"children":[{"nodeId":6,"parentId":5,"backendNodeId":13,"nodeType":3,"nodeName":"#text","localName":"","nodeValue":"LiveScore Soccer : Live Soccer Scores by LiveScore.com"}],"attributes":[]}')
        signature = ConstructSignature(dom_json)
        expected = '<title>[]'
        self.assertEquals(signature, expected)


if __name__ == '__main__':
    unittest.main()
