class HTMLnode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        if children == None:
            children = []
        if props == None:
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

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"