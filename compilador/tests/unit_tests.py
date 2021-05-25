from router_solver import *
import game_engine.game_engine_tests
import compilador.objects.function_table
import compilador.objects.quadruple
import compilador.lexer
import compilador.parser
import compilador.helpers.file_parser
import compilador.vm.virtual_machine
from compilador.objects.function_table import *
from compilador.objects.quadruple import *
from compilador.lexer import *
from compilador.parser import *
from compilador.helpers.file_parser import *
from compilador.vm.virtual_machine import *
from game_engine.game_engine_tests import *
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
            "*",
            "01 | GOTO - - 2\n02 | ENDOF - - -\n",
            "01 | GOTO - - 2\n02 | EQ 1 - a\n03 | ENDOF - - -\n",
            "01 | GOTO - - 6\n02 | EQ 2 - b\n03 | MUL a a T1\n04 | RETURN T1 - -\n05 | ENDFUNC - - -\n06 | EQ 10 - x\n07 | BEQ x 10 T1\n08 | GOTOF T1 - 14\n09 | ERA square - -\n10 | PARAM a - param1\n11 | GOSUB square - 3\n12 | EQ square - T2\n13 | EQ T2 - b\n14 | ENDOF - - -\n",
            "01 | GOTO - - 2\n02 | EQ 10 - x\n03 | EQ 2 - y\n04 | MUL x y T1\n05 | EQ T1 - a\n06 | ADD x y T2\n07 | EQ T2 - b\n08 | DIV x y T3\n09 | EQ T3 - c\n10 | SUB x y T4\n11 | EQ T4 - d\n12 | ENDOF - - -\n",
            "01 | GOTO - - 5\n02 | EQ 1 - a\n03 | EQ 2 - b\n04 | EQ 0 - c\n05 | GT a b T1\n06 | GOTOF T1 - 10\n07 | ADD a 1 T2\n08 | EQ T2 - c\n09 | GOTO - - 17\n10 | BEQ b a T3\n11 | GOTOF T3 - 15\n12 | ADD b 1 T4\n13 | EQ T4 - c\n14 | GOTO - - 17\n15 | ADD 1 2 T5\n16 | EQ T5 - c\n17 | ENDOF - - -\n",
            "01 | GOTO - - 5\n02 | EQ 1 - a\n03 | EQ 2 - b\n04 | EQ 0 - c\n05 | GT a b T1\n06 | GOTOF T1 - 10\n07 | ADD a b T2\n08 | EQ T2 - c\n09 | GOTO - - 5\n10 | ENDOF - - -\n",
            "01 | GOTO - - 4\n02 | EQ 10 - b\n03 | EQ 0 - c\n04 | EQ 0 - a\n05 | LT a b T1\n06 | GOTOF T1 - 12\n07 | ADD a 1 T2\n08 | EQ T2 - a\n09 | ADD c 1 T3\n10 | EQ T3 - c\n11 | GOTO - - 5\n12 | ADD b c T4\n13 | EQ T4 - b\n14 | ENDOF - - -\n",
            "*",
            '01 | GOTO - - 11\n02 | EQ 0 - a\n03 | EQ "hola me llamo" - saludo\n04 | ADD saludo nombre T1\n05 | EQ T1 - saludo\n06 | ADD saludo "y mi edad es " T2\n07 | EQ T2 - saludo\n08 | ADD saludo edad T3\n09 | EQ T3 - saludo\n10 | ENDFUNC - - -\n11 | EQ "Rosita" - n\n12 | EQ "22" - e\n13 | ERA hola - -\n14 | PARAM n - param1\n15 | PARAM e - param2\n16 | ADD a 1 T1\n17 | PARAM T1 - param3\n18 | GOSUB hola - 3\n19 | ENDOF - - -\n',
            "01 | GOTO - - 20\n02 | EQ 0 - respuesta\n03 | MUL b c T1\n04 | ADD a T1 T2\n05 | EQ T2 - respuesta\n06 | GT a b T3\n07 | GOTOF T3 - 11\n08 | RETURN respuesta - -\n09 | GOTO - - 19\n10 | GOTO - - 15\n11 | ADD respuesta c T4\n12 | EQ T4 - respuesta\n13 | RETURN respuesta - -\n14 | GOTO - - 19\n15 | ADD a b T5\n16 | SUB T5 c T6\n17 | EQ T6 - a\n18 | RETURN a - -\n19 | ENDFUNC - - -\n20 | ERA random - -\n21 | PARAM 5 - param1\n22 | PARAM -10 - param2\n23 | PARAM 4 - param3\n24 | GOSUB random - 2\n25 | EQ random - T1\n26 | ADD 1 T1 T2\n27 | EQ T2 - a\n28 | ERA random - -\n29 | PARAM a - param1\n30 | PARAM 3 - param2\n31 | PARAM 100 - param3\n32 | GOSUB random - 2\n33 | EQ random - T3\n34 | EQ T3 - b\n35 | ERA random - -\n36 | ERA random - -\n37 | PARAM 5 - param1\n38 | PARAM 5 - param2\n39 | PARAM 5 - param3\n40 | GOSUB random - 2\n41 | EQ random - T4\n42 | PARAM T4 - param1\n43 | PARAM 5 - param2\n44 | PARAM 5 - param3\n45 | GOSUB random - 2\n46 | EQ random - T5\n47 | EQ T5 - c\n48 | ERA random - -\n49 | PARAM 1 - param1\n50 | PARAM 2 - param2\n51 | PARAM 3 - param3\n52 | GOSUB random - 2\n53 | EQ random - T6\n54 | ERA random - -\n55 | PARAM 4 - param1\n56 | PARAM 5 - param2\n57 | PARAM 6 - param3\n58 | GOSUB random - 2\n59 | EQ random - T7\n60 | ADD T7 T6 T8\n61 | EQ T8 - d\n62 | ENDOF - - -\n",
            "01 | GOTO - - 2\n02 | EQ READ - a\n03 | EQ READ - b\n04 | EQ READ - c\n05 | ENDOF - - -\n",
            '01 | GOTO - - 2\n02 | EQ 1 - a\n03 | EQ "cowboy" - pepe.hat\n04 | JL pepe - 1\n05 | JR pepe - 10\n06 | JU pepe - a\n07 | ENDOF - - -\n',
            "01 | GOTO - - 15\n02 | BEQ n 0 T1\n03 | GOTOF T1 - 7\n04 | RETURN 1 - -\n05 | GOTO - - 14\n06 | GOTO - - 15\n07 | ERA factorial - -\n08 | SUB n 1 T2\n09 | PARAM T2 - param1\n10 | GOSUB factorial - 2\n11 | EQ factorial - T3\n12 | MUL n T3 T4\n13 | RETURN T4 - -\n14 | ENDFUNC - - -\n15 | ERA factorial - -\n16 | PARAM 5 - param1\n17 | GOSUB factorial - 2\n18 | EQ factorial - T1\n19 | EQ T1 - respuesta\n20 | ENDOF - - -\n",
        ]

        test_results = []
        test_results.append(test_file("./compilador/tests/test_1.txt", test_answers[1]))
        test_results.append(test_file("./compilador/tests/test_2.txt", test_answers[2]))
        test_results.append(test_file("./compilador/tests/test_3.txt", test_answers[3]))
        test_results.append(test_file("./compilador/tests/test_4.txt", test_answers[4]))
        test_results.append(test_file("./compilador/tests/test_5.txt", test_answers[5]))
        test_results.append(test_file("./compilador/tests/test_6.txt", test_answers[6]))
        test_results.append(test_file("./compilador/tests/test_7.txt", test_answers[7]))
        # Pendiente -> Simple For
        # test_results.append(test_file("tests/test_8.txt", test_answers[8]))
        test_results.append(test_file("./compilador/tests/test_9.txt", test_answers[9]))
        test_results.append(
            test_file("./compilador/tests/test_10.txt", test_answers[10])
        )
        test_results.append(
            test_file("./compilador/tests/test_11.txt", test_answers[11])
        )
        test_results.append(
            test_file("./compilador/tests/test_12.txt", test_answers[12])
        )
        test_results.append(
            test_file("./compilador/tests/test_13.txt", test_answers[13])
        )

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

    def test_memory_size(self):
        var = Symbol("var", "INT")
        self.assertEqual(var.memory_size(), 1)
        """
        arr = Symbol("arr", "INT", [3])
        print(arr.memory_size())
        self.assertEqual(arr.memory_size(), 3)
        """


