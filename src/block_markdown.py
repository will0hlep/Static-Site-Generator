from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    output = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        if block != '':
            output.append(block.strip('\n').strip())
    return output


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(markdown):
    if markdown[0] == "#":
        for i in range(1,7):
            if markdown[i] == " ":
                return BlockType("heading")
            if markdown[i] != "#" or i > 5:
                break
    elif markdown.startswith('```\n'):
        if markdown.endswith('```'):
            return BlockType("code")
    else:
        markdown_lines = markdown.split('\n')
        num_lines = len(markdown_lines)
        if markdown_lines[0].startswith(">"):
            for i in range(1,num_lines):
                if not markdown_lines[i].startswith(">"):
                    return BlockType("paragraph")
            return BlockType("quote")
        if markdown_lines[0].startswith("- "):
            for i in range(1,num_lines):
                if not markdown_lines[i].startswith("- "):
                    return BlockType("paragraph")
            return BlockType("unordered_list")
        if markdown_lines[0].startswith("1. "):
            for i in range(1,num_lines):
                if not markdown_lines[i].startswith(f"{i+1}. "):
                    return BlockType("paragraph")
            return BlockType("ordered_list")
    return BlockType("paragraph")


def block_stripper(blocktype, block):
    match blocktype:
        case blocktype.paragraph:
            return block, None
        case blocktype.heading:
            i = 0
            while block[i] == '#':
                i += 1
            return block[i + 1:] , i
        case blocktype.code:
            return block[4:-3], None
        case blocktype.quote:
            '''blocks = []
            lines = block.split('>')
            for line in lines:
                blocks.append(line.strip())'''
            return block.replace('> ','\n').replace('>','\n'), None
        case blocktype.unordered_list:
            return block.split('- ')[1:], None
        case blocktype.ordered_list:
            blocks = []
            i = 1
            lines = block.split('\n')
            for line in lines:
                blocks.append(line.strip(f'{i}. '))
                i += 1
            return blocks, None


def text_to_children(text):
    htmlnodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        htmlnodes.append(text_node_to_html_node(text_node))
    return htmlnodes


def blocktype_to_node(blocktype, text, depth):
    match blocktype:
        case blocktype.paragraph:
            return ParentNode('p', text_to_children(text.strip('\n')))
        case blocktype.heading:
            return ParentNode(f'h{depth}', text_to_children(text.strip('\n')))
        case blocktype.code:
            return ParentNode('pre', [LeafNode('code', text.strip('\n'))])
        case blocktype.quote:
            return LeafNode('blockquote', text.strip('\n'))
        case blocktype.unordered_list:
            return ParentNode('ul', [ParentNode('li', text_to_children(line.strip('\n'))) for line in text])
        case blocktype.ordered_list:
            return ParentNode('ol', [ParentNode('li', text_to_children(line.strip('\n'))) for line in text])


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        blocktype = block_to_block_type(block)
        text, depth = block_stripper(blocktype, block)
        htmlnode = blocktype_to_node(blocktype, text, depth)
        nodes.append(htmlnode)
    return ParentNode('div', nodes)