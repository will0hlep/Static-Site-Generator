import unittest

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """# this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('heading'))
        md = """##!# this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """#####this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """###### this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('heading'))
        md = """####### this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """```
this is a test```"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('code'))
        md = """``
this is a test```"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """```
this is a test``"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """> this is a test
> this is a test
> this is a test
> this is a test
> this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('quote'))
        md = """> this is a test
> this is a test
 this is a test
> this is a test
> this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """- this is a test
- this is a test
- this is a test
- this is a test
- this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('unordered_list'))
        md = """- this is a test
- this is a test
- this is a test
 this is a test
- this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """- this is a test
-this is a test
- this is a test
- this is a test
- this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """1. this is a test
2. this is a test
3. this is a test
4. this is a test
5. this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('ordered_list'))
        md = """1. this is a test
2.this is a test
3. this is a test
4. this is a test
5. this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """1. this is a test
2. this is a test
3. this is a test
4. this is a test
5 this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))
        md = """1. this is a test
2. this is a test
3. this is a test
3. this is a test
5. this is a test"""
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType('paragraph'))


if __name__ == "__main__":
    unittest.main()