from router_solver import *
import compilador.vm.memory_segment
from compilador.vm.memory_segment import *


class VirtualMachine(object):
    def __init__(self, global_size, constant_size, local_size, func_table, var_tables):
        self.func_table = func_table
        self.var_tables = var_tables
        self.global_segment = MemorySegment("Global Segment", global_size, 0)
        self.constant_segment = MemorySegment("Constant Segment", constant_size, global_size + 1)

        total_size_memory = global_size + constant_size + local_size
        self.local_segment = self.__build_local_segment(local_size, constant_size + 1, total_size_memory)

    def __build_local_segment(self, local_size, local_start_direction, total_size_memory):
        num_local_segments = len(self.func_table) - 1
        local_segment_size = local_size / num_local_segments

        local_memory_size = total_size_memory / num_local_segments
        start_direction = local_start_direction

        segments = []
        for func_name in self.func_table:
            if func_table != "main":
                segments.append(MemorySegment(func_name, local_segment_size, start_direction + 1))
                start_direction += local_memory_size

        return segments

    def __find_function_segment(self, func_name):
        for func_segment in local_segment:
            if func_segment.name == func_name:
                return func_segment

        return None

    def insert_symbol_in_segment(self, segment_name, symbol):
        # A symbol in global segment arrive
        if segment_name == "Global Segment":
            return self.global_segment.insert_symbol(symbol)

        # A symbol in constant segment arrive
        elif segment_name == "Constant Segment":
            return self.constant_segment.insert_symbol(symbol)

        # A symbol in local segment arrive
        else:
            function_segment = self.__find_function_segment(segment_name)

            if function_segment == None:
                print("function was not found")
                return False

            return func_segment.insert_symbol(symbol)
