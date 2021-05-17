from yacc import *
import sys

lexer = lex.lex()
parser = yacc.yacc()


def parser_file(file_name, test=None):

    file = open(file_name, "r")

    line = file.read()
    file.close()

    if line:
        if test:
            line = ":" + line
        quads = parser.parse(line)
    return quads
