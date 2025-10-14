import unittest

from inline_markdown import (

    split_nodes_delimiter,

)


from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):

    def test_delim_bold(self):

        node = TextNode("This is text with a **bolded** word", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(

            [

                TextNode("This is text with a ", TextType.TEXT),

                TextNode("bolded", TextType.BOLD),

                TextNode(" word", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_delim_bold_double(self):

        node = TextNode(

            "This is text with a **bolded** word and **another**", TextType.TEXT

        )

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(

            [

                TextNode("This is text with a ", TextType.TEXT),

                TextNode("bolded", TextType.BOLD),

                TextNode(" word and ", TextType.TEXT),

                TextNode("another", TextType.BOLD),

            ],

            new_nodes,

        )


    def test_delim_bold_multiword(self):

        node = TextNode(

            "This is text with a **bolded word** and **another**", TextType.TEXT

        )

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(

            [

                TextNode("This is text with a ", TextType.TEXT),

                TextNode("bolded word", TextType.BOLD),

                TextNode(" and ", TextType.TEXT),

                TextNode("another", TextType.BOLD),

            ],

            new_nodes,

        )


    def test_delim_italic(self):

        node = TextNode("This is text with an _italic_ word", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertListEqual(

            [

                TextNode("This is text with an ", TextType.TEXT),

                TextNode("italic", TextType.ITALIC),

                TextNode(" word", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_delim_bold_and_italic(self):

        node = TextNode("**bold** and _italic_", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        self.assertListEqual(

            [

                TextNode("bold", TextType.BOLD),

                TextNode(" and ", TextType.TEXT),

                TextNode("italic", TextType.ITALIC),

            ],

            new_nodes,

        )


    def test_delim_code(self):

        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(

            [

                TextNode("This is text with a ", TextType.TEXT),

                TextNode("code block", TextType.CODE),

                TextNode(" word", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_delim_no_delimiter_present(self):

        node = TextNode("This is plain text with no bolding.", TextType.TEXT)

        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(

            [TextNode("This is plain text with no bolding.", TextType.TEXT)],

            new_nodes,

        )


    def test_delim_unmatched_delimiters(self):

        node = TextNode("This text has an **unclosed bold section", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, formatted section not closed"):

            split_nodes_delimiter([node], "**", TextType.BOLD)


        node2 = TextNode("Another example with _unclosed italic", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, formatted section not closed"):

            split_nodes_delimiter([node2], "_", TextType.ITALIC)


        node3 = TextNode("One more `unclosed code block", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, formatted section not closed"):

            split_nodes_delimiter([node3], "`", TextType.CODE)


    def test_delim_delimiter_at_beginning_or_end(self):

        node_start = TextNode("**Bold at start** and some text.", TextType.TEXT)

        new_nodes_start = split_nodes_delimiter([node_start], "**", TextType.BOLD)

        self.assertListEqual(

            [

                TextNode("Bold at start", TextType.BOLD),

                TextNode(" and some text.", TextType.TEXT),

            ],

            new_nodes_start,

        )


        node_end = TextNode("Some text and **bold at end**", TextType.TEXT)

        new_nodes_end = split_nodes_delimiter([node_end], "**", TextType.BOLD)

        self.assertListEqual(

            [

                TextNode("Some text and ", TextType.TEXT),

                TextNode("bold at end", TextType.BOLD),

            ],

            new_nodes_end,

        )


        node_full = TextNode("**Just bold**", TextType.TEXT)

        new_nodes_full = split_nodes_delimiter([node_full], "**", TextType.BOLD)

        self.assertListEqual(

            [TextNode("Just bold", TextType.BOLD)],

            new_nodes_full,

        )


    def test_delim_multiple_nodes_in_input_list(self):

        nodes = [

            TextNode("This is **part one**.", TextType.TEXT),

            TextNode("This node is _already italic_.", TextType.ITALIC), 

            TextNode("And **part two** here.", TextType.TEXT),

            TextNode("`Already code` here.", TextType.CODE), 

        ]


        processed_nodes_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertListEqual(

            [

                TextNode("This is ", TextType.TEXT),

                TextNode("part one", TextType.BOLD),

                TextNode(".", TextType.TEXT),

                TextNode("This node is _already italic_.", TextType.ITALIC),

                TextNode("And ", TextType.TEXT),

                TextNode("part two", TextType.BOLD),

                TextNode(" here.", TextType.TEXT),

                TextNode("`Already code` here.", TextType.CODE),

            ],

            processed_nodes_bold,

        )


        nodes_for_italic_test = [

            TextNode("Text with _italic_ word.", TextType.TEXT),

            TextNode("Non-text node", TextType.BOLD), 

            TextNode("Another _italic_ here.", TextType.TEXT),

        ]

        result_italic = split_nodes_delimiter(nodes_for_italic_test, "_", TextType.ITALIC)

        self.assertListEqual(

            [

                TextNode("Text with ", TextType.TEXT),

                TextNode("italic", TextType.ITALIC),

                TextNode(" word.", TextType.TEXT),

                TextNode("Non-text node", TextType.BOLD), 

                TextNode("Another ", TextType.TEXT),

                TextNode("italic", TextType.ITALIC),

                TextNode(" here.", TextType.TEXT),

            ],

            result_italic,

        ) 

if __name__ == "__main__":

    unittest.main() 