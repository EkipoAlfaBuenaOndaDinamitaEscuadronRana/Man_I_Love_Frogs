import sys
import compilador.helpers.file_parser
from compilador.helpers.file_parser import *

if len(sys.argv) > 1:
    i = 1
    while i < len(sys.argv):
        print(sys.argv[i])
        print(parser_file(sys.argv[i]))
        i += 1
else:
    print("DEFAULT: compilador/tests/test_11.txt")
    print(parser_file("compilador/tests/test_11.txt"))
