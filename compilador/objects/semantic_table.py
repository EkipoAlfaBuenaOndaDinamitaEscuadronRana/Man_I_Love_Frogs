from router_solver import *
import compilador.objects.function_table
from compilador.objects.function_table import *


# CLASE SEMANTIC TABLE
# Guarda y valida relación entre operandos usando operadores


class SemanticTable:
    ####################### INITS #######################

    # Tipos validos para hacer operaciones
    types = {"INT", "FLT", "CHAR", "STR", "BOOL", "NULL", "FROG"}

    # Operadores de comparación
    #                 <     >     <=     >=
    comparison_op = {"LT", "GT", "LTE", "GTE"}

    # Operadores de igualdad
    #               ==     !=      ||    &&
    matching_op = {"BEQ", "BNEQ", "OR", "AND"}

    # Operadores aritmeticos
    operations_op = {
        "ADD",  # +
        "SUB",  # -
        "MUL",  # *
        "DIV",  # /
        "MOD",  # %
    }

    # Operadores de asignación compuesta
    assignment_operations_op = {
        "ADDEQ",  # +=
        "SUBEQ",  # -=
        "MULEQ",  # *=
        "DIVEQ",  # /=
        "MODEQ",  # %=
    }

    # Diccionario que indica el resultado de una operación aritmetica entre dos tipos
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

    # Diccionario que indica el resultado de una operación de comparación entre dos tipos
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

    # Diccionario que indica el resultado de una operación de asignación compuesta entre dos tipos
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

    # Si llega un operador como string valida su tipo
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

    # Regresa resultado de consideración semantica entre dos operandos y un operador
    def considerate(symbol_1, symbol_op, symbol_2):
        # When input is in string
        if [type(symbol_1), type(symbol_op), type(symbol_2)] == [str, str, str]:
            # Convert symbol into correct type
            symbol_op = SemanticTable.clasify_symbol_op(symbol_op)
        # When input is in symbol
        else:

            if symbol_1.address_flag:
                symbol_1 = symbol_1.address_flag
            else:
                symbol_1 = symbol_1.type

            if symbol_2.address_flag:
                symbol_2 = symbol_2.address_flag
            else:
                symbol_2 = symbol_2.type

            symbol_op = symbol_op.type

        # Valida que lo que llego es un tipo válido para operaciones
        if symbol_1 not in SemanticTable.types or symbol_2 not in SemanticTable.types:
            return "ERROR"

        # Regresa el valor resultante de una operación aritmetica entre tipos
        elif symbol_op == "operation":
            return SemanticTable.__operations[symbol_1][symbol_2]

        # Regresa el valor resultante de una operación de comparación entre tipos
        elif symbol_op == "comparison":
            return SemanticTable.__comparison[symbol_1][symbol_2]

        # Regresa el valor resultante de una operación de asignación compuesta entre tipos
        elif symbol_op == "assignment_operation":
            return SemanticTable.__assignment_operations[symbol_1][symbol_2]

        # Regresa un valor booleano cuando se hace una operación de igualdad
        elif symbol_op == "matching":
            return "BOOL"

        # Regresa el tipo resultante de una asignación y valida compatibilidad de tipos
        elif symbol_op == "assignment":
            return (
                symbol_2
                if Symbol.check_type_compatibility(symbol_1, symbol_2)
                else "ERROR"
            )

        else:
            return "ERROR"
