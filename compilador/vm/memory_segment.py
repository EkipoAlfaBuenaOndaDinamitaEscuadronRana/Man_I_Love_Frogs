import sys
sys.path.insert(1, '/home/adrian/Documents/universidad/8vo Semestre/Compis/man_i_love_frogs')

import compilador.objects.symbol
from compilador.objects.symbol import *


class MemorySegment(object):
    def __init__(self, name, size):
        self.name = name
        self.__size = size
        self.__memory = dict()
        self.__used_memory = 0
        self.__last_memory_loc = 0

    # TODO: No estoy 100% seguro de que eso funcione así. Lo checamos después
    def __calculate_symbol_space(self, symbol):
        return self.__used_memory + Symbol.memory_size(symbol)

    def insert_symbol(self, symbol):
        symbol_space = Symbol.memory_size(symbol)
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

ms = MemorySegment("Data Segment", 4)

a_int = Symbol("a", "INT")
b_int = Symbol("b", "INT")

print(ms.insert_symbol(a_int))
print(ms.insert_symbol(b_int))