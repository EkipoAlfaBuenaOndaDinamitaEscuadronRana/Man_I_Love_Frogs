import numpy as np


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
        Symbol("mat", "FLT", [3][10])
    
    It is also possible to specify a memory address. 
    However, this value is expected to be assigned by the virtual machine.
    """
    __memory_sizes = { 
        "INT": 4,
        "FLT": 4,
        "CHAR": 1,
        "STR": 1,
        "BOOL": 1,
        "NULL": 1,
    }

    def __init__(self, name=None, type=None, dimension_sizes=[], direction=None):
        self.name = name
        self.type = type
        self.dimension_sizes = dimension_sizes
        self.dimensions = len(dimension_sizes)
        self.direction = direction

    def __eq__(self, quad):
        return self.name == quad.name and self.type == quad.type

    def __hash__(self):
        return id(self)

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.type = type

    def get_name(self):
        return self.name

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
            return Symbol.__memory_sizes[self.type] * (np.prod(self.dimension_sizes))

        return Symbol.__memory_sizes[self.type]
