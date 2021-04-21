class SemanticTable(object):
    """docstring for SemanticTable"""
    def __init__(self):
        self.types = { 'INT', 'FLOAT', 'CHAR', 'STRING', 'BOOL', 'NULL' }
        self.comparison_op = { '<', '>', '<=', '>=' }
        self.operations_op = { '+', '-', '+=', '-=', '*', '/', '%', '*=', '/=', '%=' }
        self.matching_op = { '==', '||', '&&' }

        self.operations = {
            'INT' : {
                'INT': 'INT',
                'FLOAT': 'FLOAT',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'error',
                'NULL': 'error'
            },

            'FLOAT': {
                'INT': 'FLOAT',
                'FLOAT': 'FLOAT',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'error',
                'NULL': 'error'
            },

            'CHAR': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'STRING',
                'STRING': 'STRING',
                'BOOL': 'error',
                'NULL': 'error'
            },

            'STRING': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'STRING',
                'STRING': 'STRING',
                'BOOL': 'error',
                'NULL': 'error'
            },

            'BOOL': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'BOOL',
                'NULL': 'error'
            },

            'NULL': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'error',
                'NULL': 'error'
            },
        }

        self.comparison = {
            'INT': {
                'INT': 'BOOL',
                'FLOAT': 'BOOL',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'BOOL',
                'NULL': 'error'
            },

            'FLOAT': {
                'INT': 'BOOL',
                'FLOAT': 'BOOL',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'BOOL',
                'NULL': 'BOOL'
            },

            'CHAR': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'BOOL',
                'STRING': 'BOOL',
                'BOOL': 'error',
                'NULL': 'error'
            },

            'STRING': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'BOOL',
                'STRING': 'BOOL',
                'BOOL': 'error',
                'NULL': 'error'
            },

            'BOOL': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'BOOL',
                'NULL': 'BOOL'
            },

            'NULL': {
                'INT': 'error',
                'FLOAT': 'error',
                'CHAR': 'error',
                'STRING': 'error',
                'BOOL': 'error',
                'NULL': 'error'
            }
        }

    def considerate(self, exp_1, op, exp_2):
        if not(exp_1 in self.types) or not(exp_2 in self.types):
            return 'error'

        elif op in self.operations_op:
            return self.operations[exp_1][exp_2]

        elif op in self.comparison_op:
            return self.comparison[exp_1][exp_2]

        elif op in self.matching_op: 
            return 'bool'

        else:
            return 'error'

s = SemanticTable()
print(s.considerate('INT', '||', 'INT'))
