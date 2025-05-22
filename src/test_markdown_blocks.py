import unittest

from markdown_blocks import (
	BlockType,
	markdown_to_blocks,
	block_to_block_type
)


class TestBlockMarkdown(unittest.TestCase):
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

if __name__ == "__main__":
	unittest.main()
