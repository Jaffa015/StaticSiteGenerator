from textnode import TextNode, TextType

def main():
	node = TextNode("this is some anchor text", TextType.LINK, "https://boot.devjeff.nl")
	print(node)

main()
