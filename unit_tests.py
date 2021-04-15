'''
Para correr el archivo, usar este comando
python -m unittest unit_tests.py
'''

from symbol_table import *

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
 