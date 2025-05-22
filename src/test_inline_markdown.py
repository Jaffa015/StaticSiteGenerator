import unittest
from inline_markdown import (
	split_nodes_delimiter,
	extract_markdown_images,
	extract_markdown_links,
	split_nodes_images,
	split_nodes_links,
	text_to_textnodes
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
		
	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_links(self):
		matches = extract_markdown_links(
			"This is text with an [link](https://www.youtube.com/@bootdotdev)"
		)
		self.assertListEqual([("link", "https://www.youtube.com/@bootdotdev")], matches)

	def test_extract_markdown_images_and_links(self):
		image_matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.youtube.com/@bootdotdev)"
		)
		link_matches = extract_markdown_links(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.youtube.com/@bootdotdev)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
		self.assertListEqual([("link", "https://www.youtube.com/@bootdotdev")], link_matches)

	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_images([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes
		)

	def test_split_images2(self):
		node = TextNode(
			"![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_images([node])
		self.assertListEqual(
			[
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes
		)

	def test_split_images_With_link(self):
		node = TextNode(
			"![image](https://i.imgur.com/zjjcJKZ.png) and a link [link](https://www.boot.dev)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_images([node])
		self.assertListEqual(
			[
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and a link [link](https://www.boot.dev)", TextType.TEXT),
			],
			new_nodes
		)

	def test_split_images_only_images(self):
		node = TextNode(
			"![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_images([node])
		self.assertListEqual(
			[
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes
		)

	def test_split_links(self):
		node = TextNode(
			"This is text with an [link](https://www.boot.dev) and another [second link](https://www.google.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_links([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://www.boot.dev"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second link", TextType.LINK, "https://www.google.com"),
			],
			new_nodes
		)

	def test_split_links2(self):
		node = TextNode(
			"[link](https://www.boot.dev) and another [second link](https://www.google.com) and a bit more text!",
			TextType.TEXT,
		)
		new_nodes = split_nodes_links([node])
		self.assertListEqual(
			[
				TextNode("link", TextType.LINK, "https://www.boot.dev"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second link", TextType.LINK, "https://www.google.com"),
				TextNode(" and a bit more text!", TextType.TEXT),
			],
			new_nodes
		)

	def test_split_link_with_image(self):
		node = TextNode(
			"[link](https://www.boot.dev) and a link ![image](https://i.imgur.com/zjjcJKZ.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_links([node])
		self.assertListEqual(
			[
				TextNode("link", TextType.LINK, "https://www.boot.dev"),
				TextNode(" and a link ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
			],
			new_nodes
		)

	def test_split_links_only_links(self):
		node = TextNode(
			"[link](https://www.boot.dev)[second link](https://www.google.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_links([node])
		self.assertListEqual(
			[
				TextNode("link", TextType.LINK, "https://www.boot.dev"),
				TextNode("second link", TextType.LINK, "https://www.google.com"),
			],
			new_nodes
		)

	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		nodes = text_to_textnodes(text)
		self.assertListEqual(
			[
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" and an ", TextType.TEXT),
				TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" and a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev")
			],
			nodes
		)

	def test_text_to_textnodes2(self):
		text = "this is an image ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) with some **bold text** and some [link](https://boot.dev)"
		nodes = text_to_textnodes(text)
		self.assertListEqual(
			[
				TextNode("this is an image ", TextType.TEXT),
				TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
				TextNode(" with some ", TextType.TEXT),
				TextNode("bold text", TextType.BOLD),
				TextNode(" and some ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev")
			],
			nodes
		)



if __name__ == "__main__":
	unittest.main()
