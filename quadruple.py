from semantic_table import *

class Quadruple(object):
    def __init__(self, operator, operand_1, operand_2, result_id):
        self.operator = operator
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.result_id = result_id

    def __another_op_mdr_in_stack(stack_operators):
        return any(item in ['MUL', 'DIV', 'MOD'] for item in stack_operators)

    def __another_op_as_in_stack(stack_operators):
        return any(item in ['ADD', 'SUB'] for item in stack_operators)

    def __generate_quadruple(stack_operands, stack_operators, result_quadruple_id, final_ops):
        result_id = "T" + str(result_quadruple_id)

        q = Quadruple(stack_operators.pop(), stack_operands[-2], stack_operands[-1], result_id)
        final_ops.append(q)

        del stack_operands[-2:]

        stack_operands.append(result_id)

    '''
    A list of Symbols must be provided
    example = [Symbol("A", "INT"), Symbol("ADD", "operation"), Symbol("B", "FLT")]
    '''
    def arithmetic_expression(expression):
                                # Examples:
        stack_operands = []     # ["A", "B"]
        stack_operators = []    # ["ADD"]
        stack_types = []        # ["INT", "FLT"]

        final_ops = []
        result_quadruple_id = 1

        # TODO: Todavía no considera tipos basados en la tabla semantica
        # for symbol in format_expression(expression):
        for symbol in expression:

            s_type = symbol.type # operation
            s_name = symbol.name # +

            # is an operand
            if s_type in SemanticTable.types:
                stack_operands.append(s_name)
                stack_types.append(s_type)

            # is an operator
            elif s_type in ['operation', 'comparison', 'matching']:

                if s_name in ['MUL', 'DIV', 'MOD']:

                    # There is another operator of multiplication, division or residue
                    if Quadruple.__another_op_mdr_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(stack_operands, stack_operators, result_quadruple_id, final_ops)
                        result_quadruple_id += 1

                # Addition and substraction case
                elif s_name in ['ADD', 'SUB']:

                    # There is another operator on the stack
                    if Quadruple.__another_op_mdr_in_stack(stack_operators) or \
                       Quadruple.__another_op_as_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(stack_operands, stack_operators, result_quadruple_id, final_ops)
                        result_quadruple_id += 1

                        # There is another operator of sum or addition
                        if Quadruple.__another_op_as_in_stack(stack_operators):
                            Quadruple.__generate_quadruple(stack_operands, stack_operators, result_quadruple_id, final_ops)
                            result_quadruple_id += 1

                stack_operators.append(s_name)

            # is a parenthesis
            # TODO: Esto sera resuelto en otro issue
            elif s_type == "parentheses":
                pass

            # is an unknown character
            else:
                return "error: type {} not found".format(s_type)

        while len(stack_operators):
            Quadruple.__generate_quadruple(stack_operands, stack_operators, result_quadruple_id, final_ops)
            result_quadruple_id += 1

        return final_ops

    def format_quadruple(self):
        return "{} {} {} {}".format(self.operator, self.operand_1, self.operand_2, self.result_id)

    def format_expression(expression):
        response = []

        if type(expression) == str:
            expression = expression.replace(" ", "")
            expression = [char for char in expression]

        for symbol in expression:

            s_type = type(symbol)

            if s_type == Symbol:
                continue

            if s_type == str:

                switcher = {
                    "+" : Symbol("ADD", "operation"),
                    "-" : Symbol("SUB", "operation"),
                    "*" : Symbol("MUL", "operation"),
                    "/" : Symbol("DIV", "operation"),
                    "%" : Symbol("MOD", "operation"),
                    "<" : Symbol("LT", "comparison"),
                    ">" : Symbol("gT", "comparison"),
                    "<=" : Symbol("LTE", "comparison"),
                    ">=" : Symbol("GTE", "comparison"),
                    "==" : Symbol("BEQ", "matching"),
                    "!=" : Symbol("BNEQ", "matching"),
                    "||" : Symbol("OR", "matching"),
                    "&&" : Symbol("AND", "matching")
                }

                response.append(switcher.get(symbol, Symbol(symbol, "FLT")))

        return response