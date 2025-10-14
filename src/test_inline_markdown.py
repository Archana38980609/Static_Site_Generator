import unittest

from inline_markdown import (

    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
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







    def test_split_image(self):

        node = TextNode(

            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",

            TextType.TEXT,

        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("This is text with an ", TextType.TEXT),

                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),

            ],

            new_nodes,

        )


    def test_split_image_single(self):

        node = TextNode(

            "![image](https://www.example.COM/IMAGE.PNG)",

            TextType.TEXT,

        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),

            ],

            new_nodes,

        )


    def test_split_images(self):

        node = TextNode(

            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",

            TextType.TEXT,

        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("This is text with an ", TextType.TEXT),

                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),

                TextNode(" and another ", TextType.TEXT),

                TextNode(

                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"

                ),

            ],

            new_nodes,

        )


    def test_split_links(self):

        node = TextNode(

            "This is text with a [link](https://www.google.com) and [another link](https://www.youtube.com) with text that follows",

            TextType.TEXT,

        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("This is text with a ", TextType.TEXT),

                TextNode("link", TextType.LINK, "https://www.google.com"),

                TextNode(" and ", TextType.TEXT),

                TextNode("another link", TextType.LINK, "https://www.youtube.com"),

                TextNode(" with text that follows", TextType.TEXT),

            ],

            new_nodes,

        ) 


    def test_split_no_images(self):

        node = TextNode("This is plain text with no images.", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual([node], new_nodes)


    def test_split_no_links(self):

        node = TextNode("This is plain text with no links.", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)


    def test_split_plain_text_no_formatting(self):

        node = TextNode("Just a simple sentence.", TextType.TEXT)

        self.assertListEqual([node], split_nodes_image([node]))

        self.assertListEqual([node], split_nodes_link([node]))


    def test_split_image_at_start(self):

        node = TextNode("![start_img](http://start.com/img.png) text after image", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("start_img", TextType.IMAGE, "http://start.com/img.png"),

                TextNode(" text after image", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_split_image_at_end(self):

        node = TextNode("Text before image ![end_img](http://end.com/img.png)", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("Text before image ", TextType.TEXT),

                TextNode("end_img", TextType.IMAGE, "http://end.com/img.png"),

            ],

            new_nodes,

        )


    def test_split_link_at_start(self):

        node = TextNode("[start_link](http://start.com/link) text after link", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("start_link", TextType.LINK, "http://start.com/link"),

                TextNode(" text after link", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_split_link_at_end(self):

        node = TextNode("Text before link [end_link](http://end.com/link)", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("Text before link ", TextType.TEXT),

                TextNode("end_link", TextType.LINK, "http://end.com/link"),

            ],

            new_nodes,

        )


    def test_split_adjacent_images(self):

        node = TextNode("Hello ![a](img1.png)![b](img2.jpg) world", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("Hello ", TextType.TEXT),

                TextNode("a", TextType.IMAGE, "img1.png"),

                TextNode("b", TextType.IMAGE, "img2.jpg"),

                TextNode(" world", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_split_adjacent_links(self):

        node = TextNode("See [one](x.com)[two](y.org) for more.", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("See ", TextType.TEXT),

                TextNode("one", TextType.LINK, "x.com"),

                TextNode("two", TextType.LINK, "y.org"),

                TextNode(" for more.", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_split_malformed_image_missing_bracket(self):

        node = TextNode("Text with ![image(abc.com)", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, image section not closed or mismatched"):

            split_nodes_image([node])


    def test_split_malformed_image_no_closing_paren(self):

        node = TextNode("Text with ![image](abc.com", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, image section not closed"):

            split_nodes_image([node])


    def test_split_malformed_image_no_url(self):

        node = TextNode("Text with ![image] and more.", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, image section not closed"):

            split_nodes_image([node])


    def test_split_malformed_image_stray_exclamation(self):

        node = TextNode("Text with ! image](abc.com) and more.", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, stray '!' or malformed image syntax"):

            split_nodes_image([node])


    def test_split_malformed_link_missing_bracket(self):

        node = TextNode("Text with [link(abc.com)", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, link section not closed or mismatched"):

            split_nodes_link([node])


    def test_split_malformed_link_no_closing_paren(self):

        node = TextNode("Text with [link](abc.com", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, link section not closed"):

            split_nodes_link([node])


    def test_split_malformed_link_no_url(self):

        node = TextNode("Text with [link] and more.", TextType.TEXT)

        with self.assertRaisesRegex(ValueError, "invalid markdown, link section not closed"):

            split_nodes_link([node])


    def test_split_image_special_chars(self):

        node = TextNode("![im@ge-!_#](https://example.com/path/to/image with spaces.jpg?query=param&id=1)", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [TextNode("im@ge-!_#", TextType.IMAGE, "https://example.com/path/to/image with spaces.jpg?query=param&id=1")],

            new_nodes,

        )


    def test_split_link_special_chars(self):

        node = TextNode("Text with [LiNk_t3xt!@#](https://example.com/path/to/link_with_special_chars.html?q=test&a=b) end.", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("Text with ", TextType.TEXT),

                TextNode("LiNk_t3xt!@#", TextType.LINK, "https://example.com/path/to/link_with_special_chars.html?q=test&a=b"),

                TextNode(" end.", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_split_mixed_content_image_first(self):

        node = TextNode("![img1](url1) text [link1](urlA) more text ![img2](url2)", TextType.TEXT)

        nodes_after_image_split = split_nodes_image([node])

        final_nodes = split_nodes_link(nodes_after_image_split)


        self.assertListEqual(

            [

                TextNode("img1", TextType.IMAGE, "url1"),

                TextNode(" text ", TextType.TEXT),

                TextNode("link1", TextType.LINK, "urlA"),

                TextNode(" more text ", TextType.TEXT),

                TextNode("img2", TextType.IMAGE, "url2"),

            ],

            final_nodes,

        )


    def test_split_mixed_content_link_first(self):

        node = TextNode("[link1](urlA) text ![img1](url1) more text [link2](urlB)", TextType.TEXT)

        nodes_after_link_split = split_nodes_link([node])

        final_nodes = split_nodes_image(nodes_after_link_split)


        self.assertListEqual(

            [

                TextNode("link1", TextType.LINK, "urlA"),

                TextNode(" text ", TextType.TEXT),

                TextNode("img1", TextType.IMAGE, "url1"),

                TextNode(" more text ", TextType.TEXT),

                TextNode("link2", TextType.LINK, "urlB"),

            ],

            final_nodes,

        )


    def test_split_mixed_content_interspersed(self):

        node = TextNode("Start [link1](L1) middle ![img1](I1) end [link2](L2) final ![img2](I2)", TextType.TEXT)

        nodes_after_image_split = split_nodes_image([node])

        final_nodes = split_nodes_link(nodes_after_image_split)


        self.assertListEqual(

            [

                TextNode("Start ", TextType.TEXT),

                TextNode("link1", TextType.LINK, "L1"),

                TextNode(" middle ", TextType.TEXT),

                TextNode("img1", TextType.IMAGE, "I1"),

                TextNode(" end ", TextType.TEXT),

                TextNode("link2", TextType.LINK, "L2"),

                TextNode(" final ", TextType.TEXT),

                TextNode("img2", TextType.IMAGE, "I2"),

            ],

            final_nodes,

        ) 


    def test_split_empty_string(self):

        node = TextNode("", TextType.TEXT)

        self.assertListEqual([node], split_nodes_image([node]))

        self.assertListEqual([node], split_nodes_link([node]))


    def test_split_whitespace_only(self):

        node = TextNode("   \t\n  ", TextType.TEXT)

        self.assertListEqual([node], split_nodes_image([node]))

        self.assertListEqual([node], split_nodes_link([node]))


    def test_split_image_empty_alt(self):

        node = TextNode("Text with an empty alt ![ ](http://example.com/img.png)", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("Text with an empty alt ", TextType.TEXT),

                TextNode(" ", TextType.IMAGE, "http://example.com/img.png"),

            ],

            new_nodes,

        )


    def test_split_image_empty_url(self):

        node = TextNode("Text with an empty url ![alt text]()", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("Text with an empty url ", TextType.TEXT),

                TextNode("alt text", TextType.IMAGE, ""),

            ],

            new_nodes,

        )


    def test_split_link_empty_text(self):

        node = TextNode("Text with an empty text [ ](http://example.com/link)", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("Text with an empty text ", TextType.TEXT),

                TextNode(" ", TextType.LINK, "http://example.com/link"),  

            ],

            new_nodes,

        )


    def test_split_link_empty_url(self):

        node = TextNode("Text with an empty url [link text]()", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("Text with an empty url ", TextType.TEXT),

                TextNode("link text", TextType.LINK, ""),

            ],

            new_nodes,

        )


    def test_split_image_surrounded_by_punctuation(self):

        node = TextNode("See! ![shock](x.png). Is it shocking?", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("See! ", TextType.TEXT),

                TextNode("shock", TextType.IMAGE, "x.png"),

                TextNode(". Is it shocking?", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_split_link_surrounded_by_punctuation(self):

        node = TextNode("Wow--[check](y.com)--yes!", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("Wow--", TextType.TEXT),

                TextNode("check", TextType.LINK, "y.com"),

                TextNode("--yes!", TextType.TEXT),

            ],

            new_nodes,

        )


    def test_split_image_nested_invalid(self):

        node = TextNode("Text with ![im[alt]](url) inside.", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [TextNode("Text with ![im[alt]](url) inside.", TextType.TEXT)],

            new_nodes,

        )


    def test_split_link_nested_invalid(self):

        node = TextNode("Text with [li[nk]](url) inside.", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [TextNode("Text with [li[nk]](url) inside.", TextType.TEXT)],

            new_nodes,

        )


    def test_split_image_case_sensitive_url(self):

        node = TextNode("Image ![alt](HTTP://EXAMPLE.COM/IMG.PNG)", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("Image ", TextType.TEXT),

                TextNode("alt", TextType.IMAGE, "HTTP://EXAMPLE.COM/IMG.PNG"),

            ],

            new_nodes,

        )


    def test_split_link_case_sensitive_url(self):

        node = TextNode("Link [text](HTTPS://ANOTHER.ORG/PAGE.HTML)", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("Link ", TextType.TEXT),

                TextNode("text", TextType.LINK, "HTTPS://ANOTHER.ORG/PAGE.HTML"),

            ],

            new_nodes,

        )


    def test_split_image_case_sensitive_alt_text(self):

        node = TextNode("Image ![AlT TeXt](url.png)", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(

            [

                TextNode("Image ", TextType.TEXT),

                TextNode("AlT TeXt", TextType.IMAGE, "url.png"),

            ],

            new_nodes,

        )


    def test_split_link_case_sensitive_link_text(self):

        node = TextNode("Link [LiNk TeXt](url.html)", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(

            [

                TextNode("Link ", TextType.TEXT),

                TextNode("LiNk TeXt", TextType.LINK, "url.html"),

            ],

            new_nodes,

        )  




if __name__ == "__main__":

    unittest.main() 