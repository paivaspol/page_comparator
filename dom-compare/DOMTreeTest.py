from DOMTree import DOMTree, SIGNATURE_DELIM
from DOMNode import DOMNode

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
                '<TITLE>[]' + SIGNATURE_DELIM,
                '<TITLE>[]' + SIGNATURE_DELIM + '<div>["key","val"]'
        ]
        tree = DOMTree(dom_json)
        for i, n in enumerate(iter(tree)):
            self.assertEqual(signatures[i], n.signature)


    def test_construct_dom_tree_from_html(self):
        '''
        Test constructing the DOM tree from the main HTML.
        '''
        html = '<html><head><link rel="preload" href="foo.js"></link></head><body><div>Hello world</div></body></html>'
        tree = DOMTree(html)
        expected = [
                DOMNode(0, '#document', '', {}, -1, ''),
                DOMNode(1, 'html', '', {}, 0, ''),
                DOMNode(2, 'head', '', {}, 1, ''),
                DOMNode(3, 'body', '', {}, 1, ''),
                DOMNode(4, 'link', '', { 'rel': 'preload', 'href': 'foo.js' }, 2, ''),
                DOMNode(5, 'div', 'Hello world', {}, 3, ''),
        ]
        self.assertEquals(6, tree.size)
        for i, n in enumerate(iter(tree)):
            self.assertEquals(expected[i], n)


if __name__ == '__main__':
    unittest.main()
