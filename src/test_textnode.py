import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD)
        node5 = TextNode("This is a text node", TextType.BOLD, " ")
        node6 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node5, node6)

if __name__ == "__main__":
    unittest.main()