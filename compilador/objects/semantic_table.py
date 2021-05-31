from router_solver import *
import compilador.objects.function_table
from compilador.objects.function_table import *


class SemanticTable:
    types = {"INT", "FLT", "CHAR", "STR", "BOOL", "NULL"}

    #                 <     >     <=     >=
    comparison_op = {"LT", "GT", "LTE", "GTE"}

    #               ==     !=      ||    &&
    matching_op = {"BEQ", "BNEQ", "OR", "AND"}

    operations_op = {
        "ADD",  # +
        "SUB",  # -
        "MUL",  # *
        "DIV",  # /
        "MOD",  # %
    }

    assignment_operations_op = {
        "ADDEQ",  # +=
        "SUBEQ",  # -=
        "MULEQ",  # *=
        "DIVEQ",  # /=
        "MODEQ",  # %=
    }

    __operations = {
        "INT": {
            "INT": "INT",
            "FLT": "FLT",
            "CHAR": "INT",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "FLT": {
            "INT": "FLT",
            "FLT": "FLT",
            "CHAR": "FLT",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "CHAR": {
            "INT": "INT",
            "FLT": "FLT",
            "CHAR": "STR",
            "STR": "STR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "STR": {
            "INT": "ERROR",
            "FLT": "ERROR",
            "CHAR": "STR",
            "STR": "STR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "BOOL": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "ERROR",
            "STR": "ERROR",
            "BOOL": "BOOL",
            "NULL": "ERROR",
        },
        "NULL": {
            "INT": "ERROR",
            "FLT": "ERROR",
            "CHAR": "ERROR",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
    }

    __comparison = {
        "INT": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "BOOL",
            "STR": "ERROR",
            "BOOL": "BOOL",
            "NULL": "ERROR",
        },
        "FLT": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "BOOL",
            "STR": "ERROR",
            "BOOL": "BOOL",
            "NULL": "ERROR",
        },
        "CHAR": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "BOOL",
            "STR": "BOOL",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "STR": {
            "INT": "ERROR",
            "FLT": "ERROR",
            "CHAR": "BOOL",
            "STR": "BOOL",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "BOOL": {
            "INT": "ERROR",
            "FLT": "ERROR",
            "CHAR": "ERROR",
            "STR": "ERROR",
            "BOOL": "BOOL",
            "NULL": "BOOL",
        },
        "NULL": {
            "INT": "ERROR",
            "FLT": "ERROR",
            "CHAR": "ERROR",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
    }

    __assignment_operations = {
        "INT": {
            "INT": "INT",
            "FLT": "FLT",
            "CHAR": "INT",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "FLT": {
            "INT": "FLT",
            "FLT": "FLT",
            "CHAR": "FLT",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "CHAR": {
            "INT": "CHAR",
            "FLT": "ERROR",
            "CHAR": "ERROR",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "STR": {
            "INT": "ERROR",
            "FLT": "ERROR",
            "CHAR": "STR",
            "STR": "STR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
        "BOOL": {
            "INT": "BOOL",
            "FLT": "BOOL",
            "CHAR": "ERROR",
            "STR": "ERROR",
            "BOOL": "BOOL",
            "NULL": "ERROR",
        },
        "NULL": {
            "INT": "ERROR",
            "FLT": "ERROR",
            "CHAR": "ERROR",
            "STR": "ERROR",
            "BOOL": "ERROR",
            "NULL": "ERROR",
        },
    }

    def clasify_symbol_op(symbol_op):
        if symbol_op in SemanticTable.operations_op:
            return "operation"

        elif symbol_op in SemanticTable.assignment_operations_op:
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
            return "ERROR"

        elif symbol_op == "operation":
            return SemanticTable.__operations[symbol_1][symbol_2]

        elif symbol_op == "comparison":
            return SemanticTable.__comparison[symbol_1][symbol_2]

        elif symbol_op == "assignment_operation":
            return SemanticTable.__assignment_operations[symbol_1][symbol_2]

        elif symbol_op == "matching":
            return "BOOL"

        elif symbol_op == "assignment":
            return (
                symbol_2
                if Symbol.check_type_compatibility(symbol_1, symbol_2)
                else "ERROR"
            )

        else:
            return "ERROR"
