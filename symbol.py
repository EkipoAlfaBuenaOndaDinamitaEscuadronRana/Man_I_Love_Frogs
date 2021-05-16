import numpy as np

class Symbol(object):
    # All memory sizes are expressed in bytes.
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

    # TODO: No calcula bien las dimensiones
    def memory_size(self):
        return Symbol.__memory_sizes[self.type] * (np.prod(self.dimension_sizes) + 1)
