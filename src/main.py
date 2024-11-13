import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    type_list = []
    for type in TextType:
        type_list.append(type)
    if text_node.text_type not in type_list:
        raise Exception("Node is not an enum")
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {'href': f'{text_node.url}'})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {'src': f'{text_node.url}', 'alt': f'{text_node.text}'})
    elif text_node.text_type == TextType.NORMAL:
        return LeafNode("", text_node.text)
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []
    for node in old_nodes:
        first_pos = node.text.find(delimiter)
        if node.text_type == TextType.NORMAL and first_pos >= 0:
            second_pos = node.text.find(delimiter, first_pos + 1)
            if second_pos == -1:
                raise Exception(f"Incorrect markdown syntax. Check if '{delimiter}' occurs in pairs.")
            splitted_node = node.text.split(delimiter)
            list_of_nodes.append(TextNode(splitted_node[0], TextType.NORMAL))
            for i in range(1, len(splitted_node)):
                if i % 2 != 0:
                    list_of_nodes.append(TextNode(splitted_node[i], text_type))
                else:
                    list_of_nodes.append(TextNode(splitted_node[i], TextType.NORMAL))
        else:
            list_of_nodes.append(TextNode(node.text, node.text_type))
    return list_of_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    list_of_nodes = []
    for node in old_nodes:
        if not re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):
            list_of_nodes.append(node)
            continue
        images_tuple = extract_markdown_images(node.text)
        for tuple in images_tuple:
            image_alt = tuple[0]
            image_link = tuple[1]
            split_pattern = f"![{image_alt}]({image_link})"
            sections = node.text.split(split_pattern, 1)
            if sections[0]:
                list_of_nodes.append(TextNode(sections[0], TextType.NORMAL))
            list_of_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if sections[1]:
                node.text = sections[1]
        if node.text and not re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):
            list_of_nodes.append(TextNode(node.text, TextType.NORMAL))
    return list_of_nodes

def split_nodes_link(old_nodes):
    list_of_nodes = []
    for node in old_nodes:
        if not re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):
            list_of_nodes.append(node)
            continue
        images_tuple = extract_markdown_links(node.text)
        for tuple in images_tuple:
            link_text = tuple[0]
            link_url = tuple[1]
            split_pattern = f"[{link_text}]({link_url})"
            sections = node.text.split(split_pattern, 1)
            if sections[0]:
                list_of_nodes.append(TextNode(sections[0], TextType.NORMAL))
            list_of_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            if sections[1]:
                node.text = sections[1]
        if node.text and not re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):
            list_of_nodes.append(TextNode(node.text, TextType.NORMAL))
    return list_of_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.NORMAL)]
    type_delimit = split_nodes_delimiter(node, "`", TextType.CODE)
    type_delimit = split_nodes_delimiter(type_delimit, "**", TextType.BOLD)
    type_delimit = split_nodes_delimiter(type_delimit, "*", TextType.ITALIC)
    type_delimit = split_nodes_image(type_delimit)
    type_delimit = split_nodes_link(type_delimit)
    return type_delimit

def main():
    return

main()