'''
Para correr el archivo, usar este comando
python -m unittest unit_tests.py
'''

from symbol_tables import *
from lexer import *
from yacc import *
from semantic_table import *

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
        vt = VariableTable()

        s = Symbol("variable", "int")
        vt.set_variable(s, 12)
        ft.set_function("print_something", "void", [s], vt)
        self.assertEqual(ft.functions["print_something"], {'t': "void", 'p' : [s], 'vt' : vt} )

        ft.set_function("calculate_something", "float", [], None)
        self.assertEqual(ft.functions["calculate_something"], {'t': "float", 'p' : [], 'vt' : None} )

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

class TestSemanticTable(unittest.TestCase):
    def test_considerate(self):
        # Existent types
        s_flt = Symbol("float", "FLT")
        s_int = Symbol("int", "INT")
        s_char = Symbol("char", "CHAR")
        s_str = Symbol("string", "STR")
        s_bool = Symbol("bool", "BOOL")
        s_null = Symbol("NULL", "NULL")
        
        # Operators
        s_add = Symbol("ADD", "operation")
        s_sub = Symbol("SUB", "operation")
        s_lt = Symbol("LT", "comparison")
        s_beq = Symbol("BEQ", "matching")
        
        # Non-existent type
        s_doub = Symbol("double", "DOUBLE")

        self.assertEqual(SemanticTable.considerate(s_flt, s_add, s_int), 'FLT')
        self.assertEqual(SemanticTable.considerate(s_flt, s_sub, s_null), 'error')
        self.assertEqual(SemanticTable.considerate(s_char, s_lt, s_str), 'BOOL')
        self.assertEqual(SemanticTable.considerate(s_null, s_beq, s_bool), 'BOOL')
        self.assertEqual(SemanticTable.considerate(s_doub, s_add, s_char), 'error')
