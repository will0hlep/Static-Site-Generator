def markdown_to_blocks(markdown):
    output = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        if block != '':
            output.append(block.strip('\n').strip())
    return output