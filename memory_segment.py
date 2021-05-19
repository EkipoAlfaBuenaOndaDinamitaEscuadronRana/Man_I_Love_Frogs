from symbol import *


class MemorySegment(object):
    def __init__(self, name, size):
        self.name = name
        self.__size = size
        self.__memory = dict()
        self.__symbol_directions = dict()
        self.__type_size = size / 6 
        # self.__used_memory = 0
        # self.__last_memory_loc = 0

        self.ints = 0
        self.flts = self.__type_size
        self.strs = 2 * self.__type_size
        self.chars = 3 * self.__type_size
        self.bools = 4 * self.__type_size
        self.nulls = 5 * self.__type_size

        self.left_memory_ints = self.__type_size
        self.left_memory_flts = self.__type_size
        self.left_memory_strs = self.__type_size
        self.left_memory_chars = self.__type_size
        self.left_memory_bools = self.__type_size
        self.left_memory_nulls = self.__type_size

    # TODO: No estoy 100% seguro de que eso funcione así. Lo checamos después
    def __calculate_symbol_space(self, symbol):
        return self.__used_memory + symbol.memory_size()

    def __get_memory_inital_direction(self, s_type):
        type_inital_position = {
            "INT" : self.ints,
            "FLT" : self.flts,
            "STR" : self.strs,
            "CHAR" : self.chars,
            "BOOL" : self.bools,
            "NULL" : self.nulls,
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
        }

        return left_memory[s_type]

    def temp(self, symbol):
        initial_position = self.__get_memory_inital_direction(symbol.type)
        symbol_position = self.__get_spare_memory(symbol.type) - self.__type_size + initial_position

        return symbol_position


    def insert_symbol(self, symbol):
        symbol_space = symbol.memory_size()
        next_memory_dir = self.__calculate_symbol_space(symbol)

        if next_memory_dir <= self.__size:
            direction = self.__last_memory_loc
            symbol.direction = direction
            self.__memory[direction] = symbol
            self.__last_memory_loc += symbol_space
            self.__used_memory += symbol_space

            return True

        else:
            return False

ms = MemorySegment("Juanito", 60)
s = Symbol("A", "INT")

print(ms.temp(s))
