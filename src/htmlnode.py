class HTMLNode():
	def __init__(self, tag=None, value=None, children:list=None, props:dict=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError()
	
	def props_to_html(self):
		if not self.props:
			return None
		return "".join(list(map(lambda item: f' {item[0]}="{item[1]}"', self.props.items())))
	
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

if __name__ == "__main__":
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

	print(node.props)