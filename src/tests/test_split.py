import unittest

from nodes.textnode import TextNode, TextType
from split import split_nodes_delimeter, split_nodes_image, split_nodes_link


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


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [magical link](https://i.imgur.com/3elNhQu.png) with text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "magical link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" with text after", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_multi_node(self):
        nodes = [
            TextNode(
                "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [magical link](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            ),
            TextNode(
                "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [magical link](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "magical link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "magical link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_blanks(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[magical link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "magical link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" with text after", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_multi_node(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![magical image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            ),
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![magical image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "magical image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "magical image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )

    def test_split_images_with_blanks(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![magic image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "magic image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
