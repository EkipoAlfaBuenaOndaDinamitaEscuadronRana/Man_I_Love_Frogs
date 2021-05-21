from router_solver import *
import compilador.vm.memory_segment
from compilador.vm.memory_segment import *
import compilador.objects.function_table
from compilador.objects.function_table import *
import compilador.objects.variable_tables
from compilador.objects.variable_tables import *


class VirtualMachine(object):
    def __init__(self, global_size, constant_size, local_size, func_table=None):
        self.__total_size = global_size + constant_size + local_size
        self.func_table = func_table
        self.global_segment = MemorySegment("Global Segment", global_size, 0)
        self.constant_segment = MemorySegment(
            "Constant Segment", constant_size, global_size + 1
        )

        if func_table:
            local_size_memory = global_size + constant_size + local_size
            self.local_segment = self.__build_local_segment(
                local_size, constant_size + 1, local_size_memory
            )

        else:
            self.local_segment = None

    def __build_local_segment(
        self, local_size, local_start_direction, local_size_memory
    ):
        num_local_segments = len(self.func_table.functions) - 1
        local_segment_size = local_size / num_local_segments

        local_memory_size = local_size_memory / num_local_segments
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

            # The function was not found
            if function_segment == None:
                print("Function was not found")
                return False

            return function_segment.insert_symbol(symbol)

    def get_direction_symbol(self, direction):
        global_size = self.global_segment.size
        constant_size = self.constant_segment.size

        # Direction is in Global Segment
        if direction <= global_size:
            print("WENT to global")
            return self.global_segment.search_symbol(direction)

        # Direction is in Constant Segment
        elif direction <= global_size + constant_size:
            print("WENT to constant")
            return self.constant_segment.search_symbol(direction)

        # Direction is bigger than memory
        elif direction > self.__total_size:
            print("Direction out of bounds")
            return None

        # Direction is in Local Segment
        else:
            pass

ft = FunctionTable()
vt = VariableTable()
ft.set_function("func", "void", [], vt)
ft.set_function("main", "void", [], vt)

vm = VirtualMachine(7, 7, 7, ft)

a_int = Symbol("A", "INT")
b_flt = Symbol("B", "FLT")
c_str = Symbol("C", "STR")
d_char = Symbol("D", "CHAR")
e_bool = Symbol("E", "BOOL")
f_null = Symbol("F", "NULL")
g_frog = Symbol("G", "FROG")

vm.insert_symbol_in_segment("Global Segment", a_int)
vm.insert_symbol_in_segment("Global Segment", b_flt)
vm.insert_symbol_in_segment("Global Segment", c_str)
vm.insert_symbol_in_segment("Global Segment", d_char)
vm.insert_symbol_in_segment("Global Segment", e_bool)
vm.insert_symbol_in_segment("Global Segment", f_null)
vm.insert_symbol_in_segment("Global Segment", g_frog)

vm.insert_symbol_in_segment("Constant Segment", a_int)
vm.insert_symbol_in_segment("Constant Segment", b_flt)
vm.insert_symbol_in_segment("Constant Segment", c_str)
vm.insert_symbol_in_segment("Constant Segment", d_char)
vm.insert_symbol_in_segment("Constant Segment", e_bool)
vm.insert_symbol_in_segment("Constant Segment", f_null)
vm.insert_symbol_in_segment("Constant Segment", g_frog)

vm.get_direction_symbol(0).print_symbol()
vm.get_direction_symbol(1).print_symbol()
vm.get_direction_symbol(2).print_symbol()
vm.get_direction_symbol(3).print_symbol()
vm.get_direction_symbol(4).print_symbol()
vm.get_direction_symbol(5).print_symbol()
vm.get_direction_symbol(6).print_symbol()
# vm.get_direction_symbol(7).print_symbol()
