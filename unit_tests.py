'''
Para correr el archivo, usar este comando
python -m unittest unit_tests.py
'''

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

class TestCuadruple(unittest.TestCase):
    def test_cuadruple(self):
        c = Cuadruple("MUL", "B", "C", "T1")
        self.assertEqual(c.format_cuadruple(), "MUL B C T1")

class TestSemanticTable(unittest.TestCase):
    def test_arithmetic_expression(self):
        expression = [ # A + B * C / D - E * F
            Symbol("A", "INT"),
            Symbol("ADD", "operation"),
            Symbol("B", "FLT"),
            Symbol("MUL", "operation"),
            Symbol("C", "FLT"),
            Symbol("DIV", "operation"),
            Symbol("D", "FLT"),
            Symbol("SUB", "operation"),
            Symbol("E", "FLT"),
            Symbol("MUL", "operation"),
            Symbol("F", "FLT")
        ]

        expected_response = [
            Cuadruple("MUL", "B", "C", "T1"),
            Cuadruple("DIV", "T1", "D", "T2"),
            Cuadruple("SUM", "A", "T2", "T3"),
            Cuadruple("MUL", "E", "F", "T4"),
            Cuadruple("SUB", "T3", "T4", "T5")
        ]

        response = SemanticTable.arithmetic_expression(expression)

        self.assertEqual(response, expected_response)
