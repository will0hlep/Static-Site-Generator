import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            i = 0
            sections = node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            for part in sections:
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


def split_nodes_image(old_nodes):
    output_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            num_images = len(images)
            text_to_split = node.text
            for i in range(num_images):
                text_to_split = text_to_split.split(f"![{images[i][0]}]({images[i][1]})", 1)
                if text_to_split[0] != '':
                    new_node = TextNode(text_to_split[0], TextType.TEXT)
                    output_nodes.append(new_node)
                new_node = TextNode(images[i][0], TextType.IMAGE, images[i][1])
                output_nodes.append(new_node)
                text_to_split = text_to_split[1]
            if text_to_split != '':
                new_node = TextNode(text_to_split, TextType.TEXT)
                output_nodes.append(new_node)
        else:
            output_nodes.append(node)
    return output_nodes


def split_nodes_link(old_nodes):
    output_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_links(node.text)
            num_images = len(images)
            text_to_split = node.text
            for i in range(num_images):
                text_to_split = text_to_split.split(f"[{images[i][0]}]({images[i][1]})", 1)
                if text_to_split[0] != '':
                    new_node = TextNode(text_to_split[0], TextType.TEXT)
                    output_nodes.append(new_node)
                new_node = TextNode(images[i][0], TextType.LINK, images[i][1])
                output_nodes.append(new_node)
                text_to_split = text_to_split[1]
            if text_to_split != '':
                new_node = TextNode(text_to_split, TextType.TEXT)
                output_nodes.append(new_node)
        else:
            output_nodes.append(node)
    return output_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for type in [("**",TextType.BOLD),("_",TextType.ITALIC),("`",TextType.CODE)]:
        nodes = split_nodes_delimiter(nodes, type[0], type[1])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes