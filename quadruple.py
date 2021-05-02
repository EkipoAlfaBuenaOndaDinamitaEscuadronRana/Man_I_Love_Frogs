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

            if symbol in ["+", "-", "*", "/", "%", "(", ")"]:
                if len(operand):
                    exp.append(operand)
                exp.append(symbol)
                operand = ""

            else:
                operand += symbol

        if len(operand):
            exp.append(operand)

        return exp

    def __another_op_mdr_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(item in ["MUL", "DIV", "MOD"] for item in sub_stack_operators)

    def __another_op_as_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(item in ["ADD", "SUB"] for item in sub_stack_operators)

    def __sub_stack_from_parentheses(stack):
        if "(" in stack:

            last_position = 0

            for i in range(len(stack)):
                if stack[i] == "(":
                    last_position = i

            return stack[-last_position:]

        return stack

    def __generate_quadruple(
        stack_values, stack_operators, result_quadruple_id, final_ops
    ):
        print("--------start: __generate_quadruple--------")
        print("stack_values: {}".format(stack_values))
        print("stack_operators: {}\n".format(stack_operators))
        result_id = "T" + str(result_quadruple_id)

        q = Quadruple(
            stack_operators.pop(), stack_values[-2], stack_values[-1], result_id
        )

        del stack_values[-2:]

        # if len(stack_operators) and stack_operators[-1] == "OP":
        #     stack_values.pop()
        #     stack_operators.pop()

        print("--------end: __generate_quadruple--------")
        print("stack_values: {}".format(stack_values))
        print("stack_operators: {}\n".format(stack_operators))

        final_ops.append(q)
        stack_values.append(result_id)

    # TODO: Todavía no considera tipos basados en la tabla semantica
    # TODO: Todavía no considera tipos de comparison o matching
    # TODO: No considera parentesis
    # TODO: No considera constantes (1, 1.5, "algo asi")
    # TODO: No valida que el input sea correcto (A + B -)
    def arithmetic_expression(expression):
        # Examples:
        stack_values = []  # ["A", "B"]
        stack_operators = []  # ["ADD"]
        stack_types = []  # ["INT", "FLT"]

        final_ops = []
        result_quadruple_id = 1
        print("stack_values: {}".format(stack_values))
        print("stack_operators: {}\n".format(stack_operators))

        for symbol in Quadruple.format_expression(expression):
            s_type = symbol.type
            s_name = symbol.name

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

            # is a parentheses
            elif s_type == "parentheses":
                if s_name == "OP":
                    stack_values.append(s_name)
                    stack_operators.append(s_name)

                elif s_name == "CP":
                    sub_stack_values = Quadruple.__sub_stack_from_parentheses(
                        stack_values
                    )
                    sub_stack_operators = Quadruple.__sub_stack_from_parentheses(
                        stack_operators
                    )

                    # case when there is just one value inside parenthesis example: A + (B)
                    if len(sub_stack_operators) == 0:
                        stack_values.pop(-2)
                        stack_operators.pop()

                    else:

                        print("START OF CLOSE PARENTHESIS")

                        while len(sub_stack_operators) > 1:
                            Quadruple.__generate_quadruple(
                                sub_stack_values,
                                sub_stack_operators,
                                result_quadruple_id,
                                final_ops,
                            )
                            result_quadruple_id += 1

                        stack_operators.pop()
                        stack_values.pop(-2)

                        print("stack_operators: {}".format(stack_operators))
                        print("stack_values: {}".format(stack_values))

                        print("END OF CLOSE PARENTHESIS\n")

            # is an unknown character
            else:
                return "error: type {} not found".format(s_type)

            print("stack_values: {}".format(stack_values))
            print("stack_operators: {}\n".format(stack_operators))

        while len(stack_operators):
            Quadruple.__generate_quadruple(
                stack_values, stack_operators, result_quadruple_id, final_ops
            )
            result_quadruple_id += 1

            print("stack_values: {}".format(stack_values))
            print("stack_operators: {}\n".format(stack_operators))

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
                    "(": Symbol("OP", "parentheses"),
                    ")": Symbol("CP", "parentheses"),
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

expression = "(A + B) * (F / D)"
print("-------Expression: {}-------\n".format(expression))
result = Quadruple.arithmetic_expression(expression)

print("-----------------resultado final-----------------")
for i in result:
    print(i.format_quadruple())