from enum import Enum

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