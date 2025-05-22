import re

from enum import Enum

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
