from symbol_table import *

class SemanticTable:
    __types = { 'INT', 'FLT', 'CHAR', 'STR', 'BOOL', 'NULL' }
    __comparison_op = { 'LT', 'GT', 'LTE', 'GTE' }
    __operations_op = { 'ADD', 'SUB', 'ADDEQ', 'SUBEQ', 'MUL', 'DIV', 'MOD', 'MULEQ', 'DIVEQ', 'MODEQ' }
    __matching_op = { 'BIN_EQ', 'BIN_NOT_EQ', 'OR', 'AND' }

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

    def considerate(exp_1, op, exp_2):
        if not(exp_1 in SemanticTable.__types) or not(exp_2 in SemanticTable.__types):
            return 'error'

        elif op in SemanticTable.__operations_op:
            return SemanticTable.__operations[exp_1][exp_2]

        elif op in SemanticTable.__comparison_op:
            return SemanticTable.__comparison[exp_1][exp_2]

        elif op in SemanticTable.__matching_op: 
            return 'BOOL'

        else:
            return 'error'

    def arithmetic_expression(expression):
        poper = []
        stack_values = []
        stack_types = []
        final_ops = []

        # i     i   f   i   f    i    f   i   f
        # A * ( B + C * D - E) > B + (C * D - E)

        for symbol in expression:
            if type(symbol) == Symbol:
                stack_values.append(symbol)
            elif type(symbol) == str:
                poper.append(symbol)
            else:
                return "No baila mi hija con el señor"

        return final_ops
