# elnaz masoumi 96106106
# saeede vahedi 96102664


from parser_ import Parser_
from anytree import Node, RenderTree



parser = Parser_('./input.txt')

# for pre, fill, node in RenderTree(parser.root):
#     print("%s%s" % (pre, node.name))


with open("parse_tree.txt", 'w', encoding='utf-8') as file:    # parse_tree file
    for pre, _, node in RenderTree(parser.root):
        file.write("%s%s\n" % (pre, node.name))



with open("syntax_errors.txt", "w") as file:        # syntax errors file
    if len(parser.syn_err_l) == 0:
        file.write("There is no syntax error.\n")
    else:

        for l in parser.syn_err_l:
              file.write(l+"\n")