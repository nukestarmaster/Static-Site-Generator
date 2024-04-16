import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

leaf1 = LeafNode("Hello World")
leaf2 = LeafNode("This is bold", "b")
leaf3 = LeafNode("Link!", "a", {"href": "example.com"})
parent1 = ParentNode("p", [leaf1, leaf2, leaf3])



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("b", "This is a test!")
        node2 = HTMLNode("b", "This is a test!")
        self.assertEqual(node1, node2)

    def test_leaf1(self):
        self.assertEqual(leaf1.to_html(), "Hello World")
    
    def test_leaf2(self):
        self.assertEqual(leaf2.to_html(), "<b>This is bold</b>")

    def test_leaf3(self):
        self.assertEqual(leaf3.to_html(), '<a href="example.com">Link!</a>')
    
    def test_parent1(self):
        self.assertEqual(parent1.to_html(), '<p>Hello World<b>This is bold</b><a href="example.com">Link!</a></p>')