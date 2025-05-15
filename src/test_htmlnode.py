import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
	# HTMLNode tests
	def test_to_hmtl_props(self):
		node = HTMLNode(
			"div",
			"This is a HTML node",
			None,
			{"href": "https://www.google.com", "target": "_blank"}
		)
		self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

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
		self.assertEqual(node.tag, "ol")
		self.assertEqual(node.value, "This is a HTML node")
		self.assertListEqual(node.children, [child])
		self.assertDictEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})

	def test_repr_without_child(self):
		node = HTMLNode(
			"H1",
			"This is a HTML node",
			None,
			{"href": "https://www.google.com"}
		)
		self.assertEqual("HTMLNode(H1, This is a HTML node, children: None, {'href': 'https://www.google.com'})", repr(node))

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
	
	# LeafNode Tests
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_a(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		self.assertEqual(
			node.to_html(),
			'<a href="https://www.google.com">Click me!</a>',
		)

	def test_leaf_to_html_no_tag(self):
		node = LeafNode(None, "Hello, world!")
		self.assertEqual(node.to_html(), "Hello, world!")

	# ParentNode Tests
	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_2_children(self):
		child_node = LeafNode("span", "child")
		child_node2 = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node, child_node2])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span></div>")

	def test_to_html_with_children_no_tag(self):
		child_node = LeafNode(None, "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div>child</div>")

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
