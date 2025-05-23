import unittest

from markdown_blocks import (
	BlockType,
	markdown_to_blocks,
	block_to_block_type,
	markdown_to_html_node
)


class TestMarkdownBlocks(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = '''
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
'''
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"# This is a heading",
				"This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
				"- This is the first list item in a list block\n- This is a list item\n- This is another list item",
			]
		)

	def test_markdown_to_blocks_newlines(self):
		md = '''
# This is a heading


This is a paragraph of text. It has some **bold** and _italic_ words inside of it.



- This is the first list item in a list block
- This is a list item
- This is another list item
'''
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"# This is a heading",
				"This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
				"- This is the first list item in a list block\n- This is a list item\n- This is another list item",
			]
		)

	def test_block_to_block_type_heading(self):
		block = "# This is a heading"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.HEADING)

	def test_block_to_block_type_paragraph(self):
		block = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.PARAGRAPH)

	def test_block_to_block_type_code(self):
		block = "```This is a code block\n with multiple lines```"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.CODE)

	def test_block_to_block_type_quote(self):
		block = "> this is a quote block\n> with multiple lines"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.QUOTE)

	def test_block_to_block_type_unordered_list(self):
		block = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.UNORDERED_LIST)

	def test_block_to_block_type_ordered_list(self):
		block = "1. this is an orderd list\n2. with multiple lines\n3. even a third list item"
		block_type = block_to_block_type(block)
		self.assertEqual(block_type, BlockType.ORDERED_LIST)

	def test_paragraph(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
		)

	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)

	def test_lists(self):
		md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
		)

	def test_headings(self):
		md = """
# this is an h1

this is paragraph text

## this is an h2
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
		)

	def test_blockquote(self):
		md = """
> This is a
> blockquote block

this is paragraph text

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
		)

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)

if __name__ == "__main__":
	unittest.main()
