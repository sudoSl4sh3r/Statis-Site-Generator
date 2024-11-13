from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_image_and_link import split_nodes_image, split_nodes_link

def text_to_textnodes(text):
    node = [TextNode(text, TextType.NORMAL)]
    type_delimit = split_nodes_delimiter(node, "`", TextType.CODE)
    type_delimit = split_nodes_delimiter(type_delimit, "**", TextType.BOLD)
    type_delimit = split_nodes_delimiter(type_delimit, "*", TextType.ITALIC)
    type_delimit = split_nodes_image(type_delimit)
    type_delimit = split_nodes_link(type_delimit)
    return type_delimit