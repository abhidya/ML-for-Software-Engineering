import bblfsh
import sys
from collections import defaultdict
import re

#connect to babelfish client
client = bblfsh.BblfshClient("0.0.0.0:9432")
ast = client.parse("code_samples/%s" % sys.argv[1]).uast

#uncomment this to look at the AST produced
print(ast)

#put nodes on stack
stack = []
for node in bblfsh.iterator(ast, bblfsh.TreeOrder.PRE_ORDER):
    stack.append(node)

#traverse stack, collect internal types of nodes
result = defaultdict(int)
while stack:
    node = stack.pop()
    stack.extend(node.children)
    node = str(node)
    #token we are looking for
    internal_type = re.search('internal_type: "(.*)"', node).group(1)

