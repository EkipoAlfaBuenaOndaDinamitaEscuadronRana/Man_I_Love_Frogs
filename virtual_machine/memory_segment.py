import sys
sys.path.append('../')
from symbol import *

class MemorySegment(object):
  def __init__(self, name, size):
    self.name = name
    self.__size = size
    self.__memory = dict()
    self.__used_memory = 0
    self.__last_memory_loc = 0

  def get_symbol_on_memory_loc(self, direction):
    return self.__memory[direction]

  def calculate_symbol_space(symbol):
    return self.__used_memory + symbol.memory_size()

  def insert_symbol(self, symbol):
    symbol_space = calculate_symbol_space(symbol)

    if symbol_space <= self.__size:
      direction = self.__last_memory_loc
      symbol.direction = direction
      self.__memory[direction] = symbol
      self.__last_memory_loc += symbol_space
      return True

    else:
      return False
