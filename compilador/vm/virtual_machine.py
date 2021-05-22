from router_solver import *
import compilador.vm.memory_segment
from compilador.vm.memory_segment import *
import compilador.objects.function_table
from compilador.objects.function_table import *
import compilador.objects.variable_tables
from compilador.objects.variable_tables import *
import compilador.objects.quadruple
from compilador.objects.quadruple import *


class VirtualMachine(object):
    def __init__(self, global_size, constant_size, local_size, func_table=None):
        self.__total_size = global_size + constant_size + local_size
        self.func_table = func_table
        self.global_segment = MemorySegment("Global Segment", global_size, 0)
        self.constant_segment = MemorySegment(
            "Constant Segment", constant_size, global_size
        )

        if func_table:
            local_size_memory = global_size + constant_size

            self.local_segment = self.__build_local_segment(
                local_size, global_size + constant_size
            )
            self.local_functions = len(self.local_segment)

        else:
            self.local_segment = None
            self.local_functions = 0

    def __build_local_segment(
        self,
        local_size,
        local_start_direction,
    ):
        num_local_segments = len(self.func_table.functions) - 1
        if not num_local_segments: return []

        local_segment_size = local_size // num_local_segments

        local_memory_size = local_size // num_local_segments
        start_direction = local_start_direction

        segments = []
        for func_name in self.func_table.functions:
            if func_name != "main":
                segments.append(
                    MemorySegment(func_name, local_segment_size, start_direction)
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
                return False

            return function_segment.insert_symbol(symbol)

    def __get_local_segment(self, direction):
        current_segment_direction = (
            self.global_segment.size + self.constant_segment.size
        )
        for func in self.local_segment:
            func_size = func.size + func.initial_position - 1

            if direction <= func_size:
                return func

    def get_direction_symbol(self, direction):
        global_size = self.global_segment.size
        constant_size = self.constant_segment.size

        # Direction is in Global Segment
        if direction < global_size:
            return self.global_segment.search_symbol(direction)

        # Direction is in Constant Segment
        elif direction < global_size + constant_size:
            return self.constant_segment.search_symbol(direction)

        # Direction is bigger than memory
        elif direction > self.__total_size:
            return None

        # Direction is in Local Segment
        else:
            segment = self.__get_local_segment(direction)
            return segment.search_symbol(direction)


    def quadruple_direction_allocator(self, quad_dir):
        current_scope = ""

        for quad in quad_dir:
            curr_quad = quad_dir[quad]
            quad_operation = curr_quad.operator.name

            if quad_operation not in ["GOTO", "GOTOF", "ENDFUNC", "GOSUB", "ENDOF"]:

                if curr_quad.operand_1 and not(curr_quad.operand_1.segment_direction and curr_quad.operand_1.global_direction):
                    self.insert_symbol_in_segment(curr_quad.operand_1.scope, curr_quad.operand_1)

                if curr_quad.operand_2 and not(curr_quad.operand_2.segment_direction and curr_quad.operand_2.global_direction):
                    self.insert_symbol_in_segment(curr_quad.operand_2.scope, curr_quad.operand_2)

                if curr_quad.result_id and not(curr_quad.result_id.segment_direction and curr_quad.result_id.global_direction):
                    self.insert_symbol_in_segment(curr_quad.result_id.scope, curr_quad.result_id)

add = Symbol("ADD", "operation")
a = Symbol("A", "INT")
b = Symbol("B", "FLT")
t1 = Symbol("T1", "FLT")

a.scope = "Constant Segment"
b.scope = "Constant Segment"
t1.scope = "Constant Segment"

quad_dir = { 0: Quadruple(add, a, b, t1) }

# quad_dir[0].operator.print_symbol()
# print()
# quad_dir[0].operand_1.print_symbol()
# print()
# quad_dir[0].operand_2.print_symbol()
# print()
# quad_dir[0].result_id.print_symbol()
# print("-----------------------")

ft = FunctionTable()
vt = VariableTable()
ft.set_function("main", "void", [], vt)
real_vm = VirtualMachine(3000, 1000, 6000, ft)

real_vm.quadruple_direction_allocator(quad_dir)

# quad_dir[0].operator.print_symbol()
# print()
# quad_dir[0].operand_1.print_symbol()
# print()
# quad_dir[0].operand_2.print_symbol()
# print()
# quad_dir[0].result_id.print_symbol()
# print()
