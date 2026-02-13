import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()