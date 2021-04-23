from symbol_table import *
from cuadruple import *

class SemanticTable:
    __types = { 'INT', 'FLT', 'CHAR', 'STR', 'BOOL', 'NULL' }
    __comparison_op = { 'LT', 'GT', 'LTE', 'GTE' }
    __operations_op = { 'ADD', 'SUB', 'ADDEQ', 'SUBEQ', 'MUL', 'DIV', 'MOD', 'MULEQ', 'DIVEQ', 'MODEQ' }
    __matching_op = { 'BEQ', 'BNEQ', 'OR', 'AND' }

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
            if symbol.type in SemanticTable.__types:
                stack_operands.append(symbol.name)
                stack_types.append(symbol.type)
            elif symbol.type in ['operation', 'comparison', 'matching']:
                stack_operators.append(symbol.name)
            else:
                return "error: type {} not found".format(symbol.type)

        for operand in stack_operators:
            if len(final_ops) == 0:
                final_ops.append(Cuadruple(operand, stack_operands.pop(), stack_operands.pop(), "T" + str(result_cuadruple_id)))
            else:
                final_ops.append(Cuadruple(operand, stack_operands.pop(), final_ops[len(final_ops) - 1].result_id, "T" + str(result_cuadruple_id)))

            result_cuadruple_id += 1

        return final_ops
