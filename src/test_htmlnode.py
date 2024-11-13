import unittest
from textnode import TextNode, NodeType, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from main import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

###
# extract_markdown_images - list of tuples
###
        text = "Text with an image ![imaginery](https://i.imgur.com/aKa0qIh.gif) and ![one more](https://google.pl/)."
        text1 = "Text with a link [goto google](https://google.pl/) or [goto youtube](https://youtube.com/)."
        try:
            extract_markdown_images(text)
            extract_markdown_links(text1)
            assert True
        except Exception:
            assert False

###
# split_nodes_image test
###
        to_split_node_image = [TextNode("This is text with an ![alt text](https://google.pl/) image.", TextType.NORMAL),
                               TextNode("This is another text with an ![other alt](https://google.pl/) image.", TextType.NORMAL),
                               TextNode("This is a text without an image.", TextType.NORMAL)
        ]
        to_split_node_image1 = [TextNode("Different text with an ![alt text](https://google.pl/) image one, and ![alt text1](https://google.pl/) another image.", TextType.NORMAL)]
        to_split_node_image2 = [TextNode("![altt](https://google.pl/)", TextType.NORMAL)]
        to_split_node_image3 = [TextNode("![alt textt](https://google.pl/) Images ![alt texxt](https://google.pl/) mixed.", TextType.NORMAL)]

        #print(split_nodes_image(to_split_node_image))
        #print(split_nodes_image(to_split_node_image1))
        #print(split_nodes_image(to_split_node_image2))
        #print(split_nodes_image(to_split_node_image3))

        if (len(split_nodes_image(to_split_node_image)) == 7 and len(split_nodes_image(to_split_node_image1)) == 5 and len(split_nodes_image(to_split_node_image2)) == 1 and len(split_nodes_image(to_split_node_image3)) == 4):
            assert True
        else:
            assert False
    
###
# split_nodes_links test
###
        to_split_node_link = [
            TextNode("This is text with a [google](https://google.pl/) link.", TextType.NORMAL),
            TextNode("This is another text with a [googlelink!](https://google.pl/) link.", TextType.NORMAL),
            TextNode("This is a text without a link.", TextType.NORMAL)
        ]
        to_split_node_link1 = [TextNode("Different text with a [googlelink](https://google.pl/) link one, and [googlelink1](https://google.pl/) another link.", TextType.NORMAL)]
        to_split_node_link2 = [TextNode("[google](https://google.pl/)", TextType.NORMAL)]
        to_split_node_link3 = [TextNode("[googel](https://google.pl/) Links [googel1](https://google.pl/) mixed.", TextType.NORMAL)]

        if (len(split_nodes_link(to_split_node_link)) == 7 and len(split_nodes_link(to_split_node_link1)) == 5 and len(split_nodes_link(to_split_node_link2)) == 1 and len(split_nodes_link(to_split_node_link3)) == 4):
            assert True
        else:
            assert False

###
# test both splits
###
        to_split_node_img_link = [
            TextNode("This is text with both [google link](https://google.pl/) and an image ![alt](https://google.pl/).", TextType.NORMAL),
            TextNode("This is a text with neither of them.", TextType.NORMAL)
        ]
        if len(split_nodes_link(split_nodes_image(to_split_node_img_link))) == 6:
            assert True
        else:
            assert False

if __name__ == "__main__":
    unittest.main()