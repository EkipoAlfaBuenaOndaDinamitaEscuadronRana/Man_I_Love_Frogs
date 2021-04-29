from semantic_table import *


class Quadruple(object):
    def __init__(self, operator, operand_1, operand_2, result_id):
        self.operator = operator
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.result_id = result_id

    def __divide_expression(expression):
        exp = []
        operand = ""

        for symbol in expression:
            if symbol in ["+", "-", "*", "/", "%"]:
                exp.append(operand)
                exp.append(symbol)
                operand = ""

            else:
                operand += symbol

        if len(operand):
            exp.append(operand)

        return exp

    def __another_op_mdr_in_stack(stack_operators):
        return any(item in ["MUL", "DIV", "MOD"] for item in stack_operators)

    def __another_op_as_in_stack(stack_operators):
        return any(item in ["ADD", "SUB"] for item in stack_operators)

    def __generate_quadruple(
        stack_values, stack_operators, result_quadruple_id, final_ops
    ):
        result_id = "T" + str(result_quadruple_id)

        q = Quadruple(
            stack_operators.pop(), stack_values[-2], stack_values[-1], result_id
        )

        del stack_values[-2:]

        final_ops.append(q)
        stack_values.append(result_id)

    # TODO: Todavía no considera tipos basados en la tabla semantica
    # TODO: Todavía no considera tipos de comparison o matching
    # TODO: No considera parentesis
    # TODO: No considera constantes (1, 1.5, "algo asi")
    def arithmetic_expression(expression):
        # Examples:
        stack_values = []  # ["A", "B"]
        stack_operators = []  # ["ADD"]
        stack_types = []  # ["INT", "FLT"]

        final_ops = []
        result_quadruple_id = 1

        # for symbol in format_expression(expression):
        for symbol in Quadruple.format_expression(expression):

            s_type = symbol.type  # operation
            s_name = symbol.name  # +

            # is an operand
            if s_type in SemanticTable.types:
                stack_values.append(s_name)
                stack_types.append(s_type)

            # is an operator
            elif s_type in ["operation", "comparison", "matching"]:

                if s_name in ["MUL", "DIV", "MOD"]:

                    # There is another operator of multiplication, division or residue
                    if Quadruple.__another_op_mdr_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            final_ops,
                        )
                        result_quadruple_id += 1

                # Addition and substraction case
                elif s_name in ["ADD", "SUB"]:

                    # There is another operator on the stack
                    if Quadruple.__another_op_mdr_in_stack(
                        stack_operators
                    ) or Quadruple.__another_op_as_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            final_ops,
                        )
                        result_quadruple_id += 1

                        # There is another operator of sum or addition
                        if Quadruple.__another_op_as_in_stack(stack_operators):
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                final_ops,
                            )
                            result_quadruple_id += 1

                stack_operators.append(s_name)

            # is a parenthesis
            elif s_type == "parentheses":
                pass

            # is an unknown character
            else:
                return "error: type {} not found".format(s_type)

        while len(stack_operators):
            Quadruple.__generate_quadruple(
                stack_values, stack_operators, result_quadruple_id, final_ops
            )
            result_quadruple_id += 1

        return final_ops

    def format_quadruple(self):
        return "{} {} {} {}".format(
            self.operator, self.operand_1, self.operand_2, self.result_id
        )

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
                    "<": Symbol("LT", "comparison"),
                    ">": Symbol("GT", "comparison"),
                    "<=": Symbol("LTE", "comparison"),
                    ">=": Symbol("GTE", "comparison"),
                    "==": Symbol("BEQ", "matching"),
                    "!=": Symbol("BNEQ", "matching"),
                    "||": Symbol("OR", "matching"),
                    "&&": Symbol("AND", "matching"),
                }

                response.append(operators.get(symbol, Symbol(symbol, "FLT")))
        
        return response
