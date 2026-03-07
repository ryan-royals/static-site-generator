from leafnode import LeafNode
from textnode import TextType, TextNode
from split import split_nodes_delimeter, split_nodes_image, split_nodes_link


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text_node not valid TextType type")


def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimeter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimeter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimeter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes
