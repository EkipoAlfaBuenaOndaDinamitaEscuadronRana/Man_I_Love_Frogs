from router_solver import *
import ply.yacc as yacc
import ply.lex as lex
from compilador import parser, lexer
from compilador.parser import *
from compilador.lexer import *

import sys

lexer_loc = lex.lex()
parser_loc = yacc.yacc()


def parser_file(file_name, test=None):

    file = open(file_name, "r")

    line = file.read()
    file.close()

    if line:
        if test:

            line = ":" + line

        quads = parser_loc.parse(line)

    return quads
