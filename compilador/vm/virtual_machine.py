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
import game_engine.instruction
from game_engine.instruction import *


class VirtualMachine(object):
    def __init__(self, global_size, constant_size, local_size, func_table=None):
        self.__total_size = global_size + constant_size + local_size
        self.func_table = func_table
        self.global_segment = MemorySegment("Global Segment", global_size, 0)
        self.constant_segment = MemorySegment(
            "Constant Segment", constant_size, global_size
        )
        self.declared_symbols = []

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

    def insert_symbol_in_segment(self, segment_name, symbol):
        self.declared_symbols.append(symbol)

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
        return symbol and not (
            symbol.segment_direction != None and symbol.global_direction != None
        ) and symbol.type != "address"

    def quadruple_direction_allocator(self, quad_dir):
        current_scope = ""

        for quad in quad_dir:
            curr_quad = quad_dir[quad]
            quad_operation = curr_quad.operator.name

            if quad_operation not in ["GOTO", "GOTOF", "ENDFUNC", "ENDOF"]:
                operand_1 = curr_quad.operand_1
                operand_2 = curr_quad.operand_2
                result_id = curr_quad.result_id

                if self.__not_allocated(operand_1) and operand_1.name != "READ":
                    self.insert_symbol_in_segment(operand_1.scope, operand_1)

                if self.__not_allocated(operand_2):
                    self.insert_symbol_in_segment(operand_2.scope, operand_2)

                if self.__not_allocated(curr_quad.result_id):
                    self.insert_symbol_in_segment(result_id.scope, result_id)

    def __resolve_op(self, operation, dir_opnd_1, dir_opnd_2, dir_result):
        val_opnd_1 = self.get_direction_symbol(dir_opnd_1).value
        val_opnd_2 = self.get_direction_symbol(dir_opnd_2).value
        result = self.get_direction_symbol(dir_result)

        # print("------------dir_opnd_1-------------:", dir_opnd_1)
        # print("------------dir_opnd_2-------------:", dir_opnd_2)
        # print("------------operation-------------:", operation)

        if operation == "ADD":
            result.value = val_opnd_1 + val_opnd_2
        elif operation == "SUB":
            result.value = val_opnd_1 - val_opnd_2
        elif operation == "MUL":
            result.value = val_opnd_1 * val_opnd_2
        elif operation == "DIV":
            result.value = val_opnd_1 / val_opnd_2
        elif operation == "MOD":
            result.value = val_opnd_1 % val_opnd_2
        elif operation == "BEQ":
            result.value = val_opnd_1 == val_opnd_2
        elif operation == "BNEQ":
            result.value = val_opnd_1 != val_opnd_2
        elif operation == "OR":
            result.value = val_opnd_1 or val_opnd_2
        elif operation == "AND":
            result.value = val_opnd_1 and val_opnd_2
        elif operation == "LT":
            result.value = val_opnd_1 < val_opnd_2
        elif operation == "GT":
            result.value = val_opnd_1 > val_opnd_2
        elif operation == "LTE":
            result.value = val_opnd_1 <= val_opnd_2
        elif operation == "GTE":
            result.value = val_opnd_1 >= val_opnd_2

        # print("------------result.value-------------:", result.value)

    def __resolve_eq(self, assign_op, dir_opnd, dir_result):
        val_operand = self.get_direction_symbol(dir_opnd).value
        result = self.get_direction_symbol(dir_result)

        if assign_op == "EQ":
            result.value = val_operand
        elif assign_op == "ADDEQ":
            result.value += val_operand
        elif assign_op == "SUBEQ":
            result.value -= val_operand
        elif assign_op == "MULEQ":
            result.value *= val_operand
        elif assign_op == "DIVEQ":
            result.value /= val_operand
        elif assign_op == "MODEQ":
            result.value %= val_operand

    def __resolve_param(self, dir_operand, dir_result, saved_params):
        val_operand = self.get_direction_symbol(dir_operand).value
        result = self.get_direction_symbol(dir_result)
        result.value = val_operand
        saved_params.append(result)

    def __resolve_write(self, dir_result):
        print(self.get_direction_symbol(dir_result).value)

    # TODO: No lo he probado lo suficiente
    def __resolve_read(self, dir_result):
        user_input = input()
        symbol = self.get_direction_symbol(dir_result)

        if symbol.type == "INT":
            symbol.value = int(user_input)

        elif symbol.type == "FLT":
            symbol.value = float(user_input)

        elif symbol.type == "CHAR":
            # TODO: Ver como validar que sea un solo char
            symbol.value = user_input[0]

        elif symbol.type == "STR":
            symbol.value = user_input

        elif symbol.type == "BOOL":
            booleans = {"true": True, "false": False, "1": True, "0": False}
            symbol.value = booleans[user_input]

        elif symbol.type == "NULL":
            # TODO: Ver como validar que sea siempre null
            if user_input == "null":
                symbol.value = None

    def __resolve_frog_method(self, operation, dir_frog, dir_result):
        frog = self.get_direction_symbol(dir_frog).name
        times = self.get_direction_symbol(dir_result).value

        return Instruction(frog, operation, times)

    def __add_params(self, saved_params, func_name):
        for param in self.func_table.functions[func_name]["p"]:
            param.value = saved_params.pop(0).value

    def __resolve_return(self, saved_functions, dir_operand):
        function = saved_functions.pop()
        val_operand = self.get_direction_symbol(dir_operand).value
        function.value = val_operand
        # print("------------------__resolve_return------------------")
        # function.print_symbol()

    def run(self, quad_dir):
        era = False
        running = True
        instruction = 1
        saved_params = []
        saved_positions = []
        saved_functions = []
        game_instructions = []

        while running:
            curr_quad = quad_dir[instruction]
            operation = curr_quad.operator.name
            type = curr_quad.operator.type

            if type in ["operation", "comparison", "matching"]:
                dir_opnd_1 = curr_quad.operand_1.global_direction
                dir_opnd_2 = curr_quad.operand_2.global_direction
                dir_result = curr_quad.result_id.global_direction

                self.__resolve_op(operation, dir_opnd_1, dir_opnd_2, dir_result)

            elif operation in set.union(SemanticTable.assignment_operations_op, {"EQ"}):
                if operation == "EQ" and curr_quad.operand_1.name == "READ":
                    dir_result = curr_quad.result_id.global_direction
                    self.__resolve_read(dir_result)

                else:
                    dir_operand = curr_quad.operand_1.global_direction
                    dir_result = curr_quad.result_id.global_direction

                    if curr_quad.operand_1.name == "square":
                        # print("------------------EQ------------------")
                        # print("operand_1:")
                        # curr_quad.operand_1.print_symbol()
                        pass


                    self.__resolve_eq(operation, dir_operand, dir_result)

            elif operation == "GOTO":
                instruction = curr_quad.result_id.name
                continue

            elif operation == "GOSUB":
                function = curr_quad.operand_1
                self.__add_params(saved_params, function.name)
                saved_functions.append(function)
                saved_positions.append(instruction + 1)
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

            elif operation == "ERA":
                era = True

            elif operation == "PARAM":
                dir_operand = curr_quad.operand_1.global_direction
                dir_result = curr_quad.result_id.global_direction
                self.__resolve_param(dir_operand, dir_result, saved_params)

            elif operation == "ENDFUNC":
                instruction = saved_positions.pop()
                continue

            elif operation == "RETURN":
                dir_operand = curr_quad.operand_1.global_direction
                self.__resolve_return(saved_functions, dir_operand)

            elif type == "obj_method":
                dir_frog = curr_quad.operand_1.global_direction
                dir_result = curr_quad.result_id.global_direction
                game_instructions.append(
                    self.__resolve_frog_method(operation, dir_frog, dir_result)
                )

            instruction += 1
            if instruction > len(quad_dir):
                running = False

        return game_instructions
