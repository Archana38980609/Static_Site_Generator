import unittest

from inline_markdown import (

    split_nodes_delimiter,

    extract_markdown_images,

    extract_markdown_links,

    

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


    def test_extract_markdown_images(self):

        matches = extract_markdown_images(

            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"

        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):

        matches = extract_markdown_links(

            "This is text with a [link](https://www.google.com) and [another link](https://www.youtube.com)"

        )

        self.assertListEqual(

            [

                ("link", "https://www.google.com"),

                ("another link", "https://www.youtube.com"),

            ],

            matches,

        )


    def test_extract_no_images_or_links(self):

        text_without_markdown = "This is a plain sentence with no images or links."

        

        images = extract_markdown_images(text_without_markdown)

        self.assertListEqual([], images) 


        links = extract_markdown_links(text_without_markdown)

        self.assertListEqual([], links) 


    def test_extract_empty_string_input(self):

        images = extract_markdown_images("")

        self.assertListEqual([], images) 


        links = extract_markdown_links("")

        self.assertListEqual([], links) 


    def test_extract_images_empty_alt_text(self):

        images = extract_markdown_images("Text with an ![alt](https://example.com/image.jpg) and ![ ](url.png)")

        self.assertListEqual(

            [

                ("alt", "https://example.com/image.jpg"),

                (" ", "url.png") 

            ], 

            images

        )

    

        images_truly_empty_alt = extract_markdown_images("Text with truly ![](image.gif)")

        self.assertListEqual([("", "image.gif")], images_truly_empty_alt)


    def test_extract_images_empty_url(self):

        images = extract_markdown_images("Text with an ![image title]() and another ![pic]( )")

        self.assertListEqual(

            [

                ("image title", ""),

                ("pic", " ") 

            ], 

            images

        )

        images_truly_empty_url = extract_markdown_images("Text with ![invalid]().")

        self.assertListEqual([("invalid", "")], images_truly_empty_url)


    def test_extract_links_empty_anchor_text(self):

        links = extract_markdown_links("Visit [link](http://example.com) and [ ](http://empty.com)")

        self.assertListEqual(

            [

                ("link", "http://example.com"),

                (" ", "http://empty.com") 

            ], 

            links

        )

        links_truly_empty_anchor = extract_markdown_links("Click here [](http://test.com)")

        self.assertListEqual([("", "http://test.com")], links_truly_empty_anchor)


    def test_extract_links_empty_url(self):

        links = extract_markdown_links("Go to [website]() or [here]( )")

        self.assertListEqual(

            [

                ("website", ""),

                ("here", " ") 

            ], 

            links

        )

        links_truly_empty_url = extract_markdown_links("Broken [link]().")

        self.assertListEqual([("link", "")], links_truly_empty_url)


    def test_extract_mixed_empty_cases(self):

        text = "![img]() [link]() ![](/path) [](/another)"

        images = extract_markdown_images(text)

        links = extract_markdown_links(text)


        self.assertListEqual([("img", ""), ("", "/path")], images)

        self.assertListEqual([("link", ""), ("", "/another")], links)


    def test_extract_markdown_images_malformed(self):

        text = "This is ![an image( with a malformed url"

        matches = extract_markdown_images(text)

        self.assertListEqual([], matches)


        text = "This is ![an image with a malformed alt text]"

        matches = extract_markdown_images(text)

        self.assertListEqual([], matches)


        text = "This is ![an image](url without closing parenthesis"

        matches = extract_markdown_images(text)

        self.assertListEqual([], matches)


    def test_extract_markdown_links_malformed(self):

        text = "This is [a link( with a malformed url"

        matches = extract_markdown_links(text)

        self.assertListEqual([], matches)


        text = "This is [a link with a malformed alt text]"

        matches = extract_markdown_links(text)

        self.assertListEqual([], matches)


        text = "This is [a link](url without closing parenthesis"

        matches = extract_markdown_links(text)

        self.assertListEqual([], matches)


    def test_extract_markdown_images_with_internal_brackets_parentheses_not_parsed(self):

        text_image_alt_brackets = "![image with [brackets]](https://example.com/image.jpg)"

        matches_image_alt_brackets = extract_markdown_images(text_image_alt_brackets)

        self.assertListEqual([], matches_image_alt_brackets) 


        text_image_url_parentheses = "![image](https://example.com/url(with).jpg)"

        matches_image_url_parentheses = extract_markdown_images(text_image_url_parentheses)

        self.assertListEqual([], matches_image_url_parentheses) 


    def test_extract_markdown_links_with_internal_brackets_parentheses_not_parsed(self):

        text_link_alt_brackets = "[link with [brackets]](https://example.com/link)"

        matches_link_alt_brackets = extract_markdown_links(text_link_alt_brackets)

        self.assertListEqual([], matches_link_alt_brackets) 


        text_link_url_parentheses = "[link](https://example.com/path(to)resource)"

        matches_link_url_parentheses = extract_markdown_links(text_link_url_parentheses)

        self.assertListEqual([], matches_link_url_parentheses) 


if __name__ == "__main__":

    unittest.main() 