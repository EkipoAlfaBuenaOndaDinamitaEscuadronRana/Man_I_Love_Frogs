import compilador.helpers.printer
from compilador.helpers.printer import *
import numpy as np
import symbol

type_dictionary = {
    "int": "INT",
    "float": "FLT",
    "char": "CHAR",
    "bool": "BOOL",
    "null": "NULL",
    "string": "STR",
    "void": "VOID",
    "INT": "INT",
    "FLT": "FLT",
    "CHAR": "CHAR",
    "BOOL": "BOOL",
    "NULL": "NULL",
    "STR": "STR",
    "VOID": "VOID",
    "operation": "operation",
    "parentheses": "parentheses",
    "not": "not",
    "assignment": "assignment",
    "comparison": "comparison",
    "matching": "matching",
    "assignment_operation": "assignment_operation",
    "read": "read",
    "write": "write",
}

memory_sizes = {
    "INT": 4,
    "FLT": 4,
    "CHAR": 1,
    "STR": 1,
    "BOOL": 1,
    "NULL": 1,
}

type_translation = {
    "INT": ["INT", "NULL", "read"],
    "FLT": ["INT", "FLT", "NULL", "read"],
    "CHAR": ["CHAR", "NULL", "read"],
    "BOOL": ["INT", "FLT", "BOOL", "NULL", "read"],
    "NULL": ["NULL"],
    "STR": ["STR", "CHAR", "NULL", "read"],
}


class Symbol(object):
    """docstring for Symbol
    A symbol represents a memory space, for example:
        int A;

    It would be represented like this
        Symbol("A", "INT")

    To represent non-scalar values as vectors or arrays, such as the following:
        float arr[5];
        float mat[3][10];

    You need to send the size of the dimensions in your parameters as follows:
        Symbol("arr", "FLT", [5])
        Symbol("mat", "FLT", [3, 10])

    It is also possible to specify a memory address.
    However, this value is expected to be assigned by the virtual machine.
    """

    def __init__(self, name=None, type=None, dimension_sizes=[], direction=None):
        self.name = name
        self.type = type_dictionary[type] if type in type_dictionary else None
        self.dimension_sizes = dimension_sizes
        self.dimensions = len(dimension_sizes)
        self.direction = direction

    def __eq__(self, other):
        if type(self) is Symbol and type(other) is Symbol:
            return self.name == other.name and self.type == other.type
        elif self is None and other is None:
            return True
        else:
            return False

    def __hash__(self):
        return id(self)

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.type = type_dictionary[type] if type in type_dictionary else None

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def check_type_compatibility(type_recipient, type_sender):
        return type_sender in type_translation[type_recipient]

    def print_symbol(self):
        if self.name:
            print("VAR: ", self.name)

        if self.type:
            print("TYPE: ", self.type)

        if len(self.dimension_sizes):
            print("DIMENSIONS: ", self.dimensions)
            print("DIMENSION_SIZES: ", self.dimension_sizes)

        if self.direction:
            print("DIRECTION: ", self.direction)

    def memory_size(self):
        if self.dimensions:
            return memory_sizes[self.type] * (np.prod(self.dimension_sizes))

        return memory_sizes[self.type]
