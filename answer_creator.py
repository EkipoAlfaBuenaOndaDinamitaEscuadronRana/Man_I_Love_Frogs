import sys
from file_parser import *
# Este archivo funciona para tener los cuadruplos "correctos"
f = open("test_answers.txt", "w")

if len(sys.argv) > 1:
    i = 1
    while i < len(sys.argv):
        f.write(sys.argv[i] + "\n")
        f.write(parser_file(sys.argv[i], True))
        f.write("\n")
        i += 1  
else:
    print("DEFAULT: test_7.txt")
    print(parser_file("test_7.txt"))

f.close()