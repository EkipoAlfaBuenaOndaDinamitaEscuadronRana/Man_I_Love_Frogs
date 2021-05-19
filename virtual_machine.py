from memory_segment import *


class VirtualMachine(object):
    def __init__(self, global_size, constant_size, local_size, func_table):
        self.__global = MemorySegment("Global Segment", global_size)
        self.__constant = MemorySegment("Stack Segment", constant_size)
        self.__local = self.__build_local_memory()

        num_functions = len(func_table) - 1
        local_segment_size = local_size / num_functions


        # Esto no será así
        for i in func_table:
            self.__local.append()
            MemorySegment(i, local_segment_size)

    def __build_local_memory(self):
        num_functions = len(func_table) - 1
        local_segment_size = local_size / num_functions

    # def __init__(self, ds_size, cs_size, ss_size, es_size):
    #     self.__ds = MemorySegment("Data Segment", ds_size)
    #     self.__cs = MemorySegment("Code Segment", cs_size)
    #     self.__ss = MemorySegment("Stack Segment", ss_size)
    #     self.__es = MemorySegment("Extra Segment", es_size)

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

    def get_symbol_in_segment(self, symbol):
        pass

    def process_individal_quadruple(self, quad):
        pass

    def process_quadruples(self, quads):
        pass
