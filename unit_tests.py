'''
Para correr el archivo, usar este comando
python -m unittest unit_tests.py
'''

from symbol_tables import *
from lexer import *
from yacc import *

import unittest

class TestSymbol(unittest.TestCase):
    def test_symbol(self):
        s = Symbol("variable", "int")
        self.assertEqual(s.name, "variable")
        self.assertEqual(s.type, "int")

class TestVarTable(unittest.TestCase):
    def test_push_variable(self):
        vt = VariableTable()

        s = Symbol("variable", "int")
        vt.set_variable(s, 12)
        self.assertEqual(vt.variables[s.name], ["int", 12])

        s = Symbol("variable", "int")
        vt.set_variable(s, 23)
        self.assertEqual(vt.variables[s.name], ["int", 23])

class TestFuncTable(unittest.TestCase):
    def test_push_function(self):
        ft = FunctionTable()

        ft.set_function("print_something", "void")
        self.assertEqual(ft.functions["print_something"], "void")

        ft.set_function("calculate_something", "float")
        self.assertEqual(ft.functions["calculate_something"], "float")

class TestLexer(unittest.TestCase):
    def test_lexer(self):
        lexer = lex.lex()
        lexer.input("program test : { a = 1; b = true }") 

        lexer_values = []
        lexer_types = []

        expected_values = [
            'program', 'test', ':', '{', 'a', '=', 1, ';', 'b', '=', 'true', '}'
        ]

        expected_types = [
            'PROGRAM', 'ID', 'COL', 'OCB', 'ID', 'EQ', 'CINT', 'SCOL', 'ID', 'EQ', 'TRUE', 'CCB'
        ]

        while True: 
            tok = lexer.token()

            if not tok:
                 break

            lexer_types.append(tok.type)
            lexer_values.append(tok.value)

        self.assertEqual(lexer_values, expected_values)
        self.assertEqual(lexer_types, expected_types)
