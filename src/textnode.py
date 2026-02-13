from enum import Enum

class inline_text_type(Enum):
    Heading = "heading"
    Bold = "bold"
    Italic = "italic"
    Blockquote = "blockquote"
    Code = "code"
    Link = "link"
    Image = "image"

class TextNode():
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = inline_text_type(TEXT_TYPE)
        self.url = URL

    def __eq__(self, other):
        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
        return False
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'