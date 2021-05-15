import sys
from root.file_parser import *
 
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