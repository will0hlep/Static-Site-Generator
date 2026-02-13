import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node_props = {
                      "href": "https://www.google.com",
                      "target": "_blank",
                      }
        node = HTMLNode(props = node_props)
        node2 = HTMLNode()
        node3 = HTMLNode(props = {})
        expected_output = 'href="https://www.google.com" target="_blank"'
        expected_output2 = ''
        expected_output3 = ''
        self.assertEqual(node.props_to_html(), expected_output)
        self.assertEqual(node2.props_to_html(), expected_output2)
        self.assertEqual(node3.props_to_html(), expected_output3)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("3", None)
        with self.assertRaises(ValueError):
            node2.to_html()
        node3 = LeafNode(None, 5)
        self.assertEqual(node3.to_html(), 5)
        node4 = LeafNode("z", "Nopee", {"href": "https://www.boot.dev"})
        self.assertEqual(node4.to_html(), '<z href="https://www.boot.dev">Nopee</z>')

if __name__ == "__main__":
    unittest.main()