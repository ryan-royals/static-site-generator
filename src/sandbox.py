from textnode import TextNode, TextType
from util import extract_markdown_links

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)


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


new_nodes = split_nodes_link([node])
print(new_nodes)
