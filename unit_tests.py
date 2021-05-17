from symbol_tables import *
from lexer import *
from yacc import *
from quadruple import *
from file_parser import *

import unittest


class TestYacc(unittest.TestCase):
    def test_yacc(self):
        def test_file(file_name, answer):
            result = parser_file(file_name)
            if result == answer:
                return "."
            else:
                return "F"

        test_answers = [
            "NO EXISTE",
            "01 | ENDOF - - -\n",
            "01 | EQ 1 - a\n02 | ENDOF - - -\n",
            "NOT READY",
            "01 | EQ 10 - x\n02 | EQ 2 - y\n03 | MUL x y T3\n04 | EQ T3 - a\n05 | ADD x y T5\n06 | EQ T5 - b\n07 | DIV x y T7\n08 | EQ T7 - c\n09 | SUB x y T9\n10 | EQ T9 - d\n11 | ENDOF - - -\n",
            "01 | EQ 1 - a\n02 | EQ 2 - b\n03 | EQ 0 - c\n04 | GT a b T4\n05 | GOTOF T4 - 9\n06 | ADD a 1 T6\n07 | EQ T6 - c\n08 | GOTO - - 16\n09 | BEQ b a T9\n10 | GOTOF T9 - 14\n11 | ADD b 1 T11\n12 | EQ T11 - c\n13 | GOTO - - 16\n14 | ADD 1 2 T14\n15 | EQ T14 - c\n16 | ENDOF - - -\n",
            "01 | EQ 1 - a\n02 | EQ 2 - b\n03 | EQ 0 - c\n04 | GT a b T4\n05 | GOTOF T4 - 9\n06 | ADD a b T6\n07 | EQ T6 - c\n08 | GOTO - - 4\n09 | ENDOF - - -\n",
            "01 | EQ 10 - b\n02 | EQ 0 - c\n03 | EQ 0 - a\n04 | LT a b T4\n05 | GOTOF T4 - 11\n06 | ADD a 1 T6\n07 | EQ T6 - a\n08 | ADD c 1 T8\n09 | EQ T8 - c\n10 | GOTO - - 4\n11 | ADD b c T11\n12 | EQ T11 - b\n13 | ENDOF - - -\n",
            "NOT READY",
            '01 | EQ 0 - a\n02 | EQ "hola me llamo" - saludo\n03 | ADD saludo nombre T3\n04 | EQ T3 - saludo\n05 | ADD saludo "y mi edad es " T5\n06 | EQ T5 - saludo\n07 | ADD saludo edad T7\n08 | EQ T7 - saludo\n09 | ENDFUNC - - -\n10 | EQ "Rosita" - n\n11 | EQ "22" - e\n12 | ERA hola - -\n13 | param n - param1\n14 | param e - param2\n15 | ADD a 1 T15\n16 | param T15 - param3\n17 | GOSUB hola - 2\n18 | ENDOF - - -\n',
        ]
        test_results = []
        test_results.append(test_file("tests/test_1.txt", test_answers[1]))
        test_results.append(test_file("tests/test_2.txt", test_answers[2]))
        # Pendiente -> return y asignación de funciones? creo?
        # test_results.append(test_file("tests/test_3.txt", test_answers[3]))
        test_results.append(test_file("tests/test_4.txt", test_answers[4]))
        test_results.append(test_file("tests/test_5.txt", test_answers[5]))
        test_results.append(test_file("tests/test_6.txt", test_answers[6]))
        test_results.append(test_file("tests/test_7.txt", test_answers[7]))
        # Pendiente -> Simple For
        # test_results.append(test_file("tests/test_8.txt", test_answers[8]))
        test_results.append(test_file("tests/test_9.txt", test_answers[9]))
        if "F" in test_results:
            result = "Failed"
        else:
            result = "Passed"

        self.assertEqual(result, "Passed")


