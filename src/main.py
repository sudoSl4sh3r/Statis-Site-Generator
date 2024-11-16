import re, os, shutil
from textnode import TextType
from htmlnode import LeafNode
from markdown_to_html_node import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from pathlib import Path

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

def extract_title(markdown):
    blocks = markdown.split("\n")
    title = ""
    for block in blocks:
        if re.match(r"# ", block):
            title = block
            title = re.sub("# ", "", title).strip()
            break
    if title == "":
        raise Exception("There is no h1 tag in your document.")
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}...")
    md_file = open(from_path, mode="r")
    templ_file = open(template_path, mode="r")

    markdown = md_file.read()
    template = templ_file.read()

    md_file.close()
    templ_file.close()

    html_nodes = markdown_to_html_node(markdown)
    article = ""
    article += html_nodes.to_html()

    template = template.replace("{{ Title }}", extract_title(markdown))
    template = template.replace("{{ Content }}", article)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(f"{dest_path}", "w") as file:
        file.write(template)
    
    return f"Generated page in {dest_path}!"

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path}, using {template_path}...")
    
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        dest_path = Path(dest_path)
        html_path = dest_path.with_suffix(".html") # changing the .md to .html
        if os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, dest_path)
        else:
            templ_file = open(template_path, mode="r")
            template = templ_file.read()
            templ_file.close()
            md_file = open(item_path, mode="r")
            markdown = md_file.read()
            md_file.close()
            html_nodes = markdown_to_html_node(markdown)
            article = ""
            article += html_nodes.to_html()
            template = template.replace("{{ Title }}", extract_title(markdown))
            template = template.replace("{{ Content }}", article)
            os.makedirs(html_path.parent, exist_ok=True)

            with open (f"{html_path}", "w") as file:
                file.write(template)

    return f"Generated page in {dest_dir_path}!"

def main():

    copying_static_to_public()
    generate_pages_recursive("./content", "template.html", "./public")

main()