import unittest

from extract import extract_markdown_images, extract_markdown_links


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
