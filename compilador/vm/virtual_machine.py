from router_solver import *
import compilador.vm.memory_segment
from compilador.vm.memory_segment import *
import compilador.objects.function_table
from compilador.objects.function_table import *
import compilador.objects.variable_tables
from compilador.objects.variable_tables import *
import compilador.objects.quadruple
from compilador.objects.quadruple import *
import compilador.objects.semantic_table
from compilador.objects.semantic_table import *


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
        num_local_segments = len(self.func_table.functions)
        if not num_local_segments:
            return []

        local_segment_size = local_size // num_local_segments

        local_memory_size = local_size // num_local_segments
        start_direction = local_start_direction

        segments = []
        for func_name in self.func_table.functions:
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

    def __not_allocated(self, symbol):
        return symbol and not (symbol.segment_direction and symbol.global_direction)

    def quadruple_direction_allocator(self, quad_dir):
        current_scope = ""

        for quad in quad_dir:
            curr_quad = quad_dir[quad]
            quad_operation = curr_quad.operator.name

            if quad_operation not in ["GOTO", "GOTOF", "ENDFUNC", "GOSUB", "ENDOF"]:
                operand_1 = curr_quad.operand_1
                operand_2 = curr_quad.operand_2
                result_id = curr_quad.result_id

                if self.__not_allocated(operand_1):
                    self.insert_symbol_in_segment(operand_1.scope, operand_1)

                if self.__not_allocated(operand_2):
                    self.insert_symbol_in_segment(operand_2.scope, operand_2)

                if self.__not_allocated(curr_quad.result_id):
                    self.insert_symbol_in_segment(result_id.scope, result_id)

    def __resolve_op(self, operation, dir_opnd_1, dir_opnd_2, dir_result):
        val_opnd_1 = self.get_direction_symbol(dir_opnd_1).value
        val_opnd_2 = self.get_direction_symbol(dir_opnd_2).value

        if operation == "ADD":
            self.get_direction_symbol(dir_result).value = val_opnd_1 + val_opnd_2
        elif operation == "SUB":
            self.get_direction_symbol(dir_result).value = val_opnd_1 - val_opnd_2
        elif operation == "MUL":
            self.get_direction_symbol(dir_result).value = val_opnd_1 * val_opnd_2
        elif operation == "DIV":
            self.get_direction_symbol(dir_result).value = val_opnd_1 / val_opnd_2
        elif operation == "MOD":
            self.get_direction_symbol(dir_result).value = val_opnd_1 % val_opnd_2

    def __resolve_eq(self, assign_op, dir_opnd, dir_result):
        val_opnd = self.get_direction_symbol(dir_opnd).value

        if assign_op == "EQ":
            self.get_direction_symbol(dir_result).value = val_opnd
        elif assign_op == "ADDEQ":
            self.get_direction_symbol(dir_result).value += val_opnd
        elif assign_op == "SUBEQ":
            self.get_direction_symbol(dir_result).value -= val_opnd
        elif assign_op == "MULEQ":
            self.get_direction_symbol(dir_result).value *= val_opnd
        elif assign_op == "DIVEQ":
            self.get_direction_symbol(dir_result).value /= val_opnd
        elif assign_op == "MODEQ":
            self.get_direction_symbol(dir_result).value %= val_opnd

    def __resolve_write(self, dir_result):
        print(self.get_direction_symbol(dir_result).value)

    def run(self, quad_dir):
        running = True
        instruction = 1

        while running:
            curr_quad = quad_dir[instruction]
            operation = curr_quad.operator.name

            if operation in set.union(
                SemanticTable.operations_op,
                SemanticTable.comparison_op,
                SemanticTable.matching_op,
            ):
                dir_opnd_1 = curr_quad.operand_1.global_direction
                dir_opnd_2 = curr_quad.operand_2.global_direction
                dir_result = curr_quad.result_id.global_direction

                self.__resolve_op(operation, dir_opnd_1, dir_opnd_2, dir_result)

            elif operation in set.union(SemanticTable.assignment_operations_op, {"EQ"}):
                dir_opnd = curr_quad.operand_1.global_direction
                dir_result = curr_quad.result_id.global_direction

                self.__resolve_eq(operation, dir_opnd, dir_result)

            elif operation == "GOTO":
                # REVISA ESTOOO
                instruction = curr_quad.result_id
                continue

            elif operation == "ENDOF":
                running = False
                continue

            elif operation == "WRITE":
                dir_result = curr_quad.result_id.global_direction
                self.__resolve_write(dir_result)

            instruction += 1
            if instruction > len(quad_dir):
                running = False


# Operators
eq = Symbol("EQ", "assignment")
add = Symbol("ADD", "operation")

# States
goto = Symbol("GOTO")
write = Symbol("WRITE")
endof = Symbol("ENDOF")

# Constants
one = Symbol(1, "INT")
two = Symbol(5, "INT")
one.scope = "Constant Segment"
two.scope = "Constant Segment"

# Variables
a = Symbol("A", "INT")
b = Symbol("B", "INT")
t4 = Symbol("T4", "INT")  # Duda: Me generó T4, ¿qué pedo xD?
a.scope = "main"
b.scope = "main"
t4.scope = "main"

# Variable Table
vt = VariableTable()
vt.set_variable(a)
vt.set_variable(b)

# Function Table
ft = FunctionTable()
ft.set_function("main", "void", [], vt)

# Virtual Machine
vm = VirtualMachine(3000, 1000, 6000, ft)

quads = {
    1: Quadruple(goto, None, None, 2),  # Empieza en 1  # ESTO ES UN quadruplo
    2: Quadruple(eq, one, None, a),
    3: Quadruple(eq, two, None, b),
    4: Quadruple(add, a, b, t4),
    5: Quadruple(write, None, None, t4),
    6: Quadruple(endof, None, None, None),
}

vm.quadruple_direction_allocator(quads)
vm.run(quads)
