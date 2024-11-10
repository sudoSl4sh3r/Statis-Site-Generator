class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        if children is None:
            children = []
        if props is None:
            props = {}
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        x = ""
        for key, value in self.props.items():
            x += f" {key}='{value}'"
        return x

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=[], props=props)
        if self.value is None:
            raise ValueError("You passed an empty value.")

    def to_html(self):
        if self.tag is None:
            return self.value
        s = ''
        s += f"<{self.tag}"
        s += self.props_to_html()
        s += f">{self.value}</{self.tag}>"
        return s
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, children=children)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag has to be passed")
        if self.children is None or self.children == []:
            raise ValueError("There are no children associated")
        s = f'<{self.tag}>'
        
        for child in self.children:
            s += f"{child.to_html()}"
        s += f'</{self.tag}>'
        return s