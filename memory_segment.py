from symbol import *

class MemorySegment(object):
  def __init__(self, name, size):
    self.name = name
    self.__size = size
    self.__memory = dict()
    self.__used_memory = 0
    self.__last_memory_loc = 0

  # TODO: Creo que esto no funciona así
  def __calculate_symbol_space(self, symbol):
    return self.__used_memory + symbol.memory_size()

  def insert_symbol(self, symbol):
    # symbol_space = self.__calculate_symbol_space(symbol)
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
