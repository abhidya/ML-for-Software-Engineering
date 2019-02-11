import plyj.parser as plyj
import sys

parser = plyj.Parser()
tree = parser.parse_file(sys.argv[1])
print(tree)

