# import compilador.objects.symbol
# from compilador.objects.symbol import *


# TODO: Borrar todo lo que está dentro de symbol
# Symbooooooool
# import compilador.helpers.printer
# from compilador.helpers.printer import *
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

# NOTE: This sizes are no longer real... But I don't want to delete them...
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

    # NOTE: This funcion is no longer needed... But I don't want to delete it
    def memory_size(self):
        if self.dimensions:
            return memory_sizes[self.type] * (np.prod(self.dimension_sizes))

        return memory_sizes[self.type]


class MemorySegment(object):
    def __init__(self, name, size):
        self.name = name
        self.__size = size
        self.__memory = dict()

        self.__symbol_directions = dict()

        self.__type_size = int(size / 7)

        self.ints = 0
        self.flts = self.__type_size
        self.strs = 2 * self.__type_size
        self.chars = 3 * self.__type_size
        self.bools = 4 * self.__type_size
        self.nulls = 5 * self.__type_size
        self.frogs = 6 * self.__type_size

        self.left_memory_ints = self.__type_size
        self.left_memory_flts = self.__type_size
        self.left_memory_strs = self.__type_size
        self.left_memory_chars = self.__type_size
        self.left_memory_bools = self.__type_size
        self.left_memory_nulls = self.__type_size
        self.left_memory_frogs = self.__type_size

    # TODO: No estoy 100% seguro de que eso funcione así. Lo checamos después
    def __calculate_symbol_space(self, symbol):
        return self.__used_memory + Symbol.memory_size(symbol)

    def __get_memory_inital_direction(self, s_type):
        type_inital_position = {
            "INT" : self.ints,
            "FLT" : self.flts,
            "STR" : self.strs,
            "CHAR" : self.chars,
            "BOOL" : self.bools,
            "NULL" : self.nulls,
            "FROG" : self.frogs,
        }

        return type_inital_position[s_type]

    def __get_spare_memory(self, s_type):
        left_memory = {
            "INT" : self.left_memory_ints,
            "FLT" : self.left_memory_flts,
            "STR" : self.left_memory_strs,
            "CHAR" : self.left_memory_chars,
            "BOOL" : self.left_memory_bools,
            "NULL" : self.left_memory_nulls,
            "FROG" : self.left_memory_frogs,
        }

        return left_memory[s_type]

    def __substract_memory(self, s_type):
        if s_type == "INT":
            self.left_memory_ints -= 1

        elif s_type == "FLT":
            self.left_memory_flts -= 1

        elif s_type == "STR":
            self.left_memory_strs -= 1

        elif s_type == "CHAR":
            self.left_memory_chars -= 1

        elif s_type == "BOOL":
            self.left_memory_bools -= 1

        elif s_type == "NULL":
            self.left_memory_nulls -= 1

        elif s_type == "FROG":
            self.left_memory_frogs -= 1

    def insert_symbol(self, symbol):
        s_type = symbol.type
        initial_position = self.__get_memory_inital_direction(s_type)
        symbol_position = self.__get_spare_memory(symbol.type) - self.__type_size + initial_position

        if symbol_position <= initial_position + self.__type_size:
            self.__memory[symbol_position] = symbol
            self.__substract_memory(s_type)



            return symbol_position

        else:
            return False


ms = MemorySegment("Juanito", 7)
s = Symbol("A", "FLT")

print(ms.insert_symbol(s))
# print(ms.insert_symbol(s))
 