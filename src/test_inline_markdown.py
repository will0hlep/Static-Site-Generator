import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is a **text** node", TextType.TEXT)
        node1 = TextNode("This is a **text** node", TextType.BOLD)
        node2 = TextNode("This is a _text_ node", TextType.TEXT)
        node3 = TextNode("This is a `text` node", TextType.TEXT)

        self.assertEqual(
                         split_nodes_delimiter([node], '**', TextType.BOLD),
                         [
                          TextNode('This is a ', TextType.TEXT, None),
                          TextNode('text', TextType.BOLD, None),
                          TextNode(' node', TextType.TEXT, None)
                          ]
                         )
        self.assertEqual(
                         split_nodes_delimiter([node1], '**', TextType.BOLD),
                         [node1]
                         )
        self.assertEqual(
                         split_nodes_delimiter([node2], '_', TextType.ITALIC),
                         [
                          TextNode('This is a ', TextType.TEXT, None),
                          TextNode('text', TextType.ITALIC, None),
                          TextNode(' node', TextType.TEXT, None)
                          ]
                         )
        self.assertEqual(
                         split_nodes_delimiter([node3], '`', TextType.CODE),
                         [
                          TextNode('This is a ', TextType.TEXT, None),
                          TextNode('text', TextType.CODE, None),
                          TextNode(' node', TextType.TEXT, None)
                          ]
                         )


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with a [link](https://www.boot.dev/lessons)."
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is text with a [link](https://www.boot.dev/lessons)."
        )
        self.assertListEqual([("link", "https://www.boot.dev/lessons")], matches)