from yacc import *

lexer = lex.lex()
parser = yacc.yacc()

def parser_file(file_name):

    file = open(file_name)

    while True:
        line = file.readline()

        if line:
            parser.parse(line)

        else:
            break

parser_file("tests/works_1.txt")
