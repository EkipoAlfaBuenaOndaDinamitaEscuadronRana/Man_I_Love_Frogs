from router_solver import *
import compilador.vm.memory_segment
from compilador.vm.memory_segment import *
import compilador.objects.function_table
from compilador.objects.function_table import *
import compilador.objects.variable_tables
from compilador.objects.variable_tables import *


class VirtualMachine(object):
    def __init__(self, global_size, constant_size, local_size, func_table=None):
        self.func_table = func_table
        self.global_segment = MemorySegment("Global Segment", global_size, 0)
        self.constant_segment = MemorySegment(
            "Constant Segment", constant_size, global_size + 1
        )

        if func_table:
            total_size_memory = global_size + constant_size + local_size
            self.local_segment = self.__build_local_segment(
                local_size, constant_size + 1, total_size_memory
            )

        else:
            self.local_segment = None

    def __build_local_segment(
        self, local_size, local_start_direction, total_size_memory
    ):
        num_local_segments = self.func_table.length() - 1
        local_segment_size = local_size / num_local_segments

        local_memory_size = total_size_memory / num_local_segments
        start_direction = local_start_direction

        segments = []
        for func_name in self.func_table.functions:
            if func_name != "main":
                segments.append(
                    MemorySegment(func_name, local_segment_size, start_direction + 1)
                )
                start_direction += local_memory_size

        return segments

    def __find_function_segment(self, func_name):
        for func_segment in self.local_segment:

            if func_segment.name == func_name:
                return func_segment

        return None

    # TODO: Ahorita se inserta con nombre del segmento, estaría cool que fuera también con la dirección
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
                return False

            return function_segment.insert_symbol(symbol)
