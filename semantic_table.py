class SemanticTable:
    __types = { 'INT', 'FLOAT', 'CHAR', 'STRING', 'BOOL', 'NULL' }
    __comparison_op = { '<', '>', '<=', '>=' }
    __operations_op = { '+', '-', '+=', '-=', '*', '/', '%', '*=', '/=', '%=' }
    __matching_op = { '==', '||', '&&' }

    __operations = {
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

    __comparison = {
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
