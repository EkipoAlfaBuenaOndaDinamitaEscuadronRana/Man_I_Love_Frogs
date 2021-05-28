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
        elif operation == "BEQ":
            self.get_direction_symbol(dir_result).value = val_opnd_1 == val_opnd_2
        elif operation == "BNEQ":
            self.get_direction_symbol(dir_result).value = val_opnd_1 != val_opnd_2
        elif operation == "OR":
            self.get_direction_symbol(dir_result).value = val_opnd_1 or val_opnd_2
        elif operation == "AND":
            self.get_direction_symbol(dir_result).value = val_opnd_1 and val_opnd_2
        elif operation == "LT":
            self.get_direction_symbol(dir_result).value = val_opnd_1 < val_opnd_2
        elif operation == "GT":
            self.get_direction_symbol(dir_result).value = val_opnd_1 > val_opnd_2
        elif operation == "LTE":
            self.get_direction_symbol(dir_result).value = val_opnd_1 <= val_opnd_2
        elif operation == "GTE":
            self.get_direction_symbol(dir_result).value = val_opnd_1 >= val_opnd_2

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

    # TODO: No lo he probado lo suficiente
    def __resolve_read(self, dir_result):
        input = input()
        symbol = self.get_direction_symbol(dir_result)

        if symbol.type == "INT":
            symbol.value = int(input)

        elif symbol.type == "FLT":
            symbol.value = float(input)

        elif symbol.type == "CHAR":
            # TODO: Ver como validar que sea un solo char
            symbol.value = input[0]

        elif symbol.type == "STR":
            symbol.value = input

        elif symbol.type == "BOOL":
            booleans = {
                "true": True,
                "false": False,
                "1": True,
                "0": False
            }
            symbol.value = booleans[input]

        elif symbol.type == "NULL":
            # TODO: Ver como validar que sea siempre null
            if input == "null":
                symbol.value = None


    def run(self, quad_dir):
        running = True
        instruction = 1
        game_instructions = []

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
                instruction = curr_quad.result_id.name
                continue

            elif operation == "GOSUB":
                instruction = curr_quad.result_id.name
                continue

            elif operation == "GOTOF" and not curr_quad.operand_1.value:
                    instruction = curr_quad.result_id.name
                    continue

            elif operation == "ENDOF":
                running = False
                continue

            elif operation == "WRITE":
                dir_result = curr_quad.result_id.global_direction
                self.__resolve_write(dir_result)

            elif operation == "READ":
                dir_result = curr_quad.result_id.global_direction
                self.__resolve_read(dir_result)

            elif operation == "ERA":
                pass

            instruction += 1
            if instruction > len(quad_dir):
                running = False

        return game_instructions

# comparison
beq = Symbol("BEQ", "matching")

# compiler functions
goto = Symbol("GOTO")
gotof = Symbol("GOTOF")
write = Symbol("WRITE")
endof = Symbol("ENDOF")
dir_two = Symbol(2)
dir_six = Symbol(6)
dir_ten = Symbol(10)
dir_ele = Symbol(11)

# Variables
t1 = Symbol("T1", "BOOL")
t2 = Symbol("T2", "BOOL")
uno = Symbol("uno", "STR")
dos = Symbol("dos", "STR")
tres = Symbol("tres", "STR")
one_const = Symbol(1, "INT")
two_const = Symbol(2, "INT")
tree_const = Symbol(3, "INT")
four_const = Symbol(4, "INT")

t1.scope = "main"
t2.scope = "main"
uno.scope = "main"
dos.scope = "main"
tres.scope = "main"
one_const.scope = "Constant Segment"
two_const.scope = "Constant Segment"
tree_const.scope = "Constant Segment"
four_const.scope = "Constant Segment"

# Variable Table
vt = VariableTable()

# Function Table
ft = FunctionTable()
ft.set_function("main", "void", [], vt)

# Virtual Machine
vm = VirtualMachine(3000, 1000, 6000, ft)

main_quads = {
    1: Quadruple(goto, None, None, dir_two),
    2: Quadruple(beq, one_const, two_const, t1),
    3: Quadruple(gotof, t1, None, dir_six),
    4: Quadruple(write, None, None, uno),
    5: Quadruple(goto, None, None, dir_ele),
    6: Quadruple(beq, tree_const, four_const, t2),
    7: Quadruple(gotof, t2, None, dir_ten),
    8: Quadruple(write, None, None, dos),
    9: Quadruple(goto, None, None, dir_ele),
    10: Quadruple(write, None, None, tres),
    11: Quadruple(endof, None, None, None),
}
vm.quadruple_direction_allocator(main_quads)

for q in main_quads:
    print("======================================")
    main_quads[q].print_quad()

vm.run(main_quads)
