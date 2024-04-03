class HTMLNode:
    def __init__(self, tag = None, value =None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        tags = []
        for k in self.props:
            tags.append(f'{k}="{self.props[k]}"')
        print(' '.join(tags))
        return " " + ' '.join(tags)
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
        super().__init__(tag, value, props = props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f'<{self.tag}={self.props_to_html()}>{self.value}</{self.tag}>'