import code
import re
from enum import Enum
from shlex import quote

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown:str):
	blocks = markdown.split("\n\n")
	return [block.strip() for block in blocks if block]

def block_to_block_type(block:str):
	if re.search(r"^#{1,6}\s", block):
		return BlockType.HEADING
	
	if re.search(r"^```.*?```$", block, re.S):
		return BlockType.CODE
	
	if all(line.startswith(">") for line in block.split("\n")):
		return BlockType.QUOTE
	
	if all(line.startswith("-") for line in block.split("\n")):
		return BlockType.UNORDERED_LIST
	
	if all(line.startswith(f"{i + 1}.") for i, line in enumerate(block.split("\n"))):
		return BlockType.ORDERED_LIST
	
	return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children = []
	for block in blocks:
		html_node = block_to_html_node(block)
		children.append(html_node)
	return ParentNode('div', children, None)

def block_to_html_node(block):
	block_type = block_to_block_type(block)
	match block_type:
		case BlockType.PARAGRAPH:
			return paragraph_to_html_node(block)
		case BlockType.HEADING:
			return heading_to_html_node(block)
		case BlockType.CODE:
			return code_to_html_node(block)
		case BlockType.QUOTE:
			return quote_to_html_node(block)
		case BlockType.UNORDERED_LIST:
			return unordered_list_to_html_node(block)
		case BlockType.ORDERED_LIST:
			return ordered_list_to_html_node(block)
		case _:
			raise ValueError("invalid block type")

def text_to_children(text):
	text_nodes = text_to_textnodes(text)
	children = []
	for text_node in text_nodes:
		html_node = text_node_to_html_node(text_node)
		children.append(html_node)
	return children

def paragraph_to_html_node(block:str):
	lines = block.split("\n")
	paragraph = " ".join(lines)
	children = text_to_children(paragraph)
	return ParentNode("p", children)

def heading_to_html_node(block:str):
	level = 0
	for char in block:
		if char == "#":
			level += 1
		else:
			break
	if level + 1 >= len(block):
		raise ValueError(f"invalid heading level: {level}")
	text = block[level + 1:]
	children = text_to_children(text)
	return ParentNode(f"h{level}", children)

def code_to_html_node(block:str):
	if not block.startswith("```") or not block.endswith("```"):
		raise ValueError("Invalid code block")
	text = block[4:-3]
	raw_text_node = TextNode(text, TextType.CODE)
	child_node = text_node_to_html_node(raw_text_node)
	code_node = ParentNode("code", [child_node])
	return ParentNode("pre", [child_node])

def quote_to_html_node(block:str):
	lines = block.split("\n")
	new_lines = []
	for line in lines:
		if not line.startswith(">"):
			raise ValueError("Invalid quote block")
		new_lines.append(line.strip(">").strip())
	content = " ".join(new_lines)
	children = text_to_children(content)
	return ParentNode("blockquote", children)

def unordered_list_to_html_node(block:str):
	items = block.split("\n")
	html_items = []
	for item in items:
		text = item[2:]
		children = text_to_children(text)
		html_items.append(ParentNode("li", children))
	return ParentNode("ul", html_items)

def ordered_list_to_html_node(block:str):
	items = block.split("\n")
	html_items = []
	for item in items:
		text = item[3:]
		children = text_to_children(text)
		html_items.append(ParentNode("li", children))
	return ParentNode("ol", html_items)