class TestVarTable(unittest.TestCase):
    def test_push_variable(self):
        vt = VariableTable()

        s = Symbol("variable", "int")
        vt.set_variable(s)
        self.assertEqual(vt.variables[s.name], s)

        s = Symbol("variable", "int")
        vt.set_variable(s)
        self.assertEqual(vt.variables[s.name], s)


class TestFuncTable(unittest.TestCase):
    def test_push_function(self):
        ft = FunctionTable()
        vt = VariableTable()

        s = Symbol("variable", "int")
        vt.set_variable(s)
        ft.set_function("print_something", "void", [s], vt)
        self.assertEqual(
            ft.functions["print_something"], {"t": "VOID", "p": [s], "s": 0, "vt": vt}
        )

        ft.set_function("calculate_something", "float", [], None)
        self.assertEqual(
            ft.functions["calculate_something"],
            {"t": "FLT", "p": [], "s": 0, "vt": None},
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
        symbol = Symbol("SUB", "operation", "main")
        stack_values = ["A", "B"]
        stack_operators = ["ADD"]
        stack_types = ["FLT", "FLT"]
        stack_scopes = ["main", "main", "main"]
        resulting_quads = []
        result_quadruple_id = 1

        result = Quadruple.evaluate_symbol(
            symbol,
            stack_values,
            stack_operators,
            stack_types,
            stack_scopes,
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
        self.assertEqual(stack_types, ["FLT"])
        self.assertEqual(stack_scopes, ["main", "main"])
        self.assertEqual(resulting_quads_formatted, ["ADD A B T1"])

    def test_format_quadruple(self):
        q = Quadruple(
            Symbol("MUL", "operation"),
            Symbol("B", "FLT"),
            Symbol("C", "FLT"),
            Symbol("T1", "FLT"),
        )
        self.assertEqual(q.format_quadruple(), "MUL B C T1")


class TestMemorySegment(unittest.TestCase):
    def test_insert_symbol(self):
        ms = MemorySegment("Global Segment", 7, 0)
        a_flt = Symbol("A", "FLT")
        b_flt = Symbol("B", "FLT")
        a_frg = Symbol("f", "FROG")

        self.assertEqual(ms.insert_symbol(a_flt), True)
        self.assertEqual(ms.insert_symbol(a_frg), True)
        self.assertEqual(ms.insert_symbol(b_flt), False)

    def search_symbol(self):
        ms = MemorySegment("Global Segment", 7, 0)

        a_int = Symbol("A", "INT")
        b_flt = Symbol("B", "FLT")
        c_str = Symbol("C", "STR")
        d_char = Symbol("D", "CHAR")
        e_bool = Symbol("E", "BOOL")
        f_null = Symbol("F", "NULL")
        g_frog = Symbol("G", "FROG")

        ms.insert_symbol(a_int)
        ms.insert_symbol(b_flt)
        ms.insert_symbol(c_str)
        ms.insert_symbol(d_char)
        ms.insert_symbol(e_bool)
        ms.insert_symbol(f_null)
        ms.insert_symbol(g_frog)

        self.assertEqual(ms.search_symbol(0), a_int)
        self.assertEqual(ms.search_symbol(1), b_flt)
        self.assertEqual(ms.search_symbol(2), c_str)
        self.assertEqual(ms.search_symbol(3), d_char)
        self.assertEqual(ms.search_symbol(4), e_bool)
        self.assertEqual(ms.search_symbol(5), f_null)
        self.assertEqual(ms.search_symbol(6), g_frog)


class TestVirtualMachine(unittest.TestCase):
    def test_insert_symbol_in_segment(self):
        ft = FunctionTable()
        vt = VariableTable()
        ft.set_function("func", "void", [], vt)
        ft.set_function("main", "void", [], vt)

        vm = VirtualMachine(7, 7, 7, ft)

        a_flt = Symbol("A", "FLT")
        b_flt = Symbol("B", "FLT")

        a_frg = Symbol("a", "FROG")
        b_frg = Symbol("b", "FROG")

        self.assertEqual(vm.insert_symbol_in_segment("Global Segment", a_flt), True)
        self.assertEqual(vm.insert_symbol_in_segment("Global Segment", b_flt), False)

        self.assertEqual(vm.insert_symbol_in_segment("func", a_frg), True)
        self.assertEqual(vm.insert_symbol_in_segment("func", b_frg), False)

    def test_get_direction_symbol(self):
        ft = FunctionTable()
        vt = VariableTable()
        ft.set_function("func1", "void", [], vt)
        ft.set_function("func2", "void", [], vt)
        ft.set_function("main", "void", [], vt)

        a_int = Symbol("A", "INT")
        b_flt = Symbol("B", "FLT")
        c_str = Symbol("C", "STR")
        d_char = Symbol("D", "CHAR")
        e_bool = Symbol("E", "BOOL")
        f_null = Symbol("F", "NULL")
        g_frog = Symbol("G", "FROG")

        # Using on a small virtual machine
        small_vm = VirtualMachine(30, 10, 60, ft)

        # Inserting in Global Segment
        small_vm.insert_symbol_in_segment("Global Segment", a_int)
        small_vm.insert_symbol_in_segment("Global Segment", b_flt)
        small_vm.insert_symbol_in_segment("Global Segment", c_str)
        small_vm.insert_symbol_in_segment("Global Segment", d_char)
        small_vm.insert_symbol_in_segment("Global Segment", e_bool)
        small_vm.insert_symbol_in_segment("Global Segment", f_null)
        small_vm.insert_symbol_in_segment("Global Segment", g_frog)

        # Inserting in Constant Segment
        small_vm.insert_symbol_in_segment("Constant Segment", a_int)
        small_vm.insert_symbol_in_segment("Constant Segment", b_flt)
        small_vm.insert_symbol_in_segment("Constant Segment", c_str)
        small_vm.insert_symbol_in_segment("Constant Segment", d_char)
        small_vm.insert_symbol_in_segment("Constant Segment", e_bool)
        small_vm.insert_symbol_in_segment("Constant Segment", f_null)
        small_vm.insert_symbol_in_segment("Constant Segment", g_frog)

        # Inserting in Local segment
        small_vm.insert_symbol_in_segment("func1", a_int)
        small_vm.insert_symbol_in_segment("func1", b_flt)
        small_vm.insert_symbol_in_segment("func1", c_str)
        small_vm.insert_symbol_in_segment("func1", d_char)
        small_vm.insert_symbol_in_segment("func1", e_bool)
        small_vm.insert_symbol_in_segment("func1", f_null)
        small_vm.insert_symbol_in_segment("func1", g_frog)

        small_vm.insert_symbol_in_segment("func2", a_int)
        small_vm.insert_symbol_in_segment("func2", b_flt)
        small_vm.insert_symbol_in_segment("func2", c_str)
        small_vm.insert_symbol_in_segment("func2", d_char)
        small_vm.insert_symbol_in_segment("func2", e_bool)
        small_vm.insert_symbol_in_segment("func2", f_null)
        small_vm.insert_symbol_in_segment("func2", g_frog)

        # Searching in Global segment
        self.assertEqual(small_vm.get_direction_symbol(0), a_int)
        self.assertEqual(small_vm.get_direction_symbol(4), b_flt)
        self.assertEqual(small_vm.get_direction_symbol(8), c_str)
        self.assertEqual(small_vm.get_direction_symbol(12), d_char)
        self.assertEqual(small_vm.get_direction_symbol(16), e_bool)
        self.assertEqual(small_vm.get_direction_symbol(20), f_null)
        self.assertEqual(small_vm.get_direction_symbol(24), g_frog)

        # Searching in Constant segment
        self.assertEqual(small_vm.get_direction_symbol(30), a_int)
        self.assertEqual(small_vm.get_direction_symbol(31), b_flt)
        self.assertEqual(small_vm.get_direction_symbol(32), c_str)
        self.assertEqual(small_vm.get_direction_symbol(33), d_char)
        self.assertEqual(small_vm.get_direction_symbol(34), e_bool)
        self.assertEqual(small_vm.get_direction_symbol(35), f_null)
        self.assertEqual(small_vm.get_direction_symbol(36), g_frog)

        # Searching in Local segment
        self.assertEqual(small_vm.get_direction_symbol(40), a_int)
        self.assertEqual(small_vm.get_direction_symbol(44), b_flt)
        self.assertEqual(small_vm.get_direction_symbol(48), c_str)
        self.assertEqual(small_vm.get_direction_symbol(52), d_char)
        self.assertEqual(small_vm.get_direction_symbol(56), e_bool)
        self.assertEqual(small_vm.get_direction_symbol(60), f_null)
        self.assertEqual(small_vm.get_direction_symbol(64), g_frog)

        self.assertEqual(small_vm.get_direction_symbol(70), a_int)
        self.assertEqual(small_vm.get_direction_symbol(74), b_flt)
        self.assertEqual(small_vm.get_direction_symbol(78), c_str)
        self.assertEqual(small_vm.get_direction_symbol(82), d_char)
        self.assertEqual(small_vm.get_direction_symbol(86), e_bool)
        self.assertEqual(small_vm.get_direction_symbol(90), f_null)
        self.assertEqual(small_vm.get_direction_symbol(94), g_frog)

        # Using on the real model of virtual machine
        real_vm = VirtualMachine(3000, 1000, 6000, ft)

        # Inserting in Global Segment
        real_vm.insert_symbol_in_segment("Global Segment", a_int)
        real_vm.insert_symbol_in_segment("Global Segment", b_flt)
        real_vm.insert_symbol_in_segment("Global Segment", c_str)
        real_vm.insert_symbol_in_segment("Global Segment", d_char)
        real_vm.insert_symbol_in_segment("Global Segment", e_bool)
        real_vm.insert_symbol_in_segment("Global Segment", f_null)
        real_vm.insert_symbol_in_segment("Global Segment", g_frog)

        # Inserting in Constant Segment
        real_vm.insert_symbol_in_segment("Constant Segment", a_int)
        real_vm.insert_symbol_in_segment("Constant Segment", b_flt)
        real_vm.insert_symbol_in_segment("Constant Segment", c_str)
        real_vm.insert_symbol_in_segment("Constant Segment", d_char)
        real_vm.insert_symbol_in_segment("Constant Segment", e_bool)
        real_vm.insert_symbol_in_segment("Constant Segment", f_null)
        real_vm.insert_symbol_in_segment("Constant Segment", g_frog)

        # Inserting in Local segment
        real_vm.insert_symbol_in_segment("func1", a_int)
        real_vm.insert_symbol_in_segment("func1", b_flt)
        real_vm.insert_symbol_in_segment("func1", c_str)
        real_vm.insert_symbol_in_segment("func1", d_char)
        real_vm.insert_symbol_in_segment("func1", e_bool)
        real_vm.insert_symbol_in_segment("func1", f_null)
        real_vm.insert_symbol_in_segment("func1", g_frog)

        real_vm.insert_symbol_in_segment("func2", a_int)
        real_vm.insert_symbol_in_segment("func2", b_flt)
        real_vm.insert_symbol_in_segment("func2", c_str)
        real_vm.insert_symbol_in_segment("func2", d_char)
        real_vm.insert_symbol_in_segment("func2", e_bool)
        real_vm.insert_symbol_in_segment("func2", f_null)
        real_vm.insert_symbol_in_segment("func2", g_frog)

        # Searching in Global segment
        self.assertEqual(real_vm.get_direction_symbol(0), a_int)
        self.assertEqual(real_vm.get_direction_symbol(428), b_flt)
        self.assertEqual(real_vm.get_direction_symbol(856), c_str)
        self.assertEqual(real_vm.get_direction_symbol(1284), d_char)
        self.assertEqual(real_vm.get_direction_symbol(1712), e_bool)
        self.assertEqual(real_vm.get_direction_symbol(2140), f_null)
        self.assertEqual(real_vm.get_direction_symbol(2568), g_frog)

        # Searching in Constant segment
        self.assertEqual(real_vm.get_direction_symbol(3000), a_int)
        self.assertEqual(real_vm.get_direction_symbol(3142), b_flt)
        self.assertEqual(real_vm.get_direction_symbol(3284), c_str)
        self.assertEqual(real_vm.get_direction_symbol(3426), d_char)
        self.assertEqual(real_vm.get_direction_symbol(3568), e_bool)
        self.assertEqual(real_vm.get_direction_symbol(3710), f_null)
        self.assertEqual(real_vm.get_direction_symbol(3852), g_frog)

        # Searching in Local segment
        self.assertEqual(real_vm.get_direction_symbol(4000), a_int)
        self.assertEqual(real_vm.get_direction_symbol(4428), b_flt)
        self.assertEqual(real_vm.get_direction_symbol(4856), c_str)
        self.assertEqual(real_vm.get_direction_symbol(5284), d_char)
        self.assertEqual(real_vm.get_direction_symbol(5712), e_bool)
        self.assertEqual(real_vm.get_direction_symbol(6140), f_null)
        self.assertEqual(real_vm.get_direction_symbol(6568), g_frog)

        self.assertEqual(real_vm.get_direction_symbol(7000), a_int)
        self.assertEqual(real_vm.get_direction_symbol(7428), b_flt)
        self.assertEqual(real_vm.get_direction_symbol(7856), c_str)
        self.assertEqual(real_vm.get_direction_symbol(8284), d_char)
        self.assertEqual(real_vm.get_direction_symbol(8712), e_bool)
        self.assertEqual(real_vm.get_direction_symbol(9140), f_null)
        self.assertEqual(real_vm.get_direction_symbol(9568), g_frog)

    def test_quadruple_direction_allocator(self):
        add = Symbol("ADD", "operation")
        a = Symbol("A", "INT")
        b = Symbol("B", "FLT")
        t1 = Symbol("T1", "FLT")

        a.scope = "Constant Segment"
        b.scope = "Constant Segment"
        t1.scope = "Constant Segment"

        self.assertEqual(a.segment_direction, None)
        self.assertEqual(a.global_direction, None)

        self.assertEqual(b.segment_direction, None)
        self.assertEqual(b.global_direction, None)

        self.assertEqual(t1.segment_direction, None)
        self.assertEqual(t1.global_direction, None)

        quad_dir = {0: Quadruple(add, a, b, t1)}

        ft = FunctionTable()
        vt = VariableTable()
        ft.set_function("main", "void", [], vt)
        real_vm = VirtualMachine(3000, 1000, 6000, ft)

        real_vm.quadruple_direction_allocator(quad_dir)

        self.assertEqual(a.segment_direction, 0)
        self.assertEqual(a.global_direction, 3000)

        self.assertEqual(b.segment_direction, 142)
        self.assertEqual(b.global_direction, 3142)

        self.assertEqual(t1.segment_direction, 143)
        self.assertEqual(t1.global_direction, 3143)
