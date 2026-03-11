from nodes.textnode import TextType, TextNode
from extract import extract_markdown_images, extract_markdown_links


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


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            to_process = node.text
            links = extract_markdown_links(node.text)
            for link in links:
                sections = to_process.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                to_process = sections[1]
            if len(to_process) != 0:
                new_nodes.append(TextNode(to_process, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            to_process = node.text
            images = extract_markdown_images(node.text)
            for image in images:
                sections = to_process.split(f"![{image[0]}]({image[1]})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                to_process = sections[1]
            if len(to_process) != 0:
                new_nodes.append(TextNode(to_process, TextType.TEXT))
    return new_nodes
