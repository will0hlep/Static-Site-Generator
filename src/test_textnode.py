import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("Thisis a text_node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        node5 = TextNode("This is a text node", TextType.BOLD, 'https://www.boot.dev')
        node6 = TextNode("This is a text node", TextType.BOLD, 'https://www.boot.dev')
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)
        self.assertEqual(node5, node6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        node3 = TextNode("This is a text node", TextType.CODE)
        node4 = TextNode("This is a text node", TextType.LINK, {"href": "www.boot.dev"})
        node5 = TextNode(None, TextType.IMAGE, {
                             "src": "www.boot.dev",
                             "alt": "This is a text node"
                             })
        
        html_node = text_node_to_html_node(node)
        html_node1 = text_node_to_html_node(node1)
        html_node2 = text_node_to_html_node(node2)
        html_node3 = text_node_to_html_node(node3)
        html_node4 = text_node_to_html_node(node4)
        html_node5 = text_node_to_html_node(node5)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node1.tag, 'b')
        self.assertEqual(html_node2.tag, 'i')
        self.assertEqual(html_node3.tag, 'code')
        self.assertEqual(html_node4.tag, 'a')
        self.assertEqual(html_node5.tag, 'img')

        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node1.value, "This is a text node")
        self.assertEqual(html_node2.value, "This is a text node")
        self.assertEqual(html_node3.value, "This is a text node")
        self.assertEqual(html_node4.value, "This is a text node")
        self.assertEqual(html_node5.value, None)

if __name__ == "__main__":
    unittest.main()