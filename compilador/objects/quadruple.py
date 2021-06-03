from router_solver import *
import compilador.objects.semantic_table
from compilador.objects.semantic_table import *

# CLASE QUADRUPLE
# Objeto que guarda operando, operadores y resultado de una expresión o instrucción


class Quadruple(object):
    def __init__(self, operator, operand_1, operand_2, result_id):
        self.operator = operator  # Operador o instrucción de cuadruplo
        self.operand_1 = operand_1  # Primer operador
        self.operand_2 = operand_2  # Segundo operador
        self.result_id = result_id  # Operador donde se asigna el resultado
        self.scope = None

    # Guarda operadores de expresiones aritmeticas
    def __is_operator(symbol):
        return symbol in [
            "+",
            "-",
            "*",
            "/",
            "%",
            "(",
            ")",
            ">",
            "<",
            "=",
            "|",
            "&",
            "!",
        ]

    # Guarda nombres de operadores de asignación y asignación compuesta
    def __is_assignment(operator):
        return operator in [
            "EQ",
            "ADDEQ",
            "SUBEQ",
            "MULEQ",
            "DIVEQ",
            "MODEQ",
        ]

    # Recibe como input una expresión tipo string y la divide en simbolos
    def __divide_expression(expression):
        exp = []
        operand = ""
        i = 0

        while i < len(expression):
            symbol = expression[i]

            if Quadruple.__is_operator(symbol):
                if len(operand):
                    exp.append(operand)

                if symbol in ["<", ">", "=", "!"] and expression[i + 1] == "=":
                    symbol += "="
                    i += 1

                elif symbol in ["|", "&"] and expression[i + 1] == symbol:
                    symbol += symbol
                    i += 1

                elif symbol in ["+", "-", "*", "/", "%"] and expression[i + 1] == "=":
                    symbol += "="
                    i += 1

                exp.append(symbol)
                operand = ""

            else:
                operand += expression[i]

            i += 1

        if len(operand):
            exp.append(operand)

        return exp

    # Elimina los parenteses del stack de operadores
    def __sub_stack_from_parentheses(stack):
        if "(" in stack:
            stack.reverse()
            index = stack.index("(")
            sub_stack = stack[:index]
            stack.reverse()

            return sub_stack

        return stack

    # Valida si hay un operador * / % en el stack
    def __another_op_mdr_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(item in ["MUL", "DIV", "MOD"] for item in sub_stack_operators)

    # Valida si hay otro operador + - en el stack
    def __another_op_as_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(item in ["ADD", "SUB"] for item in sub_stack_operators)

    # Valida si hay otro operador + - * / % en el stack
    def __another_op_as_mdr_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(
            item in ["MUL", "DIV", "MOD", "ADD", "SUB"] for item in sub_stack_operators
        )

    # Valida si hay otro operador + - * / %  > < >= <= en el stack
    def __another_op_as_mdr_comp_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(
            item in ["MUL", "DIV", "MOD", "ADD", "SUB", "GT", "LT", "GTE", "LTE"]
            for item in sub_stack_operators
        )

    # Valida si hay un operador ! en el stack
    def __a_not_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return "NOT" in sub_stack_operators

    # Valida si hay cualquier tipo de operador en el stack
    def __any_op_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return True if len(sub_stack_operators) else False

    # Consideración al hacer una expresion de tipo NOT
    def __not_consideration(stack_types):
        return "BOOL"  # if stack_types[-1] == "BOOL" else "ERROR"

    # Manda los tipos de los operandos y el operador a la tabla semantica para validar comatibilidad
    def __type_consideration(stack_types, stack_operators):
        return SemanticTable.considerate(
            stack_types[-2], stack_operators[-1], stack_types[-1]
        )

    # Genera el objeto cuadruplo con los datos del stack
    def __generate_quadruple(
        stack_values,
        stack_operators,
        result_quadruple_id,
        stack_types,
        stack_scopes,
        resulting_quads,
    ):

        result_id = "T" + str(result_quadruple_id)
        consideration = Quadruple.__type_consideration(stack_types, stack_operators)
        operator = Symbol(
            stack_operators[-1],
            SemanticTable.clasify_symbol_op(stack_operators.pop()),
            stack_scopes[-2],
        )
        operand_1 = Symbol(stack_values[-2], stack_types[-2], stack_scopes[-3])
        operand_2 = Symbol(stack_values[-1], stack_types[-1], stack_scopes[-1])
        quad_result = Symbol(result_id, consideration, stack_scopes[-2])

        q = Quadruple(operator, operand_1, operand_2, quad_result)

        del stack_types[-2:]
        del stack_values[-2:]
        del stack_scopes[-3:]

        stack_types.append(consideration)
        resulting_quads.append(q)
        stack_values.append(result_id)
        stack_scopes.append(q.result_id.scope)

    # Genera el cuadruplo de una expresion de tipo NOT !
    def __generate_not_quadruple(
        stack_values,
        stack_operators,
        result_quadruple_id,
        stack_types,
        stack_scopes,
        resulting_quads,
    ):
        result_id = "T" + str(result_quadruple_id)
        consideration = Quadruple.__not_consideration(stack_types)
        operator = Symbol(stack_operators.pop(), "not", stack_scopes[-2])
        value = Symbol(stack_values.pop(), stack_types.pop(), stack_scopes.pop())
        quad_result = Symbol(result_id, consideration, stack_scopes.pop())

        q = Quadruple(operator, value, None, quad_result)

        stack_types.append(consideration)
        resulting_quads.append(q)
        stack_values.append(result_id)
        stack_scopes.append(q.result_id.scope)

    # Genera el cuadruplo de una expresion de tipo EQ =

    def __generate_assignment_quadruple(
        stack_values,
        stack_operators,
        result_quadruple_id,
        stack_types,
        stack_scopes,
        resulting_quads,
    ):
        consideration = Quadruple.__type_consideration(stack_types, stack_operators)
        operator = Symbol(stack_operators.pop(), "assignment", stack_scopes[-2])
        value = Symbol(stack_values.pop(), stack_types[-1], stack_scopes[-1])
        quad_result = Symbol(stack_values.pop(), stack_types[-1], stack_scopes[-3])

        stack_types.append(consideration)
        q = Quadruple(operator, value, None, quad_result)
        resulting_quads.append(q)

    # Saca los datos de un simbolo, revisa que hay en el stack y toma acción ante ello
    def evaluate_symbol(
        symbol,
        stack_values,
        stack_operators,
        stack_types,
        stack_scopes,
        resulting_quads,
        result_quadruple_id,
    ):
        if symbol.address_flag:
            s_type = symbol.address_flag
        else:
            s_type = symbol.type

        s_name = symbol.name
        s_scope = symbol.scope

        # is it is a ! operator
        if s_type == "not":
            stack_operators.append("NOT")
            stack_scopes.append(s_scope)

        # is an assignment or an assignment operator
        elif s_type in ["assignment", "assignment_operation"]:
            stack_operators.append(s_name)
            stack_scopes.append(s_scope)

        # is a value
        elif s_type in SemanticTable.types:
            stack_values.append(s_name)
            stack_types.append(s_type)
            stack_scopes.append(s_scope)

            if Quadruple.__a_not_in_stack(stack_operators):
                Quadruple.__generate_not_quadruple(
                    stack_values,
                    stack_operators,
                    result_quadruple_id,
                    stack_types,
                    stack_scopes,
                    resulting_quads,
                )

                if resulting_quads[-1].result_id.type == "ERROR":
                    return "ERROR: non-compatible types"

                result_quadruple_id += 1

        # is an operator
        elif s_type in ["operation", "comparison", "matching"]:

            # Multiplication, Divition and Residue cases
            if s_name in ["MUL", "DIV", "MOD"]:

                # There is another operator of multiplication, division or residue
                if Quadruple.__another_op_mdr_in_stack(stack_operators):
                    Quadruple.__generate_quadruple(
                        stack_values,
                        stack_operators,
                        result_quadruple_id,
                        stack_types,
                        stack_scopes,
                        resulting_quads,
                    )

                    if stack_types[-1] == "ERROR":
                        return "ERROR: non-compatible types"

                    result_quadruple_id += 1

            # Addition and substraction cases
            elif s_name in ["ADD", "SUB"]:

                # There is another operator on the stack
                if Quadruple.__another_op_as_mdr_in_stack(stack_operators):
                    Quadruple.__generate_quadruple(
                        stack_values,
                        stack_operators,
                        result_quadruple_id,
                        stack_types,
                        stack_scopes,
                        resulting_quads,
                    )

                    if stack_types[-1] == "ERROR":
                        return "ERROR: non-compatible types"

                    result_quadruple_id += 1

                    # There is another operator of sum or addition
                    if Quadruple.__another_op_as_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            stack_types,
                            stack_scopes,
                            resulting_quads,
                        )

                        if stack_types[-1] == "ERROR":
                            return "ERROR: non-compatible types"

                        result_quadruple_id += 1

            # Comparison operators case
            elif s_name in ["GT", "LT", "GTE", "LTE"]:

                # There is another mathematical and comparison operator on the stack
                if Quadruple.__another_op_as_mdr_comp_in_stack(stack_operators):
                    Quadruple.__generate_quadruple(
                        stack_values,
                        stack_operators,
                        result_quadruple_id,
                        stack_types,
                        stack_scopes,
                        resulting_quads,
                    )

                    if stack_types[-1] == "ERROR":
                        return "ERROR: non-compatible types"

                    result_quadruple_id += 1

                    # There is another mathematical operator in stack
                    if Quadruple.__another_op_as_mdr_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            stack_types,
                            stack_scopes,
                            resulting_quads,
                        )

                        if stack_types[-1] == "ERROR":
                            return "ERROR: non-compatible types"

                        result_quadruple_id += 1

                        # There is another operator of sum or addition
                        if Quadruple.__another_op_as_in_stack(stack_operators):
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                stack_types,
                                stack_scopes,
                                resulting_quads,
                            )

                            if stack_types[-1] == "ERROR":
                                return "ERROR: non-compatible types"

                            result_quadruple_id += 1

            # matching operators case
            elif s_name in ["BEQ", "BNEQ", "OR", "AND"]:

                # There is any another operator on the stack
                if Quadruple.__any_op_in_stack(stack_operators):
                    Quadruple.__generate_quadruple(
                        stack_values,
                        stack_operators,
                        result_quadruple_id,
                        stack_types,
                        stack_scopes,
                        resulting_quads,
                    )

                    if stack_types[-1] == "ERROR":
                        return "ERROR: non-compatible types"

                    result_quadruple_id += 1

                    # There is another mathematical and comparison operator on the stack
                    if Quadruple.__another_op_as_mdr_comp_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            stack_types,
                            stack_scopes,
                            resulting_quads,
                        )

                        if stack_types[-1] == "ERROR":
                            return "ERROR: non-compatible types"

                        result_quadruple_id += 1

                        # There is another mathematical operator in stack
                        if Quadruple.__another_op_as_mdr_in_stack(stack_operators):
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                stack_types,
                                stack_scopes,
                                resulting_quads,
                            )

                            if stack_types[-1] == "ERROR":
                                return "ERROR: non-compatible types"

                            result_quadruple_id += 1

                            # There is another operator of sum or addition
                            if Quadruple.__another_op_as_in_stack(stack_operators):
                                Quadruple.__generate_quadruple(
                                    stack_values,
                                    stack_operators,
                                    result_quadruple_id,
                                    stack_types,
                                    stack_scopes,
                                    resulting_quads,
                                )

                                if stack_types[-1] == "ERROR":
                                    return "ERROR: non-compatible types"

                                result_quadruple_id += 1

            stack_operators.append(s_name)
            stack_scopes.append(s_scope)

        # is a parentheses
        elif s_type == "parentheses":
            # When a ( arrives
            if s_name == "OP":
                stack_values.append("(")
                stack_operators.append("(")

            # When a ) arrives
            elif s_name == "CP":
                # case when there is just one value inside parenthesis example: A + (B)
                if len(stack_operators) == 0:
                    stack_values.pop(-2)
                    stack_operators.pop()

                else:
                    while stack_operators[-1] != "(":
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            stack_types,
                            stack_scopes,
                            resulting_quads,
                        )

                        if stack_types[-1] == "ERROR":
                            return "ERROR: non-compatible types"

                        result_quadruple_id += 1

                    stack_operators.pop()
                    stack_values.pop(-2)

        # is an unknown character
        else:
            return "ERROR: type {} not found".format(s_type)

        return result_quadruple_id

    # Recibe lista de simbolos de la expresion
    # llama a evaluación de expresión y generación cuadruplo
    def arithmetic_expression(expression, result_quadruple_id):
        stack_values = []  # ["A", "B"]
        stack_operators = []  # ["ADD"]
        stack_types = []  # ["INT", "FLT"]
        stack_scopes = []
        resulting_quads = []

        for symbol in Quadruple.format_expression(expression):
            result_quadruple_id = Quadruple.evaluate_symbol(
                symbol,
                stack_values,
                stack_operators,
                stack_types,
                stack_scopes,
                resulting_quads,
                result_quadruple_id,
            )

            if type(result_quadruple_id) != int:
                return result_quadruple_id

        while len(stack_operators):
            if Quadruple.__is_assignment(stack_operators[-1]):
                Quadruple.__generate_assignment_quadruple(
                    stack_values,
                    stack_operators,
                    result_quadruple_id,
                    stack_types,
                    stack_scopes,
                    resulting_quads,
                )

                if stack_types[-1] == "ERROR":
                    return "ERROR: non-compatible types"

            else:
                Quadruple.__generate_quadruple(
                    stack_values,
                    stack_operators,
                    result_quadruple_id,
                    stack_types,
                    stack_scopes,
                    resulting_quads,
                )

                if stack_types[-1] == "ERROR":
                    return "ERROR: non-compatible types"

            result_quadruple_id += 1

        # resulting_quads.append(result_quadruple_id)
        return resulting_quads

    # Si recibe una expresión de tipo string la convierte a simbolos
    # NOTA : se espera que se reciban simbolos siempre
    #        pero se valida para evitar errores
    def format_expression(expression):
        response = []

        if type(expression) == str:
            expression = expression.replace(" ", "")
            expression = Quadruple.__divide_expression(expression)

        for symbol in expression:
            s_type = type(symbol)

            if s_type == Symbol:
                response.append(symbol)

            elif s_type == str:
                operators = {
                    "+": Symbol("ADD", "operation"),
                    "-": Symbol("SUB", "operation"),
                    "*": Symbol("MUL", "operation"),
                    "/": Symbol("DIV", "operation"),
                    "%": Symbol("MOD", "operation"),
                    "(": Symbol("OP", "parentheses"),
                    ")": Symbol("CP", "parentheses"),
                    "!": Symbol("NOT", "not"),
                    "=": Symbol("EQ", "assignment"),
                    "<": Symbol("LT", "comparison"),
                    ">": Symbol("GT", "comparison"),
                    "<=": Symbol("LTE", "comparison"),
                    ">=": Symbol("GTE", "comparison"),
                    "==": Symbol("BEQ", "matching"),
                    "!=": Symbol("BNEQ", "matching"),
                    "||": Symbol("OR", "matching"),
                    "+=": Symbol("ADDEQ", "assignment_operation"),
                    "-=": Symbol("SUBEQ", "assignment_operation"),
                    "*=": Symbol("MULEQ", "assignment_operation"),
                    "/=": Symbol("DIVEQ", "assignment_operation"),
                    "%=": Symbol("MODEQ", "assignment_operation"),
                }

                response.append(operators.get(symbol, Symbol(symbol, "FLT")))

        return response

    # Imprime cuadruplo
    def print_quad(self):
        if type(self.operator) == Symbol:
            print("OPERATOR: ")
            self.operator.print_symbol()
            print()
        else:
            print("OPERATOR: \n{}\n".format(self.operator))

        if type(self.operand_1) == Symbol:
            print("OPERAND_1: ")
            self.operand_1.print_symbol()
            print()
        else:
            print("OPERAND_1: \n{}\n".format(self.operand_1))

        if type(self.operand_2) == Symbol:
            print("OPERAND_2: ")
            self.operand_2.print_symbol()
            print()
        else:
            print("OPERAND_2: \n{}\n".format(self.operand_2))

        if type(self.result_id) == Symbol:
            print("RESULT_ID:")
            self.result_id.print_symbol()
            print()
        else:
            print("RESULT_ID: \n{}\n".format(self.result_id))

    def print_quads(quads, header=None):
        if header:
            print("----------------{}-----------------".format(header))
        for q in quads:
            quads[q].print_quad()
            print("------------------------------------")
