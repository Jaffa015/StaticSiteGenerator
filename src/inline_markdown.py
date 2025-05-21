import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_images(nodes)
	nodes = split_nodes_links(nodes)
	return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		split_nodes = []
		sections = old_node.text.split(delimiter)
		if len(sections) % 2 == 0:
			raise ValueError("invalid markdown, formatted section not closed")
		for i in range(len(sections)):
			if sections[i] == "":
				continue
			if i % 2 == 0:
				split_nodes.append(TextNode(sections[i], TextType.TEXT))
			else:
				split_nodes.append(TextNode(sections[i], text_type))
		new_nodes.extend(split_nodes)
	return new_nodes


def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def build_new_nodes(text_sections:list, alt_sections:list, alt_textype:TextType):
	#build new nodes
		split_nodes = []
		for i in range(len(text_sections)):
			if text_sections[i] != "":
				split_nodes.append(TextNode(text_sections[i], TextType.TEXT))
			if i+1 <= len(alt_sections):
				(alt_text, alt_link) = alt_sections[i]
				split_nodes.append(TextNode(alt_text, alt_textype, alt_link))
		return split_nodes

def split_nodes_images(old_nodes:list):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue

		# split images
		image_sections = extract_markdown_images(old_node.text)
		# no image found
		if len(image_sections) == 0:
			new_nodes.append(old_node)
			continue
		
		# split text sections
		text_sections = []
		text_to_split = old_node.text
		for i in range(len(image_sections)):
			(image_alt, image_link) = image_sections[i]
			splits = text_to_split.split(f"![{image_alt}]({image_link})", 1)
			text_sections.append(splits[0])
			if i+1 == len(image_sections):
				text_sections.append(splits[1])
			else:
				text_to_split = splits[1]

		#build new nodes
		split_nodes = build_new_nodes(text_sections, image_sections, TextType.IMAGE)
		new_nodes.extend(split_nodes)
	return new_nodes

def split_nodes_links(old_nodes:list):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue

		# split images
		link_sections = extract_markdown_links(old_node.text)
		# no links found
		if len(link_sections) == 0:
			new_nodes.append(old_node)
			continue
		
		# split text sections
		text_sections = []
		text_to_split = old_node.text
		for i in range(len(link_sections)):
			(link_text, link_url) = link_sections[i]
			splits = text_to_split.split(f"[{link_text}]({link_url})", 1)
			text_sections.append(splits[0])
			if i+1 == len(link_sections):
				text_sections.append(splits[1])
			else:
				text_to_split = splits[1]

		#build new nodes
		split_nodes = build_new_nodes(text_sections, link_sections, TextType.LINK)
		new_nodes.extend(split_nodes)
	return new_nodes
