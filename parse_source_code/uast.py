import bblfsh
import sys

client = bblfsh.BblfshClient("0.0.0.0:9432")
ast = client.parse("code_samples/%s" % sys.argv[1]).uast
print(ast)
