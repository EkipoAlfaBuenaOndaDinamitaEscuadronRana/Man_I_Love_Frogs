from symbol_table import *
from cuadruple import *

class SemanticTable:
    #                    <     >     <=     >=
    __comparison_op = { 'LT', 'GT', 'LTE', 'GTE' }

    #                    +      -      +=       -=       *=     /=     %      *=       /=       %=
    __operations_op = { 'ADD', 'SUB', 'ADDEQ', 'SUBEQ', 'MUL', 'DIV', 'MOD', 'MULEQ', 'DIVEQ', 'MODEQ' }

    #                  ==     !=      ||    &&
    __matching_op = { 'BEQ', 'BNEQ', 'OR', 'AND' }

    __types = { 'INT', 'FLT', 'CHAR', 'STR', 'BOOL', 'NULL' }
    __operations = {
        'INT' : {
            'INT': 'INT',
            'FLT': 'FLT',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'error',
            'NULL': 'error'
        },

        'FLT': {
            'INT': 'FLT',
            'FLT': 'FLT',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'error',
            'NULL': 'error'
        },

        'CHAR': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'STR',
            'STR': 'STR',
            'BOOL': 'error',
            'NULL': 'error'
        },

        'STR': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'STR',
            'STR': 'STR',
            'BOOL': 'error',
            'NULL': 'error'
        },

        'BOOL': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'BOOL',
            'NULL': 'error'
        },

        'NULL': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'error',
            'NULL': 'error'
        },
    }

    __comparison = {
        'INT': {
            'INT': 'BOOL',
            'FLT': 'BOOL',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'BOOL',
            'NULL': 'error'
        },

        'FLT': {
            'INT': 'BOOL',
            'FLT': 'BOOL',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'BOOL',
            'NULL': 'BOOL'
        },

        'CHAR': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'BOOL',
            'STR': 'BOOL',
            'BOOL': 'error',
            'NULL': 'error'
        },

        'STR': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'BOOL',
            'STR': 'BOOL',
            'BOOL': 'error',
            'NULL': 'error'
        },

        'BOOL': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'BOOL',
            'NULL': 'BOOL'
        },

        'NULL': {
            'INT': 'error',
            'FLT': 'error',
            'CHAR': 'error',
            'STR': 'error',
            'BOOL': 'error',
            'NULL': 'error'
        }
    }

    def __another_op_mdr_in_stack(stack_operands):
        any(item in ['MUL', 'DIV', 'MOD'] for item in stack_operands)

    def __another_op_as_in_stack(stack_operands):
        any(item in ['ADD', 'SUB'] for item in stack_operands)

    def __generate_quadruple(stack_operands, stack_operators, result_cuadruple_id, final_ops):
        result_id = "T" + str(result_cuadruple_id)
        
        q = Cuadruple(stack_operators.pop(), stack_operands[-2], stack_operands[-1], result_id)
        final_ops.append(q)

        del stack_operands[-2:]

        stack_operands.append(result_id)
        return result_cuadruple_id + 1

    def considerate(symbol_1, symbol_op, symbol_2):
        if not(symbol_1.type in SemanticTable.__types) or not(symbol_2.type in SemanticTable.__types):
            return 'error'

        elif symbol_op.type == 'operation':
            return SemanticTable.__operations[symbol_1.type][symbol_2.type]

        elif symbol_op.type == 'comparison':
            return SemanticTable.__comparison[symbol_1.type][symbol_2.type]

        elif symbol_op.type == 'matching': 
            return 'BOOL'

        else:
            return 'error'

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
        result_cuadruple_id = 1

        for symbol in expression:

            s_type = symbol.type
            s_name = symbol.name

            # is a constant or an ID
            if s_type in SemanticTable.__types:
                stack_operands.append(symbol.name)
                stack_types.append(symbol.type)

            # is an operator
            elif s_type in ['operation', 'comparison', 'matching']:

                # Multiplication and division case
                if s_name in ['MUL', 'DIV']:

                    if SemanticTable.__another_op_mdr_in_stack(stack_operands):
                        result_cuadruple_id = SemanticTable.__generate_quadruple(stack_operands, stack_operators, result_cuadruple_id, final_ops)

                # Addition and substraction case
                elif s_name in ['ADD', 'SUB']:

                    # There is another multiplication  
                    if SemanticTable.__another_op_mdr_in_stack(stack_operands) or \
                       SemanticTable.__another_op_as_in_stack(stack_operands):
                        result_cuadruple_id = SemanticTable.__generate_quadruple(stack_operands, stack_operators, result_cuadruple_id, final_ops)

                        if SemanticTable.__another_op_as_in_stack(stack_operands):
                            result_cuadruple_id = SemanticTable.__generate_quadruple(stack_operands, stack_operators, result_cuadruple_id, final_ops)

                stack_operators.append(s_name)

            # is a parenthesis
            elif s_type == "parentheses":
                pass

            # is an unknown character
            else:
                return "error: type {} not found".format(symbol.type)

        while len(stack_operators):
            result_cuadruple_id = SemanticTable.__generate_quadruple(stack_operands, stack_operators, result_cuadruple_id, final_ops)

        return final_ops

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

test = SemanticTable.arithmetic_expression(expression)

for i in test:
    print(i.format_cuadruple())


print()
print()
print()
print()
print(test[0].operator)