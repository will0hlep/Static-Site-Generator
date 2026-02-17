from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = TextType(TEXT_TYPE)
        self.url = URL

    def __eq__(self, other):
        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
        return False
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode(
                            'a',
                            text_node.text,
                            {"href": text_node.url}
                            )
        case TextType.IMAGE:
            return LeafNode(
                            "img",
                            None,
                            {
                             "src": text_node.url,
                             "alt": text_node.text
                             }
                            )

       
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            i = 0
            for part in node.text.split(delimiter):
                if part != '':
                    new_node = TextNode(part, text_type if i == 1 else TextType.TEXT)
                    output_nodes.append(new_node)
                i += 1
                i %= 2
        else:
            output_nodes.append(node)
    return output_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

