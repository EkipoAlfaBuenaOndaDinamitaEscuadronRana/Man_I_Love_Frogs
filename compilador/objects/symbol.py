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
    "address": "address",
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

    def __init__(
        self,
        name=None,
        type=None,
        scope=None,
        return_location=[],
        dimension_sizes=[],
        address=[],
    ):
        self.name = name
        self.type = type_dictionary[type] if type in type_dictionary else None
        self.scope = scope
        self.dimension_sizes = dimension_sizes
        self.dimension_nodes = {}
        self.dimensions = len(dimension_sizes)
        self.return_location = return_location
        self.address = address
        self.segment_direction = None
        self.global_direction = None
        self.value = None

    def __eq__(self, other):
        if type(self) is Symbol and type(other) is Symbol:
            self_data = [
                self.name,
                self.type,
                self.dimension_sizes,
                self.dimensions,
                self.segment_direction,
                self.global_direction,
                self.value,
                self.scope,
            ]

            other_data = [
                other.name,
                other.type,
                other.dimension_sizes,
                other.dimensions,
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

    def __hash__(self):
        return id(self)

    def set_name(self, name):
        self.name = name

    def is_dimensioned(self):
        if type(self.dimension_sizes) == list:
            return len(self.dimension_sizes) > 0
        else:
            return self.dimension_sizes > 0

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

    def get_dimension_size(self):
        return list(self.dimension_nodes.keys())[-1]

    def set_address(self, offset):
        self.address = []
        self.address.append(offset)
        if type(self.dimension_sizes) == int or len(self.dimension_sizes) > 0:
            self.address.append(offset + self.dimension_sizes)
            return offset + self.dimension_sizes + 1
        else:
            self.address.append(offset)
            return offset + 1

    def get_address(self):
        return self.address

    def get_dimension_nodes_len(self):
        return len(self.dimension_nodes)

    def set_dimension_sizes(self, d_sizes):
        if type(d_sizes) == list:
            self.dimension_sizes = d_sizes

    def get_dimension_sizes(self):
        return self.dimension_sizes

    def set_scope(self, scope):
        self.scope = scope

    def set_type(self, type):
        self.type = type_dictionary[type] if type in type_dictionary else None

    def set_return_location(self, loc):
        self.return_location.append(loc)

    def get_name(self):
        return self.name

    def get_return_location(self):
        if len(self.return_location) > 0:
            return self.return_location.pop()
        else:
            return None

    def get_type(self):
        return self.type

    def check_type_compatibility(type_recipient, type_sender):
        return type_sender in type_translation[type_recipient]

    def print_symbol(self):
        if self.name:
            print("VAR:", self.name)

        if self.type:
            print("TYPE:", self.type)

        if len(self.dimension_sizes):
            print("DIMENSIONS:", self.dimensions)
            print("DIMENSION_SIZES:", self.dimension_sizes)

        if self.segment_direction != None and self.global_direction != None:
            print("SEGMENT_DIRECTION:", self.segment_direction)
            print("GLOBAL_DIRECTION:", self.global_direction)

        if self.scope:
            print("SCOPE:", self.scope)

        if self.value:
            print("VALUE: ", self.value)

    def memory_size(self):
        return int(np.prod(self.dimension_sizes))
