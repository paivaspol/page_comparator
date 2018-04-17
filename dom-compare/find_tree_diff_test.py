from DOMNode import DOMNode, ConstructDOMNodeObj

import find_tree_diff
import unittest

class TestDOMNode(unittest.TestCase):

    def test_common_nodes_same_nodes(self):
        # Simple case: same DOM nodes
        test = [ DOMNode(2, 'div', 'value', { "abbc": "bbcc" }, -1, ''), DOMNode(2, 'div', 'value', { "abbc": "abbc" }, -1, '') ]
        common_nodes, _, _ = find_tree_diff.FindCommonNodes(test, test)
        for n in common_nodes:
            print n
        
        self.assertEquals(len(test), len(common_nodes))

        for i in range(0, len(test)):
            self.assertEquals(test[i], common_nodes[i])


    def test_single_node_same(self):
        # Degenerative case: single node and same nodes
        test = [ DOMNode(2, 'div', 'value', { "abbc": "bbcc" }, -1, '') ]
        common_nodes, _, _ = find_tree_diff.FindCommonNodes(test, test)
        
        self.assertEquals(len(test), len(common_nodes))

        for i in range(0, len(test)):
            self.assertEquals(test[i], common_nodes[i])


    def test_single_node_different(self):
        # Degenerative case: single node and same nodes
        test1 = [ DOMNode(2, 'div', 'value', { "abbc": "bbcc" }, -1, '') ]
        test2 = [ DOMNode(2, 'div', 'value', { "abbc": "bbccaa" }, -1, '') ]

        expected = []
        common_nodes, _, _ = find_tree_diff.FindCommonNodes(test1, test2)
        
        self.assertEquals(0, len(common_nodes))


    def test_extra_nodes(self):
        # Common case: find the common longest nodes.
        test1 = [ 
            DOMNode(1, 'div', 'value', { "abbc": "a" }, -1, ''), \
            DOMNode(2, 'div', 'value', { "abbc": "b" }, -1, ''), \
            DOMNode(3, 'div', 'value', { "abbc": "c" }, -1, ''), \
            DOMNode(4, 'div', 'value', { "abbc": "d" }, -1, ''), \
            DOMNode(5, 'div', 'value', { "abbc": "g" }, -1, ''), \
        ]
        test2 = [ 
            DOMNode(1, 'div', 'value', { "abbc": "a" }, -1, ''), \
            DOMNode(2, 'div', 'value', { "abbc": "b" }, -1, ''), \
            DOMNode(3, 'div', 'value', { "abbc": "e" }, -1, ''), \
            DOMNode(4, 'div', 'value', { "abbc": "d" }, -1, ''), \
            DOMNode(4, 'div', 'value', { "abbc": "f" }, -1, ''), \
        ]
        expected = [
            DOMNode(1, 'div', 'value', { "abbc": "a" }, -1, ''), \
            DOMNode(2, 'div', 'value', { "abbc": "b" }, -1, ''), \
            DOMNode(4, 'div', 'value', { "abbc": "d" }, -1, ''), \
        ]

        common_nodes, _, _ = find_tree_diff.FindCommonNodes(test1, test2)
        self.assertEquals(len(expected), len(common_nodes))

        for i in range(0, len(expected)):
            self.assertEquals(expected[i], common_nodes[i])

    def test_lcs_producing_nones(self):
        # This case is extracted from an actual run where the resulting nodes
        # are all None.
        dom1 = [
            DOMNode(795, 'div', '', { 'class': 'tr-card card card--featured   card--aligned    tr-card-30-feature' }, -1, ''),
            DOMNode(814, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-31-featured' }, -1, ''),
            DOMNode(829, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-32-feature' }, -1, ''),
            DOMNode(844, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-33-feature' }, -1, ''),
            DOMNode(859, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-34-feature' }, -1, ''),
            DOMNode(878, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-35-feature' }, -1, ''),
        ]
        dom2 = [
            DOMNode(774, 'div', '', { 'class': 'tr-card card card--featured   card--aligned    tr-card-29-feature' }, -1, ''),
            DOMNode(793, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-30-feature' }, -1, ''),
            DOMNode(808, 'div', '', { 'class': 'tr-card card card--featured tr-card-vid card--video  card--aligned    tr-card-31-featured' }, -1, ''),
            DOMNode(835, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-32-feature' }, -1, ''),
            DOMNode(850, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-33-feature' }, -1, ''),
            DOMNode(865, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-34-feature' }, -1, ''),
        ]

        common_nodes, _, _ = find_tree_diff.FindCommonNodes(dom1, dom2, debug=True)

        expected = [
            DOMNode(829, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-32-feature' }, -1, ''),
            DOMNode(844, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-33-feature' }, -1, ''),
            DOMNode(859, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-34-feature' }, -1, ''),
        ]

        self.assertEquals(len(expected), len(common_nodes))
        self.assertFalse(None in common_nodes)
        for i in range(0, len(expected)):
            self.assertEquals(expected[i], common_nodes[i])


    def test_missing_nodes(self):
        print 'TEST_MISSING_NODES'
        dom1 = [
            DOMNode(795, 'div', '', { 'class': 'tr-card card card--featured   card--aligned    tr-card-30-feature' }, -1, ''),
            DOMNode(814, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-31-featured' }, -1, ''),
            DOMNode(829, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-32-feature' }, -1, ''),
            DOMNode(844, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-33-feature' }, -1, ''),
            DOMNode(859, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-34-feature' }, -1, ''),
            DOMNode(878, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-35-feature' }, -1, ''),
        ]
        dom2 = [
            DOMNode(774, 'div', '', { 'class': 'tr-card card card--featured   card--aligned    tr-card-29-feature' }, -1, ''),
            DOMNode(793, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-30-feature' }, -1, ''),
            DOMNode(808, 'div', '', { 'class': 'tr-card card card--featured tr-card-vid card--video  card--aligned    tr-card-31-featured' }, -1, ''),
            DOMNode(835, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-32-feature' }, -1, ''),
            DOMNode(850, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-33-feature' }, -1, ''),
            DOMNode(865, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-34-feature' }, -1, ''),
        ]

        expected = [
            DOMNode(795, 'div', '', { 'class': 'tr-card card card--featured   card--aligned    tr-card-30-feature' }, -1, ''),
            DOMNode(814, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-31-featured' }, -1, ''),
            DOMNode(878, 'div', '', { 'class': 'tr-card card    card--aligned    tr-card-35-feature' }, -1, ''),
        ]

        common_nodes, _, missing_nodes = find_tree_diff.FindCommonNodes(dom1, dom2, debug=True)
        print 'COMMON:'
        for n in common_nodes:
            print n
        print 'MISSING:'
        for n in missing_nodes:
            print n
        self.assertEquals(len(expected), len(missing_nodes))
        self.assertFalse(None in missing_nodes)
        for i in range(0, len(expected)):
            self.assertEquals(expected[i], missing_nodes[i])


if __name__ == '__main__':
    unittest.main()
