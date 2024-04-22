import re
from .htmlnode import LeafNode, ParentNode

texttype_text = "text"
texttype_bold = "bold"
texttype_ital = "italic"
texttype_code = "code"
texttype_link = "link"
texttype_img = "image"

blocktype_par = "paragraph"
blocktype_head = "heading"
blocktype_code = "code"
blocktype_quote = "quote"
blocktype_ulist = "unordered_list"
blocktype_olist = "ordered_list"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"Textnode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html_node(self):
        switch = {"text": (self.text, None, None),
                  "bold": (self.text, "b", None),
                  "italic": (self.text, "i", None),
                  "code": (self.text, "code", None),
                  "link": (self.text, "a", {"href": self.url}),
                  "image": ("", "img", {"src": self.url,
                                       "alt": self.text})}
        if self.text_type not in switch:
            raise ValueError("Text type not recognized")
        return LeafNode(switch[self.text_type][0],
                        switch[self.text_type][1],
                        switch[self.text_type][2])
    
def split_nodes_delimiter(old_nodes: TextNode, delimiter: str, text_type: str):
    new_nodes = []
    for n in old_nodes:
        split_text = n.text.split(delimiter)
        new_list = []
        for i in range(len(split_text)):
            if i % 2 == 0:
                new_list.append(TextNode(split_text[i], n.text_type, n.url))
            else:
                new_list.append(TextNode(split_text[i], text_type))
        new_nodes.extend(new_list)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        split_text = re.split(r"!\[(.*?)\]\((.*?)\)", n.text)
        list_images = extract_markdown_images(n.text)
        new_list = []
        for i in range(len(split_text)):
            if i % 2 == 0:
                new_list.append(TextNode(split_text[i], n.text_type, n.url))
            else:
                new_list.append(TextNode(split_text[i], "image", list_images[i // 2][1]))
        new_nodes.extend(new_list)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        split_text = re.split(r"!\[.*?\]\(.*?\)", n.text)
        list_images = extract_markdown_images(n.text)
        new_list = []
        for i in range(len(split_text) - 1):
            new_nodes.append(TextNode(split_text[i], n.text_type, n.url))
            new_nodes.append(TextNode(list_images[i][0], "image", list_images[i][1]))
        new_nodes.append(TextNode(split_text[-1], n.text_type, n.url))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        split_text = re.split(r"\[.*?\]\(.*?\)", n.text)
        list_links = extract_markdown_links(n.text)
        new_list = []
        for i in range(len(split_text) - 1):
            new_nodes.append(TextNode(split_text[i], n.text_type, n.url))
            new_nodes.append(TextNode(list_links[i][0], "link", list_links[i][1]))
        new_nodes.append(TextNode(split_text[-1], n.text_type, n.url))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def text_to_textnodes(text):
    new_nodes = [TextNode(text, "text")]
    new_nodes = split_nodes_delimiter(new_nodes, "**", "bold")
    new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
    new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    for i in new_nodes:
        if i.text == "":
            new_nodes.remove(i)
    return new_nodes

def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    for b in blocks:
        b = b.strip()
        if b == "":
            blocks.remove("")
    return blocks
    

def block_to_blocktype(block):
    lines = block.split("\n")
    if (block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")):
        return blocktype_head
    if block[:3] == "```" and block[-3:] == "```" and len(lines) > 1:
        return blocktype_code
    if block[0] == ">":
        for l in lines:
            if l[0] != ">":
                return blocktype_par
        return blocktype_quote
    if block[:2] == "- ":
        for l in lines:
            if l[:2] != "- ":
                return blocktype_par
        return blocktype_ulist
    if block[:2] == "* ":
        for l in lines:
            if l[:2] != "* ":
                return blocktype_par
        return blocktype_ulist
        return blocktype_ulist
    if block[:3] == "1. ":
        i = 1
        for l in lines:
            if l[:3] != f"{i}. ":
                return blocktype_par
            i += 1
        return blocktype_olist
    return blocktype_par

def markdown_to_html_node(text):
    text_blocks = markdown_to_blocks(text)
    html_nodes = []
    for b in text_blocks:
        html_nodes.append(block_to_html_node(b, block_to_blocktype(b)))
    return ParentNode("div", html_nodes)
    
def block_to_html_node(text, type):
    if type == blocktype_par:
        return par_to_html_node(text)
    if type == blocktype_head:
        return head_to_html_node(text)
    if type == blocktype_code:
        return code_to_html(text)
    if type == blocktype_quote:
        return quote_to_html(text)
    if type == blocktype_ulist:
        return ulist_to_html(text)
    if type == blocktype_olist:
        return olist_to_html(text)
    raise ValueError("TextType not recognized")

def par_to_html_node(text):
    nodes = text_to_textnodes(text)
    htmlnodes = []
    for n in nodes:
        htmlnodes.append(n.text_node_to_html_node())
    return ParentNode("p", htmlnodes)

def head_to_html_node(text):
    i = 0
    while text[0] == "#":
        text = text[1:]
        i += 1
    text = text[1:]
    nodes = text_to_textnodes(text)
    htmlnodes = []
    for n in nodes:
        htmlnodes.append(n.text_node_to_html_node())
    return ParentNode(f"h{i}", htmlnodes)

def code_to_html(text):
    text = text[3:-3]
    nodes = text_to_textnodes(text)
    htmlnodes = []
    for n in nodes:
        htmlnodes.append(n.text_node_to_html_node())
    return ParentNode("pre", [ParentNode("code", htmlnodes)])

def quote_to_html(text):
    nodes = text_to_textnodes(text)
    htmlnodes = []
    for n in nodes:
        n.text = n.text[1:]
        htmlnodes.append(n.text_node_to_html_node())
    return ParentNode(f"blockquote", htmlnodes)

def ulist_to_html(text):
    lines = text.split("\n")
    html = []
    for l in lines:
        l = l[3:]
        nodes = text_to_textnodes(l)
        htmlnodes = []
        for n in nodes:
            htmlnodes.append(n.text_node_to_html_node())
        html.append(ParentNode("li", htmlnodes))
    return ParentNode("ul", html)

def olist_to_html(text):
    lines = text.split("\n")
    html = []
    for l in lines:
        l = l[3:]
        nodes = text_to_textnodes(l)
        htmlnodes = []
        for n in nodes:
            htmlnodes.append(n.text_node_to_html_node())
        html.append(ParentNode("li", htmlnodes))
    return ParentNode("ol", html)