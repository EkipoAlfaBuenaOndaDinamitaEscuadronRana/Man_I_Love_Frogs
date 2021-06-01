from router_solver import *
import sys
import compilador.helpers.file_parser
from compilador.helpers.file_parser import *
import glob, os
import re


# Este archivo funciona para tener los cuadruplos "correctos"
f = open("test_answers.txt", "w")
os.chdir("./compilador/tests/")
data = {}
for file in glob.glob("*.milf"):
    num = re.findall(r"\d+", str(file))
    data[num.pop()] = file

i = 1

while i <= 22:
    f.write(data[str(i)] + "\n")
    f.write(parser_file(data[str(i)], True))
    f.write("\n")
    i += 1


f.close()
