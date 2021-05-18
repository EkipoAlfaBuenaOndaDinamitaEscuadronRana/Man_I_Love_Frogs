import sys
from file_parser import *

if len(sys.argv) > 1:
    i = 1
    while i < len(sys.argv):
        print(sys.argv[i])
        print(parser_file(sys.argv[i]))
        i += 1
else:
    print("DEFAULT: tests/test_10.txt")
    print(parser_file("tests/test_10.txt"))
