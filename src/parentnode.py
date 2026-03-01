from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        else:
            childString = ""
            for child in self.children:
                childString += f"{child.to_html()}"

            return f"<{self.tag}>{childString}</{self.tag}>"

    def props_to_html(self):
        propsString = ""
        for prop in self.props:
            propsString += f' {prop}="{self.props[prop]}"'
        return propsString

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.children}, {self.props})"