class TestSymbol(unittest.TestCase):
    def test_symbol(self):
        s = Symbol("variable", "int")
        self.assertEqual(s.name, "variable")
        self.assertEqual(s.type, "INT")


class TestVarTable(unittest.TestCase):
    def test_push_variable(self):
        vt = VariableTable()

        s = Symbol("variable", "int")
        vt.set_variable(s, 12)
        self.assertEqual(vt.variables[s.name], ["INT", 12])

        s = Symbol("variable", "int")
        vt.set_variable(s, 23)
        self.assertEqual(vt.variables[s.name], ["INT", 23])


class TestFuncTable(unittest.TestCase):
    def test_push_function(self):
        ft = FunctionTable()
        vt = VariableTable()

        s = Symbol("variable", "int")
        vt.set_variable(s, 12)
        ft.set_function("print_something", "void", [s], vt)
        self.assertEqual(
            ft.functions["print_something"], {"t": "void", "p": [s], "s": 0, "vt": vt}
        )

        ft.set_function("calculate_something", "float", [], None)
        self.assertEqual(
            ft.functions["calculate_something"],
            {"t": "float", "p": [], "s": 0, "vt": None},
        )


class TestLexer(unittest.TestCase):
    def test_lexer(self):
        lexer = lex.lex()
        lexer.input("program test : { a = 1; b = true }")

        lexer_values = []
        lexer_types = []

        expected_values = [
            "program",
            "test",
            ":",
            "{",
            "a",
            "=",
            1,
            ";",
            "b",
            "=",
            "true",
            "}",
        ]

        expected_types = [
            "PROGRAM",
            "ID",
            "COL",
            "OCB",
            "ID",
            "EQ",
            "CINT",
            "SCOL",
            "ID",
            "EQ",
            "TRUE",
            "CCB",
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
        s_addeq = Symbol("ADDEQ", "assignment_operation")
        s_eq = Symbol("ADDEQ", "assignment")

        # Non-existent type
        s_doub = Symbol("double", "DOUBLE")

        # TODO: This consideration is no loger done with symbols. But I don't want to delete the tests yet
        self.assertEqual(SemanticTable.considerate(s_flt, s_add, s_int), "FLT")
        self.assertEqual(SemanticTable.considerate(s_flt, s_sub, s_null), "error")
        self.assertEqual(SemanticTable.considerate(s_char, s_lt, s_str), "BOOL")
        self.assertEqual(SemanticTable.considerate(s_null, s_beq, s_bool), "BOOL")
        self.assertEqual(SemanticTable.considerate(s_doub, s_add, s_char), "error")
        self.assertEqual(SemanticTable.considerate(s_int, s_addeq, s_int), "INT")
        self.assertEqual(SemanticTable.considerate(s_int, s_addeq, s_null), "error")
        self.assertEqual(SemanticTable.considerate(s_flt, s_eq, s_flt), "FLT")
        self.assertEqual(SemanticTable.considerate(s_flt, s_eq, s_int), "error")

        # Consideration with strings
        self.assertEqual(SemanticTable.considerate("FLT", "ADD", "INT"), "FLT")
        self.assertEqual(SemanticTable.considerate("FLT", "SUB", "NULL"), "error")
        self.assertEqual(SemanticTable.considerate("CHAR", "LT", "STR"), "BOOL")
        self.assertEqual(SemanticTable.considerate("NULL", "BEQ", "BOOL"), "BOOL")
        self.assertEqual(SemanticTable.considerate("DOUBLE", "ADD", "CHAR"), "error")
        self.assertEqual(SemanticTable.considerate("INT", "ADDEQ", "INT"), "INT")
        self.assertEqual(SemanticTable.considerate("INT", "ADDEQ", "NULL"), "error")
        self.assertEqual(SemanticTable.considerate("FLT", "EQ", "FLT"), "FLT")
        self.assertEqual(SemanticTable.considerate("FLT", "EQ", "INT"), "error")


class TestQuadruple(unittest.TestCase):
    def test_arithmetic_expression(self):
        def format_response(quad_response):
            if type(quad_response) == str:
                return quad_response

            response = []
            for quad in quad_response:
                response.append(quad.format_quadruple())

            return response

        expected_response = [
            "MUL B C T1",
            "DIV T1 D T2",
            "ADD A T2 T3",
            "MUL E F T4",
            "SUB T3 T4 T5",
        ]

        expression_in_symbols = [
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
            Symbol("F", "FLT"),
        ]

        response = format_response(
            Quadruple.arithmetic_expression(expression_in_symbols, 1)
        )
        self.assertEqual(response, expected_response)

        expression_in_string = "A + B * C / D - E * F"
        response = format_response(
            Quadruple.arithmetic_expression(expression_in_string, 1)
        )
        self.assertEqual(response, expected_response)

        expression_with_parentheses = "A + B * ( C - D )"
        expected_response_parentheses = ["SUB C D T1", "MUL B T1 T2", "ADD A T2 T3"]

        response = format_response(
            Quadruple.arithmetic_expression(expression_with_parentheses, 1)
        )
        self.assertEqual(response, expected_response_parentheses)

        expression_with_comparison_operators = "A + B >= C * D"
        expected_response_comparison_operators = [
            "ADD A B T1",
            "MUL C D T2",
            "GTE T1 T2 T3",
        ]

        response = format_response(
            Quadruple.arithmetic_expression(expression_with_comparison_operators, 1)
        )
        self.assertEqual(response, expected_response_comparison_operators)

        expression_with_matching_operators = "A + B != C * D"
        expected_response_matching_operators = [
            "ADD A B T1",
            "MUL C D T2",
            "BNEQ T1 T2 T3",
        ]

        response = format_response(
            Quadruple.arithmetic_expression(expression_with_matching_operators, 1)
        )
        self.assertEqual(response, expected_response_matching_operators)

        # !A || B < C + D * E && (F != G)
        expression_with_all_type_operators = [
            Symbol("NOT", "not"),
            Symbol("A", "BOOL"),
            Symbol("OR", "matching"),
            Symbol("B", "INT"),
            Symbol("LT", "comparison"),
            Symbol("C", "FLT"),
            Symbol("ADD", "operation"),
            Symbol("D", "INT"),
            Symbol("MUL", "operation"),
            Symbol("E", "FLT"),
            Symbol("AND", "matching"),
            Symbol("OP", "parentheses"),
            Symbol("F", "STR"),
            Symbol("BNEQ", "matching"),
            Symbol("G", "CHAR"),
            Symbol("CP", "parentheses"),
        ]

        expected_response_with_all_type_operators = [
            "NOT A None T1",
            "MUL D E T2",
            "ADD C T2 T3",
            "BNEQ F G T4",
            "AND T3 T4 T5",
            "LT B T5 T6",
            "OR T1 T6 T7",
        ]

        response = format_response(
            Quadruple.arithmetic_expression(expression_with_all_type_operators, 1)
        )
        self.assertEqual(response, expected_response_with_all_type_operators)

        expression_with_uncompatible_types = [
            Symbol("A", "INT"),
            Symbol("ADD", "operation"),
            Symbol("B", "BOOL"),
        ]

        response = format_response(
            Quadruple.arithmetic_expression(expression_with_uncompatible_types, 1)
        )
        self.assertEqual(response, "error: non-compatible types")

        expression_with_not_and_int = [
            Symbol("NOT", "not"),
            Symbol("A", "INT"),
        ]

        response = format_response(
            Quadruple.arithmetic_expression(expression_with_uncompatible_types, 1)
        )
        self.assertEqual(response, "error: non-compatible types")

        assignment_expression = [
            Symbol("A", "FLT"),
            Symbol("EQ", "assignment"),
            Symbol("B", "FLT"),
            Symbol("ADD", "operation"),
            Symbol("C", "FLT"),
        ]
        expected_response = [
            "ADD B C T1",
            "EQ T1 None A",
        ]
        response = format_response(
            Quadruple.arithmetic_expression(assignment_expression, 1)
        )
        self.assertEqual(response, expected_response)

        assignment_sub_expression = [
            Symbol("A", "FLT"),
            Symbol("SUBEQ", "assignment_operation"),
            Symbol("B", "FLT"),
            Symbol("ADD", "operation"),
            Symbol("C", "FLT"),
        ]
        expected_response = [
            "ADD B C T1",
            "SUBEQ T1 None A",
        ]
        response = format_response(
            Quadruple.arithmetic_expression(assignment_sub_expression, 1)
        )
        self.assertEqual(response, expected_response)

        wrong_type_assignation = [
            Symbol("A", "INT"),
            Symbol("EQ", "assignment"),
            Symbol("B", "FLT"),
        ]

        response = format_response(
            Quadruple.arithmetic_expression(wrong_type_assignation, 1)
        )
        self.assertEqual(response, "error: non-compatible types")

    def test_format_expression(self):
        in_string_with_spaces = "Ab = B >= C / ( D - E ) * F < G || H"
        in_string_without_spaces = "Ab=B>=C/(D-E)*F<G||H"

        in_list_of_strings = [
            "Ab",
            "=",
            "B",
            ">=",
            "C",
            "/",
            "(",
            "D",
            "-",
            "E",
            ")",
            "*",
            "F",
            "<",
            "G",
            "||",
            "H",
        ]

        in_list_of_symbols = [
            Symbol("Ab", "FLT"),
            Symbol("EQ", "assignment"),
            Symbol("B", "FLT"),
            Symbol("GTE", "comparison"),
            Symbol("C", "FLT"),
            Symbol("DIV", "operation"),
            Symbol("OP", "parentheses"),
            Symbol("D", "FLT"),
            Symbol("SUB", "operation"),
            Symbol("E", "FLT"),
            Symbol("CP", "parentheses"),
            Symbol("MUL", "operation"),
            Symbol("F", "FLT"),
            Symbol("LT", "comparison"),
            Symbol("G", "FLT"),
            Symbol("OR", "matching"),
            Symbol("H", "FLT"),
        ]

        self.assertEqual(
            Quadruple.format_expression(in_string_with_spaces), in_list_of_symbols
        )
        self.assertEqual(
            Quadruple.format_expression(in_string_without_spaces), in_list_of_symbols
        )
        self.assertEqual(
            Quadruple.format_expression(in_list_of_strings), in_list_of_symbols
        )
        self.assertEqual(
            Quadruple.format_expression(in_list_of_symbols), in_list_of_symbols
        )

    def test_evaluate_symbol(self):
        symbol = Symbol("SUB", "operation")
        stack_values = ["A", "B"]
        stack_operators = ["ADD"]
        stack_types = ["FLT", "FLT"]
        resulting_quads = []
        result_quadruple_id = 1

        result = Quadruple.evaluate_symbol(
            symbol,
            stack_values,
            stack_operators,
            stack_types,
            resulting_quads,
            result_quadruple_id,
        )

        resulting_quads_formatted = []
        for quad in resulting_quads:
            resulting_quads_formatted.append(quad.format_quadruple())

        # Do the operation
        self.assertEqual(result, result_quadruple_id + 1)
        self.assertEqual(stack_values, ["T1"])
        self.assertEqual(stack_operators, ["SUB"])
        self.assertEqual(stack_types, ["FLT"])
        self.assertEqual(resulting_quads_formatted, ["ADD A B T1"])

    def test_format_quadruple(self):
        q = Quadruple(
            Symbol("MUL", "operation"),
            Symbol("B", "FLT"),
            Symbol("C", "FLT"),
            Symbol("T1", "FLT"),
        )
        self.assertEqual(q.format_quadruple(), "MUL B C T1")
