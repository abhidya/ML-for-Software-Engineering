import bblfsh
import sys
from collections import defaultdict
import re


client = bblfsh.BblfshClient("0.0.0.0:9432")
ast = client.parse("code_samples/%s" % sys.argv[1]).uast

print(ast)


stack = []
for node in bblfsh.iterator(ast, bblfsh.TreeOrder.PRE_ORDER):
    stack.append(node)


result = defaultdict(int)
while stack:
    node = stack.pop()
    stack.extend(node.children)
    node = str(node)
    try:
        internal_type = re.search('internal_type: "(.*)"', node).group(1)
        token = re.search('token: "(.*)"', node).group(1)
    except:
        pass
    result[internal_type] += 1
    result[token] += 1

for k, v in result.items():
    print(k, v)
