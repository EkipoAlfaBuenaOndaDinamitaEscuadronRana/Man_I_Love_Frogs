import compilador.objects.symbol
from compilador.objects.symbol import *


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
 