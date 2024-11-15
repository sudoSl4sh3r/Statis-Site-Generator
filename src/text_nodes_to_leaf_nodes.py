from textnode import TextType
from htmlnode import LeafNode

def text_nodes_to_leaf_nodes(list_of_textnodes):
    list_of_leaf_nodes = []
    for item in list_of_textnodes:
        
        if item.text_type == TextType.NORMAL:
            list_of_leaf_nodes.append(LeafNode(None, item.text))
        
        elif item.text_type == TextType.BOLD:
            list_of_leaf_nodes.append(LeafNode("b", item.text))

        elif item.text_type == TextType.ITALIC:
            list_of_leaf_nodes.append(LeafNode("i", item.text))
        
        elif item.text_type == TextType.CODE:
            list_of_leaf_nodes.append(LeafNode("code", item.text))
        
        elif item.text_type == TextType.IMAGE:
            image_props = {"src": item.url, "alt": item.text} 
            list_of_leaf_nodes.append(LeafNode("img", " ", props=image_props))

        elif item.text_type == TextType.LINK:
            link_props = {"href": item.url}
            list_of_leaf_nodes.append(LeafNode("a", item.text, props=link_props))
    
    return list_of_leaf_nodes