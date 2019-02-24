import bblfsh #this library makes UASTs that can be converted into embedded vectors
import sys

client = bblfsh.BblfshClient("0.0.0.0:9432")
#code_samples path included temporarily
uast = client.parse("code_samples/%s" % sys.argv[1]).uast 
print(uast)
