import unittest
from textnode import TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

node1 = TextNode("This is a *bold* test.", "text")
nodes1 = [node1]
imagetext = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
imagenodes = [TextNode(imagetext, "text")]
linktext = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
linknodes = [TextNode(linktext, "text")]
fulltext = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
blocktext = "A\n\nB\nC"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_split(self):
        result = [TextNode("This is a ", "text"),
                  TextNode("bold", "bold"),
                  TextNode(" test.", "text")]
        self.assertEqual(split_nodes_delimiter(nodes1, "*", "bold"), result)

    def test_image(self):
        result = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(extract_markdown_images(imagetext), result)

    def test_image_split(self):
        result = [TextNode("This is text with an ", "text"),
                  TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                  TextNode(" and ", "text"),
                  TextNode("another", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
                  TextNode("", "text")]
        self.assertEqual(split_nodes_image(imagenodes), result)

    def test_link(self):
        result = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(linktext), result)

    def test_link_split(self):
        result = [TextNode("This is text with a ", "text"),
                  TextNode("link", "link", "https://www.example.com"),
                  TextNode(" and ", "text"),
                  TextNode("another", "link", "https://www.example.com/another"),
                  TextNode("", "text")]
        self.assertEqual(split_nodes_link(linknodes), result)
        
    def test_text_to_textnodes(self):
        result = [
    TextNode("This is ", "text"),
    TextNode("text", "bold"),
    TextNode(" with an ", "text"),
    TextNode("italic", "italic"),
    TextNode(" word and a ", "text"),
    TextNode("code block", "code"),
    TextNode(" and an ", "text"),
    TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and a ", "text"),
    TextNode("link", "link", "https://boot.dev"),
]
        self.assertEqual(text_to_textnodes(fulltext), result)

    def test_mmarkdown_to_blocks(self):
        result = ["A", "B\nC"]
        self.assertEqual(markdown_to_blocks(blocktext), result)

if __name__ == "__main__":
    unittest.main()
