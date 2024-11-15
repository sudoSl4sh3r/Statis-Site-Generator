from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_image_and_link import split_nodes_image, split_nodes_link

def text_to_textnodes(text, block_type=None):
    nodes = []

    if block_type == "quote":
        nodes.append(TextNode(text, TextType.NORMAL))

    else:
        if "\n" in text: # if there are newlines in text, split them (for nested formatting)
            split_text = text.split("\n")
            for line in split_text:
                line = line.lstrip()
                nodes.append(TextNode(line, TextType.NORMAL))
        
        else:
            nodes = [TextNode(text, TextType.NORMAL)]
    
    type_delimit = split_nodes_delimiter(nodes, "`", TextType.CODE)
    type_delimit = split_nodes_delimiter(type_delimit, "**", TextType.BOLD)
    type_delimit = split_nodes_delimiter(type_delimit, "*", TextType.ITALIC)
    print(type_delimit)
    type_delimit = split_nodes_image(type_delimit)
    type_delimit = split_nodes_link(type_delimit)
    return type_delimit