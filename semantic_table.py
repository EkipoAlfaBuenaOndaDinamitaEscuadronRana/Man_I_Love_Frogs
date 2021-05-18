from symbol_tables import *


class SemanticTable:
    types = {"INT", "FLT", "CHAR", "STR", "BOOL", "NULL"}

    #                  <     >     <=     >=
    comparison_op = {"LT", "GT", "LTE", "GTE"}

    __operations_op = {
        "ADD",  # +
        "SUB",  # -
        "MUL",  # *
        "DIV",  # /
        "MOD",  # %
    }

    __assignment_operations_op = {
        "ADDEQ",  # +=
        "SUBEQ",  # -=
        "MULEQ",  # *=
        "DIVEQ",  # /=
        "MODEQ",  # %=
    }

    #                ==     !=      ||    &&
    matching_op = {"BEQ", "BNEQ", "OR", "AND"}

    __operations = {
        "INT": {
            "INT": "INT",
            "FLT": "FLT",
            "CHAR": "INT",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
        "FLT": {
            "INT": "FLT",
            "FLT": "FLT",
            "CHAR": "FLT",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
        "CHAR": {
            "INT": "INT",
            "FLT": "FLT",
            "CHAR": "STR",
            "STR": "STR",
            "BOOL": "error",
            "NULL": "error",
        },
        "STR": {
            "INT": "error",
            "FLT": "error",
            "CHAR": "STR",
            "STR": "STR",
            "BOOL": "error",
            "NULL": "error",
        },
        "BOOL": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "error",
            "STR": "error",
            "BOOL": "BOOL",
            "NULL": "error",
        },
        "NULL": {
            "INT": "error",
            "FLT": "error",
            "CHAR": "error",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
    }

    __comparison = {
        "INT": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "BOOL",
            "STR": "error",
            "BOOL": "BOOL",
            "NULL": "error",
        },
        "FLT": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "BOOL",
            "STR": "error",
            "BOOL": "BOOL",
            "NULL": "error",
        },
        "CHAR": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "BOOL",
            "STR": "BOOL",
            "BOOL": "error",
            "NULL": "error",
        },
        "STR": {
            "INT": "error",
            "FLT": "error",
            "CHAR": "BOOL",
            "STR": "BOOL",
            "BOOL": "error",
            "NULL": "error",
        },
        "BOOL": {
            "INT": "error",
            "FLT": "error",
            "CHAR": "error",
            "STR": "error",
            "BOOL": "BOOL",
            "NULL": "BOOL",
        },
        "NULL": {
            "INT": "error",
            "FLT": "error",
            "CHAR": "error",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
    }

    __assignment_operations = {
        "INT": {
            "INT": "INT",
            "FLT": "FLT",
            "CHAR": "INT",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
        "FLT": {
            "INT": "FLT",
            "FLT": "FLT",
            "CHAR": "FLT",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
        "CHAR": {
            "INT": "CHAR",
            "FLT": "error",
            "CHAR": "error",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
        "STR": {
            "INT": "error",
            "FLT": "error",
            "CHAR": "STR",
            "STR": "STR",
            "BOOL": "error",
            "NULL": "error",
        },
        "BOOL": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "error",
            "STR": "error",
            "BOOL": "BOOL",
            "NULL": "error",
        },
        "NULL": {
            "INT": "error",
            "FLT": "error",
            "CHAR": "error",
            "STR": "error",
            "BOOL": "error",
            "NULL": "error",
        },
    }

    def clasify_symbol_op(symbol_op):
        if symbol_op in SemanticTable.__operations_op:
            return "operation"

        elif symbol_op in SemanticTable.__assignment_operations_op:
            return "assignment_operation"

        elif symbol_op in SemanticTable.comparison_op:
            return "comparison"

        elif symbol_op in SemanticTable.matching_op:
            return "matching"

        elif symbol_op == "EQ":
            return "assignment"

    def considerate(symbol_1, symbol_op, symbol_2):
        # When input is in string
        if [type(symbol_1), type(symbol_op), type(symbol_2)] == [str, str, str]:

            # Convert symbol into correct type
            symbol_op = SemanticTable.clasify_symbol_op(symbol_op)

        # When input is in symbol
        else:
            symbol_1 = symbol_1.type
            symbol_2 = symbol_2.type
            symbol_op = symbol_op.type

        if symbol_1 not in SemanticTable.types or symbol_2 not in SemanticTable.types:
            return "error"

        elif symbol_op == "operation":
            return SemanticTable.__operations[symbol_1][symbol_2]

        elif symbol_op == "comparison":
            return SemanticTable.__comparison[symbol_1][symbol_2]

        elif symbol_op == "assignment_operation":
            return SemanticTable.__assignment_operations[symbol_1][symbol_2]

        elif symbol_op == "matching":
            return "BOOL"

        elif symbol_op == "assignment":
            return symbol_1 if symbol_1 == symbol_2 else "error"

        else:
            return "error"
