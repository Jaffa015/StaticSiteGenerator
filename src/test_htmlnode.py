import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_to_hmtl_props(self):
		node = HTMLNode(
			"div",
			"This is a HTML node",
			None,
			{"href": "https://www.google.com", "target": "_blank"}
		)
		self.assertEqual(
			node.props_to_html(),
			' href="https://www.google.com" target="_blank"', 
		)

	def test_values(self):
		child = HTMLNode(
			"li",
			"I am the child"
		)
		node = HTMLNode(
			"ol",
			"This is a HTML node",
			[child],
			{"href": "https://www.google.com", "target": "_blank"}
		)
		self.assertEqual(
			node.tag,
			"ol"
		)
		self.assertEqual(
			node.value,
			"This is a HTML node"
		)
		self.assertListEqual(
			node.children,
			[child]
		)
		self.assertDictEqual(
			node.props,
			{"href": "https://www.google.com", "target": "_blank"}
		)

	def test_repr_without_child(self):
		node = HTMLNode(
			"H1",
			"This is a HTML node",
			None,
			{"href": "https://www.google.com"}
		)
		self.assertEqual(
			repr(node),
			"HTMLNode(H1, This is a HTML node, children: None, {'href': 'https://www.google.com'})"
		)

	def test_repr_with_child(self):
		child = HTMLNode(
			"l",
			"This is as HTML node"
		)
		node = HTMLNode(
			"H1",
			"This is a HTML node",
			[child],
			{"href": "https://www.google.com"}
		)
		self.assertEqual(
			repr(node),
			"HTMLNode(H1, This is a HTML node, children: [HTMLNode(l, This is as HTML node, children: None, None)], {'href': 'https://www.google.com'})"
		)


if __name__ == "__main__":
	unittest.main()
