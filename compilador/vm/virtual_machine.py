from router_solver import *
import compilador.vm.memory_segment
from compilador.vm.memory_segment import *
import compilador.objects.function_table
from compilador.objects.function_table import *
import compilador.objects.variable_tables
from compilador.objects.variable_tables import *


class VirtualMachine(object):
    def __init__(self, global_size, constant_size, local_size, func_table = None):
        # print("--------------------init-------------------")
        self.func_table = func_table
        self.global_segment = MemorySegment("Global Segment", global_size, 0)
        self.constant_segment = MemorySegment("Constant Segment", constant_size, global_size + 1)

        if func_table:
            # print("func_table: ", func_table.functions)
            total_size_memory = global_size + constant_size + local_size
            # print("total_size_memory: ", total_size_memory)
            self.local_segment = self.__build_local_segment(local_size, constant_size + 1, total_size_memory)

        else:
            self.local_segment = None

    def __build_local_segment(self, local_size, local_start_direction, total_size_memory):
        num_local_segments = self.func_table.length() - 1
        local_segment_size = local_size / num_local_segments

        local_memory_size = total_size_memory / num_local_segments
        start_direction = local_start_direction

        segments = []
        for func_name in self.func_table.functions:
            if func_name != "main":
                segments.append(MemorySegment(func_name, local_segment_size, start_direction + 1))
                start_direction += local_memory_size

        return segments

    def __find_function_segment(self, func_name):
        # print("segment_name:", func_name)
        # print("local_segment:", self.local_segment)
        for func_segment in self.local_segment:

            if func_segment.name == func_name:
                return func_segment

        return None

    # TODO: Ahorita se inserta con nombre del segmento, estaría cool que fuera también con la dirección
    def insert_symbol_in_segment(self, segment_name, symbol):
        # print("--------------------start--------------------")
        # A symbol in global segment arrive
        if segment_name == "Global Segment":
            # print("Inserted into global_segment")
            return self.global_segment.insert_symbol(symbol)

        # A symbol in constant segment arrive
        elif segment_name == "Constant Segment":
            # print("Inserted into constant_segment")
            return self.constant_segment.insert_symbol(symbol)

        # A symbol in local segment arrive
        else:
            # print("Inserted into local_segment")
            function_segment = self.__find_function_segment(segment_name)

            if function_segment == None:
                # print("function was not found")
                return False

            return function_segment.insert_symbol(symbol)

ft = FunctionTable()
vt = VariableTable()
ft.set_function("func", "void", [], vt)
ft.set_function("main", "void", [], vt)

vm = VirtualMachine(21, 7, 42, ft)
s = Symbol("A", "FLT")
f = Symbol("f", "FROG")


# res_s_1 = vm.insert_symbol_in_segment("Global Segment", s)
# print("result:", res_s_1)
# print("---------------------end---------------------\n")
# res_s_2 = vm.insert_symbol_in_segment("Global Segment", s)
# print("result:", res_s_2)
# print("---------------------end---------------------\n")
# res_s_3 = vm.insert_symbol_in_segment("Global Segment", s)
# print("result:", res_s_3)
# print("---------------------end---------------------\n")
# res_s_4 = vm.insert_symbol_in_segment("Global Segment", s)
# print("result:", res_s_4)
# print("---------------------end---------------------\n")


res_f_1 = vm.insert_symbol_in_segment("func", s)
# print("result:", res_f_1)
# print("---------------------end---------------------\n")

res_f_2 = vm.insert_symbol_in_segment("func", s)
# print("result:", res_f_2)
# print("---------------------end---------------------\n")

res_f_3 = vm.insert_symbol_in_segment("func", s)
# print("result:", res_f_3)
# print("---------------------end---------------------\n")