from yacc import *

lexer = lex.lex()
parser = yacc.yacc()

def parser_file(file_name):

    file = open(file_name, "r")

    line = file.read()
    
    if line:
        parser.parse(line)


parser_file("tests/test_4.txt")
