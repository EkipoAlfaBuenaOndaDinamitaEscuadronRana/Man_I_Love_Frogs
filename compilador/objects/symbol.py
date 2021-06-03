from router_solver import *
import compilador.helpers.printer
from compilador.helpers.printer import *
import numpy as np
import symbol

# CLASE SYMBOL
# Objeto que guarda los datos de un token


####################### GLOBALS #######################

# Diccoionario de para consistencia de tipos de datos
type_dictionary = {
    "int": "INT",
    "float": "FLT",
    "char": "CHAR",
    "bool": "BOOL",
    "null": "NULL",
    "string": "STR",
    "void": "VOID",
    "frog": "FROG",
    "INT": "INT",
    "FLT": "FLT",
    "CHAR": "CHAR",
    "BOOL": "BOOL",
    "NULL": "NULL",
    "STR": "STR",
    "VOID": "VOID",
    "FROG": "FROG",
    "operation": "operation",
    "parentheses": "parentheses",
    "not": "not",
    "assignment": "assignment",
    "comparison": "comparison",
    "matching": "matching",
    "assignment_operation": "assignment_operation",
    "read": "read",
    "write": "write",
    "obj_method": "obj_method",
    "instruction": "instruction",
    "address": "address",
}
# Diccionario de compatibilidad de tipos de datos
type_translation = {
    "INT": ["INT", "NULL", "read"],
    "FLT": ["INT", "FLT", "NULL", "read"],
    "CHAR": ["CHAR", "NULL", "read"],
    "BOOL": ["INT", "FLT", "BOOL", "NULL", "read"],
    "NULL": ["NULL"],
    "STR": ["STR", "CHAR", "NULL", "read"],
    "FROG": ["FROG", "NULL"],
}


class Symbol(object):

    ####################### INITS #######################

    def __init__(
        self,
        name=None,
        type=None,
        scope=None,
        return_location=[],
        dimension_sizes=[],
        address=[],
        address_flag=None,
        object_atr_flag=None,
    ):
        self.name = name  # Nombre de simbolo
        self.type = (
            type_dictionary[type] if type in type_dictionary else None
        )  # Tipo de simbolo
        self.scope = scope  # Contexto de simbolo
        self.dimension_sizes = dimension_sizes  # Tamaño de simbolo dimensionado
        self.dimension_nodes = {}  # Nodos de dimensiones
        self.return_location = (
            return_location  # Stack de temporales con valor de retorno
        )
        self.address = address  # Direcciones de memoria en tabla de variables
        self.segment_direction = None  # Dirección en segmento
        self.global_direction = None  # Dirección global
        self.value = None  # Valor
        self.address_flag = address_flag  # Guarda el tipo de la dirección que guarda
        self.object_atr_flag = object_atr_flag  # Guarda el simbolo de su objeto padre

    # Operador == entre dos simbolos
    def __eq__(self, other):
        if type(self) is Symbol and type(other) is Symbol:
            self_data = [
                self.name,
                self.type,
                self.dimension_sizes,
                self.segment_direction,
                self.global_direction,
                self.value,
                self.scope,
            ]

            other_data = [
                other.name,
                other.type,
                other.dimension_sizes,
                other.segment_direction,
                other.global_direction,
                other.value,
                other.scope,
            ]

            return self_data == other_data

        elif self is None and other is None:
            return True

        else:
            return False

    # Valor unico de simbolo
    def __hash__(self):
        return id(self)

    ####################### SETS #######################

    # Guarda una dirección considerando lo que ya se guardo en la tabla
    def set_address(self, offset):
        self.address = []
        self.address.append(offset)
        if type(self.dimension_sizes) == int or len(self.dimension_sizes) > 0:
            self.address.append(offset + self.dimension_sizes)
            return offset + self.dimension_sizes + 1
        else:
            self.address.append(offset)
            return offset + 1

    # Guarda el contexto en el que se usa el simbolo
    def set_scope(self, scope):
        self.scope = scope

    # Guarda el temporal al que se le asigno el valor de retorno de una función
    def set_return_location(self, loc):
        self.return_location.append(loc)

    # Guarda los parametros que se le enviaron a la variable en declaración
    def set_dimension_sizes(self, d_sizes):
        if type(d_sizes) == list:
            self.dimension_sizes = d_sizes

    # Crea los nodos de dimensiones del arreglo
    def create_dimension_nodes(self):
        DIM = 1
        R = 1
        for d in self.dimension_sizes:
            node = {}
            node["LI"] = 0
            node["LS"] = d - 1
            R = (node["LS"] - node["LI"] + 1) * R
            self.dimension_nodes[DIM] = node
            DIM += 1
        Offset = 0
        self.dimension_sizes = R
        for k, v in self.dimension_nodes.items():
            m = R / (v["LS"] - v["LI"] + 1)
            v["M"] = m
            R = m
            Offset = Offset + v["LI"] * m
        self.dimension_nodes[DIM - 1]["M"] = Offset

    ####################### GETS #######################

    # Regresa el nombre de el simbolo
    def get_name(self):
        return self.name

    # Regresa el numero de dimensiones del arreglo
    def get_dimension_size(self):
        return list(self.dimension_nodes.keys())[-1]

    # Regresa el tamaño real del objeto en memoria
    def get_dimension_sizes(self):
        return self.dimension_sizes

    # Regresa el temporal donde esta guardado el valor de retorno
    def get_return_location(self):
        if len(self.return_location) > 0:
            return self.return_location.pop()
        else:
            return None

    ####################### VALIDATIONS #######################

    # Indica si una variable es dimensionada
    def is_dimensioned(self):
        if type(self.dimension_sizes) == list:
            return len(self.dimension_sizes) > 0
        else:
            return self.dimension_sizes > 0

    # Indica si los tipos de los simbolos son compatibles
    def check_type_compatibility(type_recipient, type_sender):
        return type_sender in type_translation[type_recipient]

    ####################### PRINTS #######################

    # Imprime los datos de un simbolo
    def print_symbol(self):
        if self.name:
            print("VAR:", self.name)

        if self.type:
            print("TYPE:", self.type)

        if self.name in ["arr", "mat"]:
            print("dimension_sizes", self.dimension_sizes)

        if self.segment_direction != None and self.global_direction != None:
            print("SEGMENT_DIRECTION:", self.segment_direction)
            print("GLOBAL_DIRECTION:", self.global_direction)

        if self.scope:
            print("SCOPE:", self.scope)

        if self.value:
            print("VALUE: ", self.value)

    # Calcula el tamaño real del simbolo en memoria
    def memory_size(self):
        return int(np.prod(self.dimension_sizes))
