from markdown_to_html_node import markdown_to_html_node
import unittest

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_heading_conversion(self):
        markdown = "# Heading 1"
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><h1>Heading 1</h1></div>"

    def test_paragraph_conversion(self):
        markdown = "This is a paragraph."
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><p>This is a paragraph.</p></div>"

    def test_unordered_list_conversion(self):
        markdown = "- Item 1\n- Item 2"
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"

    def test_ordered_list_conversion(self):
        markdown = "1. First.\n2. Second."
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><ol><li>First.</li><li>Second.</li></ol></div>"

    def test_code_block_conversion(self):
        markdown = "```\ncode line 1\ncode line 2\n```"
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><pre><code>code line 1\ncode line 2</code></pre></div>"

    def test_quote_block_conversion(self):
        markdown = ">A simple quote.\n>Even simpler quote."
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><blockquote>A simple quote.\nEven simpler quote.</blockquote></div>"

    def test_mixed_block_conversion(self):
        markdown = "A normal block, that should be a paragraph, with a **bold** text and `code`."
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><p>A normal block, that should be a paragraph, with a <b>bold</b> text and <code>code</code>.</p></div>"

    def test_mixed1_block_conversion(self):
        markdown = ">This is a **bolded quote**.\n\n1. And this is \n2. an ordered list."
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><blockquote>This is a <b>bolded quote</b>.</blockquote><ol><li>And this is </li><li>an ordered list.</li></ol></div>"

    def test_mixed2_block_conversion(self):
        markdown = "1. An *ordered* list\n2. one more\n\n# h1 heading with [a link](https://google.pl/)."
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><ol><li>An <i>ordered</i> list</li><li>one more</li></ol><h1>h1 heading with <a href='https://google.pl/'>a link</a>.</h1></div>"

    def test_mixed3_block_conversion(self):
        markdown = "* An *ordered* list\n* one more\n\n# h1 heading with [a link](https://google.pl/)."
        node = markdown_to_html_node(markdown)
        assert node.to_html() == "<div><ul><li>An <i>ordered</i> list</li><li>one more</li></ul><h1>h1 heading with <a href='https://google.pl/'>a link</a>.</h1></div>"
