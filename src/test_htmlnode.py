import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("b", "This is a test!")
        node2 = HTMLNode("b", "This is a test!")
        self.assertEqual(node, node2)