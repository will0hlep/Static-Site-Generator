from enum import Enum

class TextType(Enum):
    HEADING = "heading"
    BOLD = "bold"
    ITALIC = "italic"
    BLOCKQUOTE = "blockquote"
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