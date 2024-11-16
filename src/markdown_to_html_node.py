from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type
from text_to_textnodes import text_to_textnodes
from text_nodes_to_leaf_nodes import text_nodes_to_leaf_nodes
from htmlnode import HTMLNode, ParentNode, LeafNode
import re

def markdown_to_html_node(markdown): #input: full markdown document - output: html nodes
    div_node = ParentNode("div", children=[])
    clean_blocks = markdown_to_blocks(markdown) # list of trimmed, split blocks
    for block in clean_blocks: # iterate through blocks
        block_type = block_to_block_type(block) # determine type
        
        if block_type == "code":
            no_gravis_block = re.sub("(```)", "", block).strip()
            code_node = LeafNode("code", no_gravis_block) # create LeafNode (last node)
            parent_pre_node = ParentNode("pre", [code_node]) # create its parent
            div_node.children.append(parent_pre_node) # add parent to general node

        elif block_type == "heading":
            hash_count = block.count("#") # count ammount of hashes
            header_content = block.lstrip("#").strip() # strip the hashes and whitespace - html does not need them
            header_node = ParentNode(f"h{hash_count}", children=[]) # create appropiate h tag (1-6)
            list_of_text_nodes = text_to_textnodes(header_content) # transform all nested formatting to a list of textnodes
            list_of_leaf_nodes = text_nodes_to_leaf_nodes(list_of_text_nodes) # transform textnodes to leafnodes
            for item in list_of_leaf_nodes:
                header_node.children.append(item) # append the nodes to its parent, h{x}
            div_node.children.append(header_node) # add parent h{x} to the general node
        
        elif block_type == "paragraph":
            p_node = ParentNode("p", children=[]) # create parent p tag
            list_of_text_nodes = text_to_textnodes(block) # return a list o nodes
            list_of_leaf_nodes = text_nodes_to_leaf_nodes(list_of_text_nodes) # transform textnodes to leafnodes
            for item in list_of_leaf_nodes:
                p_node.children.append(item) # append the found items to the parent, p
            div_node.children.append(p_node) # append parent to the general node

        elif block_type == "quote":
            quote_node = ParentNode("blockquote", children=[]) # create parent quote tag
            cleaned_block = re.sub("(>)", "", block).strip()
            list_of_text_nodes = text_to_textnodes(cleaned_block, block_type) # transform to list of textnodes
            list_of_leaf_nodes = text_nodes_to_leaf_nodes(list_of_text_nodes) # transform textnodes to leafnodes
            for item in list_of_leaf_nodes:
                quote_node.children.append(item) # append the found items to the parent, blockquote
            div_node.children.append(quote_node) # append parent to the general node

        elif block_type == "unordered_list":
            ul_node = ParentNode("ul", children=[]) # create parent ul tag
            list_item_content = []
            list_list_item_content = []
            block_list = block.splitlines(True) # preserves \n
            
            for line in block_list:
                if line.startswith("* "):
                    content = line.split("* ", 1)
                    content.remove("")
                    list_list_item_content.append(content) # making a list inside a list
                elif line.startswith("- "):
                    content = line.split("- ", 1)
                    content.remove("")
                    list_list_item_content.append(content) # making a list inside a list
            
            for item in list_list_item_content: 
                list_item_content.extend(item) # getting rid of unnesessary list

            for item in list_item_content:
                node_item = text_to_textnodes(item)
                leaf_node = text_nodes_to_leaf_nodes(node_item)
                li_node = ParentNode("li", leaf_node)
                ul_node.children.append(li_node)
            
            div_node.children.append(ul_node) # append parent to the general node

        elif block_type == "ordered_list": 
            ol_node = ParentNode("ol", children=[]) # create parent ol tag
            list_list_item_content = []
            list_item_content = []
            block_list = block.splitlines(True) # preserves \n

            for line in block_list:
                content = re.sub(r"(\d+\. )", "", line)
                list_list_item_content.append(content)

            for item in list_list_item_content:
                list_item_content.append(item)
            
            for item in list_list_item_content:
                node_item = text_to_textnodes(item)
                leaf_node = text_nodes_to_leaf_nodes(node_item)
                li_node = ParentNode("li", leaf_node)
                ol_node.children.append(li_node)
            div_node.children.append(ol_node) # append parent to the general node

    return div_node