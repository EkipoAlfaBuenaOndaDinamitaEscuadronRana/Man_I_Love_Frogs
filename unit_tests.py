'''
Para correr el archivo, usar este comando
python -m unittest unit_tests.py
'''

from symbol_table import *
from lexer import *
from yacc import *
from semantic_table import *

import unittest

class TestSymbol(unittest.TestCase):
    def test_symbol(self):
        s = Symbol("variable", "int")

class TestVarTable(unittest.TestCase):
    def test_push_variable(self):
        vt = VarTable()

        s = Symbol("variable", "int")
        vt.push_variable(s, 12)
        self.assertEqual(vt.variables[s], 12)

        s = Symbol("variable", "int")
        vt.push_variable(s, 12)
        self.assertEqual(vt.variables[s], 12)

class TestFuncTable(unittest.TestCase):
    def test_push_function(self):
        ft = FuncTable()

        ft.push_function("print_something", "void")
        self.assertEqual(ft.functions["print_something"], "void")

        ft.push_function("calculate_something", "float")
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
            'PROGRAM', 'ID', 'COL', 'CCB', 'ID', 'EQ', 'CINT', 'SCOL', 'ID', 'EQ', 'TRUE', 'OCB'
        ]

        while True: 
            tok = lexer.token()

            if not tok:
                 break

            lexer_types.append(tok.type)
            lexer_values.append(tok.value)

        self.assertEqual(lexer_values, expected_values)
        self.assertEqual(lexer_types, expected_types)

class TestSemanticTable(unittest.TestCase):
    def test_considerate(self):
        self.assertEqual(SemanticTable.considerate('FLOAT', '+', 'INT'), 'FLOAT')
        self.assertEqual(SemanticTable.considerate('FLOAT', '-', 'NULL'), 'error')
        self.assertEqual(SemanticTable.considerate('CHAR', '>', 'STRING'), 'BOOL')
        self.assertEqual(SemanticTable.considerate('NULL', '==', 'BOOL'), 'BOOL')
        self.assertEqual(SemanticTable.considerate('DOUBLE', '+', 'CHAR'), 'error')
