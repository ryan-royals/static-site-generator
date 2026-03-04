from src.textnode import TextNode
from src.util import extract_markdown_links
node = TextNode(
)


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        for link in links:
            sections = node.text.split(f"[{link[0]}]({link[1]})", 1)
            print(sections)
