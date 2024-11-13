from main import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
import re

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