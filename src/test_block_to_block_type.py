import unittest
from block_to_block_type import block_to_block_type
import re

class TestBlockToBlock(unittest.TestCase):
    def test_returns(self):
        markdown_text = """* This is the first list item in a list block
* This is a list item
* This is another list item"""

        markdown_text1 = """```The first code block.```"""

        markdown_text2 = """>Do or do not - there is no try.
>I am your father...
>You were supposed to destroy The Sith, not join them!"""

        markdown_text3 = """## Powerful header!"""

        markdown_text4 = """1. Ordered list
2. Second point
3. And third one"""

        markdown_text5 = """
That's a faulty text
that should become a paragraph"""

        markdown_text6 = """2. Wrongly enumerated list
3. Should become a paragraph"""

        markdown_text7 = """##Header with no space - a paragraph!"""
        markdown_text8 = """Text
>and a quote - should be a paragraph"""
        markdown_text9 = """A piece of code only with 3 backticks ``` should become a paragraph"""

        self.assertEqual(block_to_block_type(markdown_text), "unordered_list")
        self.assertEqual(block_to_block_type(markdown_text1), "code")
        self.assertEqual(block_to_block_type(markdown_text2), "quote")
        self.assertEqual(block_to_block_type(markdown_text3), "heading")
        self.assertEqual(block_to_block_type(markdown_text4), "ordered_list")
        self.assertEqual(block_to_block_type(markdown_text5), "paragraph")
        self.assertEqual(block_to_block_type(markdown_text6), "paragraph")
        self.assertEqual(block_to_block_type(markdown_text7), "paragraph")
        self.assertEqual(block_to_block_type(markdown_text8), "paragraph")
        self.assertEqual(block_to_block_type(markdown_text9), "paragraph")

if __name__ == "__main__":
    unittest.main()