from htmlnode import LeafNode, HTMLNode
from textnode import TextNode


test = TextNode('This is a text node', 'bold', 'https://www.boot.dev')
Leaf1 = LeafNode("Hello World")
Leaf2 = LeafNode("This is bold", "b")
Leaf3 = LeafNode("Link!", "a", {"href": "example.com"})
print(test)
print(Leaf1.to_html())
print(Leaf2.to_html())
print(Leaf3.to_html())