import sys
sys.path.append('../')
from memory_segment import *


class VirtualMachineMap(object):
  def __init__(self, ds_size, cs_size, ss_size, es_size):
    self.__ds = MemorySegment("Data Segment", ds_size)
    self.__cs = MemorySegment("Code Segment", cs_size)
    self.__ss = MemorySegment("Stack Segment", ss_size)
    self.__es = MemorySegment("Extra Segment", es_size)

  def insert_symbol_in_segment(self, segment_name, symbol):
    if segment_name == "Data Segment":
      return self.__ds.insert_symbol(symbol)

    elif segment_name == "Code Segment":
      return self.__cs.insert_symbol(symbol)

    elif segment_name == "Stack Segment":
      return self.__ss.insert_symbol(symbol)

    elif segment_name == "Extra Segment":
      return self.__es.insert_symbol(symbol)

    else:
      return False


vmm = VirtualMachineMap(4, 4, 4, 4)
a_int = Symbol("a", "INT")
print(vmm.insert_symbol_in_segment("Data Segment", a_int))
