from textnode import TextNode, TextType


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