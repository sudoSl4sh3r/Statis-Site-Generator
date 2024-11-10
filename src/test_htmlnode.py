import unittest
from htmlnode import HTMLnode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLnode("a", "https://google.pl/", None, {"href": "https://google.pl/", "target": "_blank",})
        node2 = HTMLnode("p", "Typical paragraph of text", [node], {"color": "navy", "text-indent": "30px"})
        # node3 = HTMLnode()
        assert node.__repr__() == "HTMLNode(tag='a', value='https://google.pl/', children=[], props={'href': 'https://google.pl/', 'target': '_blank'})"
        assert node2.__repr__() == "HTMLNode(tag='p', value='Typical paragraph of text', children=[HTMLNode(tag='a', value='https://google.pl/', children=[], props={'href': 'https://google.pl/', 'target': '_blank'})], props={'color': 'navy', 'text-indent': '30px'})"
        self.assertNotEqual(node.__repr__(), node2.__repr__())

if __name__ == "__main__":
    unittest.main()