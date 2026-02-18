import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://www.boot.dev) and another [second link](https://www.bbc.co.uk/news) but not another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.bbc.co.uk/news"
                ),
                TextNode(" but not another", TextType.TEXT)
            ],
            new_nodes,
        )
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [],
            new_nodes,
        )