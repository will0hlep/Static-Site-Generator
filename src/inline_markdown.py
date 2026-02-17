import re
from textnode import TextType, TextNode

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