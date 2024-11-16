import re, os, shutil
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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def deleting_public_contents():
    if os.path.exists("./public"):
        contents = os.listdir(path="./public")
        for item in contents:
            item_path = os.path.join("./public", item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    return "Deleted /public contents."

def copy_directory(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest, mode=0o777)
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isdir(item_path):
            copy_directory(item_path, dest_path)
        else:
            shutil.copy(item_path, dest_path)

def copying_static_to_public():
    print(deleting_public_contents())
    print("Copying the /static contents to /public...")
    copy_directory("./static", "./public")
    print("Copying completed successfully.")

def main():
    copying_static_to_public()
    return

main()