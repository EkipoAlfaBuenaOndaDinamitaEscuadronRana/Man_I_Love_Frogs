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

    #               ==     !=      ||    &&
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

    def considerate(symbol_1, symbol_op, symbol_2):
        # When input is in string
        if [type(symbol_1), type(symbol_op), type(symbol_2)] == [str, str, str]:

            # Convert symbol into correct type
            if symbol_op in [
                "ADD",
                "SUB",
                "DIV",
                "MUL",
                "MOD",
                "ADDEQ",
                "SUBEQ",
                "DIVEQ",
                "MODEQ",
                "MODEQ",
            ]:
                symbol_op = "operation"
            elif symbol_op in ["LT", "GT", "LTE", "GTE"]:
                symbol_op = "comparison"
            elif symbol_op in ["BEQ", "BNEQ", "OR", "AND"]:
                symbol_op = "matching"
            elif symbol_op == "EQ":
                symbol_op = "assignment"

        # When input is in symbol
        else:
            symbol_1 = symbol_1.type
            symbol_2 = symbol_2.type
            symbol_op = symbol_op.type

        if not (symbol_1 in SemanticTable.types) or not (
            symbol_2 in SemanticTable.types
        ):
            return "error"

        elif symbol_op == "operation":
            return SemanticTable.__operations[symbol_1][symbol_2]

        elif symbol_op == "comparison":
            return SemanticTable.__comparison[symbol_1][symbol_2]

        elif symbol_op == "matching":
            return "BOOL"

        elif symbol_op == "assignment":
            return True

        else:
            return "error"
