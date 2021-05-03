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

    def __sub_stack_from_parentheses(stack):
        if "(" in stack:
            stack.reverse()
            index = stack.index("(")
            sub_stack = stack[:index]
            stack.reverse()

            return sub_stack

        return stack

    def __another_op_mdr_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        print("<<<<<<<<<<<__another_op_mdr_in_stack>>>>>>>>>>")
        print("sub_stack_operators: ", sub_stack_operators)
        print("<<<<<<<<<<<__another_op_mdr_in_stack>>>>>>>>>>\n")
        return any(item in ["MUL", "DIV", "MOD"] for item in sub_stack_operators)

    def __another_op_as_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        print("<<<<<<<<<<<__another_op_as_in_stack>>>>>>>>>>")
        print("sub_stack_operators: ", sub_stack_operators)
        print("<<<<<<<<<<<__another_op_mdr_in_stack>>>>>>>>>>\n")
        return any(item in ["ADD", "SUB"] for item in sub_stack_operators)

    def __generate_quadruple(
        stack_values, stack_operators, result_quadruple_id, final_ops
    ):
        print("--------start: __generate_quadruple--------")
        print("stack_operators: {}".format(stack_operators))
        print("stack_values: {}".format(stack_values))
        result_id = "T" + str(result_quadruple_id)

        q = Quadruple(
            stack_operators.pop(), stack_values[-2], stack_values[-1], result_id
        )

        del stack_values[-2:]

        print("-------------__generate_quadruple--------")
        print("stack_operators: {}".format(stack_operators))
        print("stack_values: {}".format(stack_values))
        print("--------end: __generate_quadruple--------\n")

        final_ops.append(q)
        stack_values.append(result_id)

    # TODO: Todavía no considera tipos basados en la tabla semantica
    # TODO: Todavía no considera tipos de comparison o matching
    # TODO: No considera constantes (1, 1.5, "algo asi")
    # TODO: No valida que el input sea correcto (A + B -)
    def arithmetic_expression(expression):
        # Examples:
        stack_values = []  # ["A", "B"]
        stack_operators = []  # ["ADD"]
        stack_types = []  # ["INT", "FLT"]

        final_ops = []
        result_quadruple_id = 1
        print("stack_operators: {}".format(stack_operators))
        print("stack_values: {}\n".format(stack_values))

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
                        print("============START OF CLOSE PARENTHESIS============\n")

                        while stack_operators[-1] != "(":
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                final_ops,
                            )

                            print("stack_operators: ", stack_operators)
                            print("stack_values: ", stack_values, "\n")

                            result_quadruple_id += 1

                        stack_operators.pop()
                        stack_values.pop(-2)
                        print("=============END OF CLOSE PARENTHESIS=============\n")

            # is an unknown character
            else:
                return "error: type {} not found".format(s_type)

            print("stack_operators: {}".format(stack_operators))
            print("stack_values: {}\n".format(stack_values))

        while len(stack_operators):
            Quadruple.__generate_quadruple(
                stack_values, stack_operators, result_quadruple_id, final_ops
            )
            result_quadruple_id += 1

            print("stack_operators: {}".format(stack_operators))
            print("stack_values: {}\n".format(stack_values))

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

# expression = "(A + B * C) + C * (D + E)"                  # PASS
# expression = "(D / (E * F + G))"                          # PASS
# expression = "C * (D / (E + F))"                          # PASS
# expression = "(E / F + G / H)"                            # PASS
# expression = "(A * (E / F + G / H) + I)"                  # PASS
# expression = "(C * (E / F + G * H))"                      # PASS
expression = "(A / (C * (E / F + G * (H / I + J - K - (L * M * N)))))"                # PASS

result = Quadruple.arithmetic_expression(expression)

print("------Expression: {}------".format(expression))
print("-----------------resultado final-----------------")
for i in result:
    print(i.format_quadruple())