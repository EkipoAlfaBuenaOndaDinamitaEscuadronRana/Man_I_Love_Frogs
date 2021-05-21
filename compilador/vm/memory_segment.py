from router_solver import *
import compilador.objects.symbol
from compilador.objects.symbol import *


class MemorySegment(object):
    def __init__(self, name, size, initial_position):
        self.name = name
        self.size = size
        self.__memory = dict()
        self.__symbol_directions = dict()
        self.__inial_position = initial_position

        self.__subsegment_size = int(size / 7)

        self.ints = 0
        self.flts = self.__subsegment_size
        self.strs = 2 * self.__subsegment_size
        self.chars = 3 * self.__subsegment_size
        self.bools = 4 * self.__subsegment_size
        self.nulls = 5 * self.__subsegment_size
        self.frogs = 6 * self.__subsegment_size

        self.spare_memory_ints = self.__subsegment_size
        self.spare_memory_flts = self.__subsegment_size
        self.spare_memory_strs = self.__subsegment_size
        self.spare_memory_chars = self.__subsegment_size
        self.spare_memory_bools = self.__subsegment_size
        self.spare_memory_nulls = self.__subsegment_size
        self.spare_memory_frogs = self.__subsegment_size

    def __get_memory_inital_direction(self, s_type):
        type_inital_position = {
            "INT": self.ints - self.__subsegment_size,
            "FLT": self.flts - self.__subsegment_size,
            "STR": self.strs - self.__subsegment_size,
            "CHAR": self.chars - self.__subsegment_size,
            "BOOL": self.bools - self.__subsegment_size,
            "NULL": self.nulls - self.__subsegment_size,
            "FROG": self.frogs - self.__subsegment_size,
        }

        return type_inital_position[s_type]

    def __get_spare_memory(self, s_type):
        left_memory = {
            "INT": self.spare_memory_ints,
            "FLT": self.spare_memory_flts,
            "STR": self.spare_memory_strs,
            "CHAR": self.spare_memory_chars,
            "BOOL": self.spare_memory_bools,
            "NULL": self.spare_memory_nulls,
            "FROG": self.spare_memory_frogs,
        }

        return left_memory[s_type]

    def __get_symbol_position(self, s_type):
        return (
            self.__subsegment_size
            - self.__get_spare_memory(s_type)
            + self.__get_memory_inital_direction(s_type)
        )

    def __substract_memory(self, symbol):
        s_type = symbol.type
        s_size = symbol.memory_size()

        if s_type == "INT":
            self.spare_memory_ints -= s_size

        elif s_type == "FLT":
            self.spare_memory_flts -= s_size

        elif s_type == "STR":
            self.spare_memory_strs -= s_size

        elif s_type == "CHAR":
            self.spare_memory_chars -= s_size

        elif s_type == "BOOL":
            self.spare_memory_bools -= s_size

        elif s_type == "NULL":
            self.spare_memory_nulls -= s_size

        elif s_type == "FROG":
            self.spare_memory_frogs -= s_size

    # TODO: Does not assign arrays
    def __assign_memory(self, symbol, symbol_position):
        # Scalar or array size 1
        if symbol.memory_size() == 1:
            self.__memory[symbol_position] = symbol

        # Two or three dimensional array
        else:
            pass

    # TODO: Does not work with arrays
    def insert_symbol(self, symbol):
        s_type = symbol.type
        initial_position = self.__get_memory_inital_direction(s_type)
        symbol_position = self.__get_symbol_position(s_type)
        s_size = symbol.memory_size()

        if symbol_position + s_size - 1 < initial_position + self.__subsegment_size:
            self.__assign_memory(symbol, symbol_position)
            self.__substract_memory(symbol)

            return True

        return False

    def search_symbol(self, direction):
        direction = direction - self.__initial_position
        return self.__memory.get(direction, None)
