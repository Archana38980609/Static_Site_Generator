import unittest


from textnode import TextNode, TextType, text_node_to_html_node 



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


        def test_text(self):

            node = TextNode("This is a text node", TextType.TEXT)

            html_node = text_node_to_html_node(node)

            self.assertEqual(html_node.tag, None)

            self.assertEqual(html_node.value, "This is a text node")


        def test_bold(self):

            node = TextNode("This is a bold text node", TextType.BOLD)

            html_node = text_node_to_html_node(node)

            self.assertEqual(html_node.tag, "b")

            self.assertEqual(html_node.value, "This is a bold text node")


        def test_italic(self):

            node = TextNode("This is an italic text node", TextType.ITALIC)

            html_node = text_node_to_html_node(node)

            self.assertEqual(html_node.tag, "i")

            self.assertEqual(html_node.value, "This is an italic text node")


        def test_code(self):

            node = TextNode("This is a code", TextType.CODE)

            html_node = text_node_to_html_node(node)

            self.assertEqual(html_node.tag, "code")

            self.assertEqual(html_node.value, "This is a code")


        def test_link(self):

            node = TextNode("This is a link", TextType.LINK, "https://www.google.com")

            html_node = text_node_to_html_node(node)

            self.assertEqual(html_node.tag, "a")

            self.assertEqual(html_node.value, "This is a link")

            self.assertEqual(

            html_node.props,

            {"href": "https://www.google.com"},)                                                                                                                                


        def test_image(self):

            node = TextNode("This is an image", TextType.IMAGE, "https://www.google.com")

            html_node = text_node_to_html_node(node)

            self.assertEqual(html_node.tag, "img")

            self.assertEqual(html_node.value, "")

            self.assertEqual(

            html_node.props,

            {"src": "https://www.google.com", "alt": "This is an image"},

            ) 


if __name__ == "__main__":

    unittest.main()
