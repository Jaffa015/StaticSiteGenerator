import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This is a text node", TextType.TEXT)
		self.assertEqual(node, node2)

	def test_eq_false(self):
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_eq_false2(self):
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This is a text node2", TextType.TEXT)
		self.assertNotEqual(node, node2)

	def test_eq_url(self):
		node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
		node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
		self.assertEqual(node, node2)

	def test_repr(self):
		node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
		self.assertEqual(
			"TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
		)

	# tests textnode to HTML
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
		self.assertEqual(html_node.to_html(), "This is a text node")

	def test_text_bold(self):
		node = TextNode("This is bold", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is bold")
		self.assertEqual(html_node.to_html(), "<b>This is bold</b>")

	def test_text_italic(self):
		node = TextNode("This is italic", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is italic")
		self.assertEqual(html_node.to_html(), "<i>This is italic</i>")

	def test_text_code(self):
		node = TextNode("This is code", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is code")
		self.assertEqual(html_node.to_html(), "<code>This is code</code>")

	def test_text_link(self):
		node = TextNode("This is a link", TextType.LINK, "www.boot.devjeff.nl")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link")
		self.assertDictEqual(html_node.props, {"href": "www.boot.devjeff.nl"})
		self.assertEqual(html_node.to_html(), '<a href="www.boot.devjeff.nl">This is a link</a>')

	def test_text_image(self):
		node = TextNode("This is an image", TextType.IMAGE, "www.boot.devjeff.nl")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertDictEqual(html_node.props, {"src": "www.boot.devjeff.nl", "alt":"This is an image"})
		self.assertEqual(html_node.to_html(), '<img src="www.boot.devjeff.nl" alt="This is an image"></img>')


if __name__ == "__main__":
	unittest.main()
