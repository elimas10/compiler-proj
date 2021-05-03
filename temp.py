from anytree import Node, RenderTree


node=Node("a")
b=Node("b" , node)
c=Node("c", node)
d=Node("d", b)


for pre, fill, node in RenderTree(node):
    print("%s%s" % (pre, node.name))

# print(d.parent)
# print(d.name)
# print(d.root)
d=None

for pre, fill, node in RenderTree(node):
    print("%s%s" % (pre, node.name))

