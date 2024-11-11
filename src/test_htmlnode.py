import unittest
from textnode import TextNode, NodeType, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from main import text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
###
# html node'y
###
        node = HTMLNode("a", "https://google.pl/", None, {"href": "https://google.pl/", "target": "_blank"})
        node2 = HTMLNode("p", "Typical paragraph of text", [node], {"color": "navy", "text-indent": "30px"})

        assert node.__repr__() == "HTMLNode(tag='a', value='https://google.pl/', children=[], props={'href': 'https://google.pl/', 'target': '_blank'})"
        assert node2.__repr__() == "HTMLNode(tag='p', value='Typical paragraph of text', children=[HTMLNode(tag='a', value='https://google.pl/', children=[], props={'href': 'https://google.pl/', 'target': '_blank'})], props={'color': 'navy', 'text-indent': '30px'})"
        self.assertNotEqual(node.__repr__(), node2.__repr__())

###
# leaf node'y
###
        leaf_node = LeafNode("a", "https://google.pl/", {"href": "https://google.pl/", "target": "_blank"})
        leaf_node2 = LeafNode("p", "Typical paragraph of text.", {"color": "white"})
        leaf_node3 = LeafNode("b", "", {})
        leaf_node4 = LeafNode("", " ", {})
        leaf_node5 = LeafNode(None, " ", {})

        ## sprawdzenie wartościdrukowaniem
        ## print(f"Expected leaf_node: ValueError('You passed an empty value.')")
        ## print(f"Actual leaf_node: {leaf_node5.to_html()}")
        ## print(f"")

        assert leaf_node.to_html() == "<a href='https://google.pl/' target='_blank'>https://google.pl/</a>"
        assert leaf_node2.to_html() == "<p color='white'>Typical paragraph of text.</p>"
        assert leaf_node3.to_html() == "<b></b>"
        assert leaf_node4.to_html() == "<> </>"
        assert leaf_node5.to_html() == " "
        try:
            leaf_node6 = LeafNode("p", None, {})
            assert False, "Value should have been passed"
        except ValueError:
            assert True

### 
# parent node'y
###
        parent_node = ParentNode("div", [LeafNode("b", "hello")])
        grandparent_node = ParentNode("div", [ParentNode("p", [LeafNode(None, "Text of a grandchildren")])])
        grandparent_node1 = ParentNode("div", [
            ParentNode("ul", [LeafNode("i", "Typical leaf value", {"color": "blue"})]), 
            ParentNode("ul", [LeafNode("b", "Second typical leaf value", {"color": "white"})])])

##        print(f"Actual: {grandparent_node1.to_html()}")
##        print(f"Expected: <div><ul><i color='blue'>Typical leaf value</i></ul><ul><b color='white'>Second typical leaf value</b></ul>")

        assert parent_node.to_html() == "<div><b>hello</b></div>"
        assert grandparent_node.to_html() == "<div><p>Text of a grandchildren</p></div>"
        assert grandparent_node1.to_html() == "<div><ul><i color='blue'>Typical leaf value</i></ul><ul><b color='white'>Second typical leaf value</b></ul></div>"
        try:
            parent_node_exception = ParentNode("div", [
                ParentNode("li", [LeafNode("b", None, {'color': 'black'})])
            ])
            assert False, "Value should have been passed"
        except ValueError:
            assert True

###
# text node'y do html node'a
###     
        try:
            text_node_to_html_node(TextNode("Typical text node", TextType.NORMAL))
            text_node_to_html_node(TextNode("Bolded one", TextType.BOLD))
            text_node_to_html_node(TextNode("Italic one", TextType.ITALIC))
            text_node_to_html_node(TextNode("\# Piece of code - print('hello world')", TextType.CODE))
            text_node_to_html_node(TextNode("", TextType.LINK, "https://google.pl/"))
            text_node_to_html_node(TextNode("Alt for image", TextType.IMAGE, "https://google.pl/"))
            assert True
        except Exception:
            assert False
        try:
            text_node_to_html_node(TextNode("Test of exception", "exception"))
            assert False, "Known text type"
        except Exception:
            assert True

###
# split_nodes_delimiter test
###
        
        to_split_node = TextNode("This is text with a `code block` word.", TextType.NORMAL)
        to_split_node1 = TextNode("This is text with a **bold** word.", TextType.NORMAL)
        to_split_node2 = TextNode("This is text with a *italic* word.", TextType.NORMAL)
        to_split_node3 = TextNode("This is text without a special markdowned word.", TextType.NORMAL)
        to_split_node4 = TextNode("This is text with **wrong** type.", TextType.BOLD)
        try:
            nodes_delimited = split_nodes_delimiter([to_split_node], "`", TextType.CODE)
            nodes_delimited1 = split_nodes_delimiter([to_split_node1, to_split_node2], "*", TextType.ITALIC)
            nodes_delimited2 = split_nodes_delimiter([to_split_node3], "**", TextType.BOLD)
            nodes_delimited3 = split_nodes_delimiter([to_split_node1], "*", TextType.ITALIC)
            nodes_delimited4 = split_nodes_delimiter([to_split_node4], "`", TextType.CODE)
            assert True
        except Exception:
            assert False


if __name__ == "__main__":
    unittest.main()