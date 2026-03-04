import re

from leafnode import LeafNode
from textnode import TextType, TextNode


def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimeter)
            if len(parts) % 2 == 0:
                raise Exception(f"Invalid markdown: unmatched delimiter '{
                    delimeter}' in '{node.text}'")
            else:
                for i, part in enumerate(parts):
                    if part == "":
                        continue
                    node_type = TextType.TEXT if i % 2 == 0 else text_type
                    new_nodes.append(TextNode(part, node_type))
    return new_nodes


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        to_process = node.text
        links = extract_markdown_links(node.text)
        for link in links:
            sections = to_process.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            to_process = sections[1]
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        to_process = node.text
        images = extract_markdown_images(node.text)
        for image in images:
            sections = to_process.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            to_process = sections[1]
    return new_nodes


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


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
