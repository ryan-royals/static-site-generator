import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_basic_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD,
                        "http://ryanroyals.cloud")
        node2 = TextNode("This is a text node", TextType.BOLD,
                         "http://ryanroyals.cloud")
        self.assertEqual(node, node2)

    def test_basic_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node but different", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD,
                         "http://ryanroyals.cloud")
        self.assertNotEqual(node, node2)


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


if __name__ == "__main__":
    unittest.main()
