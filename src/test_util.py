import unittest

from textnode import TextNode, TextType
from util import text_node_to_html_node, split_nodes_delimeter, extract_markdown_images, extract_markdown_links


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_not_valid_type(self):
        node = TextNode("Not a valid Node", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_text(self):
        text = TextNode("Text Node", TextType.TEXT)
        html = text_node_to_html_node(text)

        self.assertEqual(html.to_html(), "Text Node")
        self.assertEqual(html.props_to_html(), "")
        self.assertEqual(html.tag, None)
        self.assertEqual(html.value, "Text Node")

    def test_bold(self):
        text = TextNode("Bold Text Node", TextType.BOLD)
        html = text_node_to_html_node(text)

        self.assertEqual(html.to_html(), "<b>Bold Text Node</b>")
        self.assertEqual(html.props_to_html(), "")
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "Bold Text Node")

    def test_italic(self):
        text = TextNode("Italic Text Node", TextType.ITALIC)
        html = text_node_to_html_node(text)

        self.assertEqual(html.to_html(), "<i>Italic Text Node</i>")
        self.assertEqual(html.props_to_html(), "")
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "Italic Text Node")

    def test_code(self):
        text = TextNode("Code Text Node", TextType.CODE)
        html = text_node_to_html_node(text)

        self.assertEqual(html.to_html(), "<code>Code Text Node</code>")
        self.assertEqual(html.props_to_html(), "")
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "Code Text Node")

    def test_link(self):
        text = TextNode("Link Text Node", TextType.LINK,
                        "https://ryanroyals.cloud")
        html = text_node_to_html_node(text)

        self.assertEqual(html.to_html(), "<a>Link Text Node</a>")
        self.assertEqual(html.props_to_html(),
                         ' href="https://ryanroyals.cloud"')
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Link Text Node")

    def test_image(self):
        text = TextNode("Image Text Node", TextType.IMAGE,
                        "https://ryanroyals.cloud/cat.png")
        html = text_node_to_html_node(text)

        self.assertEqual(html.to_html(), "<img></img>")
        self.assertEqual(html.props_to_html(),
                         ' src="https://ryanroyals.cloud/cat.png" alt="Image Text Node"')
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")


class SplitNodesDelimeter(unittest.TestCase):
    def test_invalid_target(self):
        nodes = [
            TextNode("*test", TextType.TEXT)
        ]
        with self.assertRaises(Exception):
            split_nodes_delimeter(nodes, "*", TextType.ITALIC)

    def test_short_target(self):
        nodes = [
            TextNode("*test*", TextType.TEXT)
        ]
        expected = [
            TextNode("test", TextType.ITALIC)
        ]
        self.assertEqual(split_nodes_delimeter(
            nodes, "*", TextType.ITALIC), expected)

    def test_single_end_target(self):
        nodes = [
            TextNode("This is a *test*", TextType.TEXT)
        ]
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.ITALIC)
        ]
        self.assertEqual(split_nodes_delimeter(
            nodes, "*", TextType.ITALIC), expected)

    def test_single_start_target(self):
        nodes = [
            TextNode("*This* is a test", TextType.TEXT)
        ]
        expected = [
            TextNode("This", TextType.ITALIC),
            TextNode(" is a test", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimeter(
            nodes, "*", TextType.ITALIC), expected)

    def test_middle_target(self):
        nodes = [
            TextNode("This is a *test* that splits in the middle", TextType.TEXT)
        ]
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.ITALIC),
            TextNode(" that splits in the middle", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimeter(
            nodes, "*", TextType.ITALIC), expected)

    def test_multi_node(self):
        nodes = [
            TextNode("This is a *test*", TextType.TEXT),
            TextNode("This is another *test*", TextType.TEXT)
        ]
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.ITALIC),
            TextNode("This is another ", TextType.TEXT),
            TextNode("test", TextType.ITALIC)
        ]
        self.assertEqual(split_nodes_delimeter(
            nodes, "*", TextType.ITALIC), expected)

    def test_multi_target(self):
        nodes = [
            TextNode(
                "This is a *test* that splits *twice* in a tricky way", TextType.TEXT)
        ]
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.ITALIC),
            TextNode(" that splits ", TextType.TEXT),
            TextNode("twice", TextType.ITALIC),
            TextNode(" in a tricky way", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimeter(
            nodes, "*", TextType.ITALIC), expected)

    # def test_multi_transform(self):
    #     nodes = [
    #         TextNode("This is a *test* that has `two` transforms", TextType.TEXT),
    #     ]
    #     expected = [
    #         TextNode("This is a ", TextType.TEXT),
    #         TextNode("test", TextType.ITALIC),
    #         TextNode(" that has ", TextType.TEXT),
    #         TextNode("two", TextType.CODE),
    #         TextNode(" transforms", TextType.TEXT)
    #     ]
    #     pipelined = []
    #
    #     self.assertEqual(split_nodes_delimeter(
    #         nodes, "*", TextType.ITALIC), expected)


class TestRegex(unittest.TestCase):
    def test_extract_single_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and also This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_single_markdown_link(self):
        matches = extract_markdown_links(
            "This is link [to my blog](https://ryanroyals.cloud)"
        )
        self.assertListEqual(
            [("to my blog", "https://ryanroyals.cloud")], matches)

    def test_extract_multiple_markdown_link(self):
        matches = extract_markdown_links(
            "This is link [to my blog](https://ryanroyals.cloud) and [to claires portfolio](https://clairewebber.design)"
        )
        self.assertListEqual(
            [("to my blog", "https://ryanroyals.cloud"), ("to claires portfolio", "https://clairewebber.design")], matches)


if __name__ == "__main__":
    unittest.main()
