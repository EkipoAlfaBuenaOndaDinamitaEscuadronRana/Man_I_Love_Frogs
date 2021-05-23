from router_solver import *
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
    "address" : "address"
}

# NOTE: This sizes are no longer used... But I don't want to delete them yet...
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
    "FROG": ["NULL"],
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

    def __init__(self, name=None, type=None, scope= None, address=[], dimension_sizes=[]):
        self.name = name
        self.type = type_dictionary[type] if type in type_dictionary else None
        self.scope = scope
        self.dimension_sizes = dimension_sizes
        self.dimensions = len(dimension_sizes)
        self.address = address

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
    
    def set_scope(self, scope):
        self.scope = scope

    def set_type(self, type):
        self.type = type_dictionary[type] if type in type_dictionary else None
    
    def set_address(self, address):
        self.address.append(address)

    def get_name(self):
        return self.name

    def get_address(self):
        print(self.address)
        if len(self.address) > 0:
            return self.address.pop()
        else:
            return None

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

        if self.address:
            print("ADDRESS: ", self.address)

    def memory_size(self):
        return int(np.prod(self.dimension_sizes))
