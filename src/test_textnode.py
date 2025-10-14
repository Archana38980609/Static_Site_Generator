import unittest


from textnode import TextNode, TextType



class TestTextNode(unittest.TestCase):

    def test_eq_basic(self):

        node = TextNode("This is a text node", TextType.BOLD)

        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)


    def test_eq_different_text_type(self):

        node = TextNode("This is a text node", TextType.BOLD)

        node2 = TextNode("This is a text node", TextType.ITALIC)

        self.assertNotEqual(node, node2)


    def test_eq_different_url(self):

        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")

        node2 = TextNode("This is a text node", TextType.BOLD, None)

        self.assertNotEqual(node, node2)


    def test_eq_different_text(self):

        node = TextNode("This is a text node", TextType.BOLD)

        node2 = TextNode("This is a text node2", TextType.BOLD)

        self.assertNotEqual(node, node2)


    def test_eq_two_different_urls(self):

        node = TextNode("Link text", TextType.LINK, "www.example.com")

        node2 = TextNode("Link text", TextType.LINK, "www.google.com")

        self.assertNotEqual(node, node2) 


    def test_eq_same_full_node(self):

        node = TextNode("Another link", TextType.LINK, "www.sameurl.com")

        node2 = TextNode("Another link", TextType.LINK, "www.sameurl.com")

        self.assertEqual(node, node2)


    def test_ne_slightly_different_text(self):

        node = TextNode("Hello World", TextType.TEXT, "http://example.com")

        node2 = TextNode("Hello world", TextType.TEXT, "http://example.com") 

        self.assertNotEqual(node, node2)


        def test_ne_other_object_type(self):

            node = TextNode("A text node", TextType.TEXT)


            # Comparing to a string

            self.assertNotEqual(node, "just a string")


            # Comparing to an integer

            self.assertNotEqual(node, 123)


            # Comparing to None

            self.assertNotEqual(node, None)


        def test_repr(self):

            node = TextNode("This is a text node", TextType.TEXT, "https://www.google.com")

            self.assertEqual(

            "TextNode(This is a text node, text, https://www.google.com)", repr(node)

            )

if __name__ == "__main__":

    unittest.main()
