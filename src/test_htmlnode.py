import unittest

from htmlnode import HTMLNode

from htmlnode import LeafNode

from htmlnode import ParentNode 

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):

        node = HTMLNode("div", "Hello, world!", None, {"class": "greeting", "href": "https://www.youtube.com"},

        )

        self.assertEqual(node.props_to_html(),

            ' class="greeting" href="https://www.youtube.com"',)


    def test_props_to_html_empty_props(self):

        node = HTMLNode("p", "Some text", None, {})

        self.assertEqual(node.props_to_html(), "")


    def test_values(self):

        node = HTMLNode(

            "div",

            "Hey, I am Archana",

        )

        self.assertEqual(

            node.tag,

            "div",

        )

        self.assertEqual(

            node.value,

            "Hey, I am Archana",

        )

        self.assertEqual(

            node.children,

            None,

        )

        self.assertEqual(

            node.props,

            None,

        )


    def test_node_all_parameters(self):

        child = HTMLNode("b", "bold text")

        node = HTMLNode(

            "div",

            "Parent text",

            [child],

            {"id": "main", "class": "container"}

        )

        self.assertEqual(node.tag, "div")

        self.assertEqual(node.value, "Parent text")

        self.assertIsNotNone(node.children)

        self.assertEqual(node.children[0].tag, "b")

        self.assertEqual(node.props, {"id": "main", "class": "container"})

        self.assertEqual(node.__repr__(), "HTMLNode(div, Parent text, children: [HTMLNode(b, bold text, children: None, None)], {'id': 'main', 'class': 'container'})")


    def test_node_without_tag(self):

        node = HTMLNode(None, "Just some raw text.")

        self.assertEqual(node.tag, None)

        self.assertEqual(node.value, "Just some raw text.")

        self.assertEqual(node.children, None)

        self.assertEqual(node.props, None)

        self.assertEqual(node.__repr__(), "HTMLNode(None, Just some raw text., children: None, None)")


    def test_node_with_children_no_value(self):

        child_node = HTMLNode("span", "child text")

        node = HTMLNode("p", None, [child_node], None)

        self.assertEqual(node.tag, "p")

        self.assertEqual(node.value, None)

        self.assertIsNotNone(node.children) 

        self.assertEqual(len(node.children), 1) 

        self.assertEqual(node.children[0].tag, "span") 

        self.assertEqual(node.props, None)

        self.assertEqual(node.__repr__(), "HTMLNode(p, None, children: [HTMLNode(span, child text, children: None, None)], None)")


    def test_to_html_raises_error(self):

        node = HTMLNode("p", "Some text")

        with self.assertRaises(NotImplementedError):

            node.to_html()

    

    def test_repr(self):

        node = HTMLNode(

            "p",

            "What a beautiful city",

            None,

            {"class": "primary"},

        )

        self.assertEqual(

            node.__repr__(),

            "HTMLNode(p, What a beautiful city, children: None, {'class': 'primary'})",

        ) 



    def test_leaf_to_html_p(self):

        node = LeafNode("p", "Hello, world!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_no_tag_p(self):

        node = LeafNode(None, "Hello, world!")

        self.assertEqual(node.to_html(), "Hello, world!")


    def test_leaf_to_html_no_value_p(self):

        node = LeafNode("p", None)

        with self.assertRaises(ValueError):

            node.to_html()


    def test_leaf_repr_p(self):

        node = LeafNode("p", "Hello, world!")

        self.assertEqual(node.__repr__(), 'LeafNode(p, Hello, world!, None)')


    def test_leaf_to_html_a_with_props(self):

        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


    def test_leaf_to_html_a_with_props(self):

        node = LeafNode("a", "Click me!", {"class": "greeting", "href": "https://www.youtube.com"})

        self.assertEqual(node.to_html(), '<a class="greeting" href="https://www.youtube.com">Click me!</a>')


    def test_to_html_with_children(self):

        child_node = LeafNode("span", "child")

        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):

        grandchild_node = LeafNode("b", "grandchild")

        child_node = ParentNode("span", [grandchild_node])

        parent_node = ParentNode("div", [child_node])

        self.assertEqual(

            parent_node.to_html(),

            "<div><span><b>grandchild</b></span></div>",

        )


    def test_to_html_many_children(self):

        node = ParentNode(

            "p",

            [

                LeafNode("b", "Bold text"),

                LeafNode(None, "Normal text"),

                LeafNode("i", "italic text"),

                LeafNode(None, "Normal text"),

            ],

        )

        self.assertEqual(

            node.to_html(),

            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",

        )




    def test_to_html_no_tag(self):

        node = ParentNode(

            None,

            [

                LeafNode("b", "Bold text"),

                LeafNode(None, "Normal text"),

                LeafNode("i", "italic text"),

                LeafNode(None, "Normal text"),

            ],

        )

        with self.assertRaises(ValueError):

            node.to_html()



    def test_to_html_no_children(self):

        node = ParentNode(

            "p", None,

        )

        with self.assertRaises(ValueError):

            node.to_html()


    def test_to_html_with_empty_children_list(self):

        node = ParentNode(

            "p", [],

        )

        self.assertEqual(

            node.to_html(),

            "<p></p>",

        )


    def test_headings(self):

        node = ParentNode(

            "h2",

            [

                LeafNode("b", "Bold text"),

                LeafNode(None, "Normal text"),

                LeafNode("i", "italic text"),

                LeafNode(None, "Normal text"),

            ],

        )

        self.assertEqual(

            node.to_html(),

            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",

        )


if __name__ == "__main__":

    unittest.main() 