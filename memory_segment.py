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
    used_symbol_space = self.__calculate_symbol_space(symbol)

    print("-----------------------------------------")
    print("symbol.name:", symbol.name)
    print("symbol.size:", symbol.memory_size())
    print("before\n  used_memory:", self.__used_memory)
    print("  last_memory_loc:", self.__last_memory_loc)

    if used_symbol_space <= self.__size:
      direction = self.__last_memory_loc
      symbol.direction = direction
      self.__memory[direction] = symbol
      self.__last_memory_loc += symbol_space
      self.__used_memory += symbol_space
      print("after\n  used_memory:", self.__used_memory)
      print("  last_memory_loc:", self.__last_memory_loc)
      print("-----------------------------------------")
      return True

    else:
      return False

ms = MemorySegment("Data Segment", 4)
a_int = Symbol("a", "INT")
b_int = Symbol("b", "INT")

a_res = ms.insert_symbol(a_int)
b_res = ms.insert_symbol(b_int)

print("\n", a_res, b_res)