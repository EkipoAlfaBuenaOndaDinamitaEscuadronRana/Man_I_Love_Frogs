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
        self.next_function_segment = []

        # func_table.print_FuncTable()

        if func_table:
            local_size_memory = global_size + constant_size

            self.local_segment = self.__build_local_segment(
                local_size, global_size + constant_size
            )
            self.local_functions = len(self.local_segment)
            self.__func_table_assign_memory()

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
        segments.append(MemorySegment("main", local_segment_size, start_direction))
        start_direction += local_memory_size
        self.next_function_segment.append(start_direction)
        return segments

    def __func_table_assign_memory(self):
        functions = self.func_table.functions
        tables_init = ["Global Segment", "Constant Segment", "main"]
        for ft in functions:
            if ft in tables_init:
                var_tab = functions[ft]["vt"]
                vars = var_tab.variables
                # var_tab.print_VariableTable()
                for k, v in vars.items():
                    self.insert_symbol_in_segment(ft, v)
                    # vars[k].print_symbol()
                    # print("------------------------")

    def __function_instance(self, func_name):
        function_object = self.func_table.functions
        function_size = function_object[func_name]["s"] * 7
        start_direction = self.next_function_segment.pop()
        name = str(func_name) + "-" + str(start_direction)
        self.local_segment.append(MemorySegment(name, function_size, start_direction))
        start_direction += function_size
        self.next_function_segment.append(start_direction)

        var_tab = function_object[func_name]["vt"]
        vars = var_tab.variables
        # var_tab.print_VariableTable()

        for k, v in vars.items():
            self.insert_symbol_in_segment(name, v)
            # vars[k].print_symbol()
            # print("------------------------")

        return name

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

    def modify_address_symbol(self, array_acces, result_value):
        segment_name = array_acces.scope
        if segment_name == "Global Segment":
            return self.global_segment.modify_address(array_acces, result_value)

        # A symbol in constant segment arrive
        elif segment_name == "Constant Segment":
            return self.constant_segment.modify_address(array_acces, result_value)

        # A symbol in local segment arrive
        else:
            function_segment = self.__find_function_segment(segment_name)

            # The function was not found
            if function_segment == None:
                return False

            return function_segment.modify_address(array_acces, result_value)

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
            print("ERROR: Address greater than memory")
            sys.exit()

        # Direction is in Local Segment
        else:
            segment = self.__get_local_segment(direction)
            return segment.search_symbol(direction)

    def get_direction_value(self, direction):
        global_size = self.global_segment.size
        constant_size = self.constant_segment.size
        # Direction is in Global Segment
        if direction < global_size:
            return self.global_segment.search_value(direction)

        # Direction is in Constant Segment
        elif direction < global_size + constant_size:
            return self.constant_segment.search_value(direction)

        # Direction is bigger than memory
        elif direction > self.__total_size:
            print("ERROR: Address greater than memory")
            sys.exit()

        # Direction is in Local Segment
        else:
            segment = self.__get_local_segment(direction)
            return segment.search_value(direction)

    def modify_direction_value(self, direction, value):
        global_size = self.global_segment.size
        constant_size = self.constant_segment.size
        # Direction is in Global Segment
        if direction < global_size:
            self.global_segment.modify_value(direction, value)

        # Direction is in Constant Segment
        elif direction < global_size + constant_size:
            self.constant_segment.modify_value(direction, value)

        # Direction is bigger than memory
        elif direction > self.__total_size:
            print("ERROR: Address greater than memory")
            sys.exit()
        # Direction is in Local Segment
        else:
            segment = self.__get_local_segment(direction)
            segment.modify_value(direction, value)

    ################## FUNCTION CALL PREPARATION ##################

    def __save_local_scope(self, scope):
        f_name = scope[1]
        f_unique = scope[0]
        segment = self.__find_function_segment(f_unique)
        return segment.save_local_memory()

    def __unfreeze_local_scope(self, scope, frozen_memory):
        f_name = scope[1]
        f_unique = scope[0]
        segment = self.__find_function_segment(f_unique)
        segment.backtrack_memory(frozen_memory)

    def __erase_local_instance(self):
        local_segment = self.local_segment.pop()
        new_next = self.next_function_segment.pop()
        new_next = new_next - local_segment.size
        local_segment.erase_local_memory()
        self.next_function_segment.append(new_next)

    ########################### RESOLVE ###########################
    def __resolve_ver(self, dir_opnd_1, dir_opnd_2, dir_result):
        val_opnd_1 = self.get_direction_value(dir_opnd_1)
        val_opnd_2 = self.get_direction_value(dir_opnd_2)
        result = self.get_direction_value(dir_result)

        if val_opnd_1 == None or val_opnd_1 == "null":
            sym_opnd_1 = self.get_direction_symbol(dir_opnd_1).name
            print("ERROR: variable " + str(sym_opnd_1) + " has no assigned value")
            sys.exit()

        if val_opnd_2 == None or val_opnd_2 == "null":
            sym_opnd_2 = self.get_direction_symbol(dir_opnd_2).name
            print("ERROR: variable " + str(sym_opnd_2) + " has no assigned value")
            sys.exit()

        if not (val_opnd_1 >= val_opnd_2) and (val_opnd_1 <= result):
            print("ERROR: Trying to acces an index that is out of bounds")
            sys.exit()

    def __resolve_address_op(
        self, operation, dir_opnd_1, dir_opnd_2, dir_result, parent_name, index
    ):
        val_opnd_1 = self.get_direction_value(dir_opnd_1)
        parent = self.get_direction_symbol(dir_opnd_2)
        parent_dir = parent.segment_direction
        result = self.get_direction_symbol(dir_result)

        if val_opnd_1 == None or val_opnd_1 == "null":
            sym_opnd_1 = self.get_direction_symbol(dir_opnd_1).name
            print("ERROR: variable " + str(sym_opnd_1) + " has no assigned value")
            sys.exit()

        if dir_opnd_2 == None or parent_dir == None:
            print("ERROR: Variable " + str(parent.name) + " has not been declared")
            sys.exit()

        if operation == "ADD":
            result_value = val_opnd_1 + int(dir_opnd_2)
            child_dir = val_opnd_1 + int(parent_dir)
            result.value = result_value
            self.modify_direction_value(dir_result, result_value)
            array_acces = Symbol(
                str(parent_name) + "[ " + str(index) + " ]", parent.type, parent.scope
            )
            print
            self.modify_address_symbol(array_acces, child_dir)

    def __resolve_op(self, operation, dir_opnd_1, dir_opnd_2, dir_result):
        sym_opnd_1 = self.get_direction_symbol(dir_opnd_1)
        sym_opnd_2 = self.get_direction_symbol(dir_opnd_2)
        sym_result = self.get_direction_symbol(dir_result)

        type_op_1 = sym_opnd_1.type
        type_op_2 = sym_opnd_2.type
        val_opnd_1 = self.get_direction_value(dir_opnd_1)
        val_opnd_2 = self.get_direction_value(dir_opnd_2)

        if operation == "BEQ":
            result_value = val_opnd_1 == val_opnd_2
            sym_result.value = val_opnd_1 == val_opnd_2
        elif operation == "BNEQ":
            result_value = val_opnd_1 != val_opnd_2
            sym_result.value = val_opnd_1 != val_opnd_2
        elif operation == "OR":
            if val_opnd_1 == "null":
                val_opnd_1 = None
            if val_opnd_2 == "null":
                val_opnd_2 = None
            result_value = val_opnd_1 or val_opnd_2
            sym_result.value = val_opnd_1 or val_opnd_2
        elif operation == "AND":
            if val_opnd_1 == "null":
                val_opnd_1 = None
            if val_opnd_2 == "null":
                val_opnd_2 = None
            result_value = val_opnd_1 and val_opnd_2
            sym_result.value = val_opnd_1 and val_opnd_2
        else:
            if val_opnd_1 == None or val_opnd_1 == "null":
                sym_opnd_1 = sym_opnd_1.name
                print("ERROR: variable " + str(sym_opnd_1) + " has no assigned value")
                sys.exit()

            if val_opnd_2 == None or val_opnd_2 == "null":
                sym_opnd_2 = sym_opnd_2.name
                print("ERROR: variable " + str(sym_opnd_2) + " has no assigned value")
                sys.exit()

            if operation == "ADD":
                if type_op_1 == "STR" and type_op_2 == "STR":
                    if val_opnd_1[0] != val_opnd_2[0]:
                        val_opnd_2[-1] = val_opnd_1[-1]
                    result_value = val_opnd_1[:-1] + val_opnd_2[1:]
                    sym_result.value = val_opnd_1[:-1] + val_opnd_2[1:]
                else:
                    result_value = val_opnd_1 + val_opnd_2
                    sym_result.value = val_opnd_1 + val_opnd_2

            elif operation == "SUB":
                result_value = val_opnd_1 - val_opnd_2
                sym_result.value = val_opnd_1 - val_opnd_2
            elif operation == "MUL":
                result_value = val_opnd_1 * val_opnd_2
                sym_result.value = val_opnd_1 * val_opnd_2
            elif operation == "DIV":
                result_value = val_opnd_1 / val_opnd_2
                sym_result.value = val_opnd_1 / val_opnd_2
            elif operation == "MOD":
                result_value = val_opnd_1 % val_opnd_2
                sym_result.value = val_opnd_1 % val_opnd_2
            elif operation == "LT":
                result_value = val_opnd_1 < val_opnd_2
                sym_result.value = val_opnd_1 < val_opnd_2
            elif operation == "GT":
                result_value = val_opnd_1 > val_opnd_2
                sym_result.value = val_opnd_1 > val_opnd_2
            elif operation == "LTE":
                result_value = val_opnd_1 <= val_opnd_2
                sym_result.value = val_opnd_1 <= val_opnd_2
            elif operation == "GTE":
                result_value = val_opnd_1 >= val_opnd_2
                sym_result.value = val_opnd_1 >= val_opnd_2

        self.modify_direction_value(dir_result, result_value)

    def __resolve_eq(self, assign_op, dir_opnd, dir_result):
        val_operand = self.get_direction_value(dir_opnd)
        result = self.get_direction_symbol(dir_result)
        result_value = self.get_direction_value(dir_result)

        if assign_op != "EQ" and (val_operand == None or val_operand == "null"):
            sym_opnd = self.get_direction_symbol(dir_opnd).name
            print("ERROR: variable " + str(sym_opnd) + " has no assigned value")
            sys.exit()

        if assign_op != "EQ" and (result_value == None or result_value == "null"):
            result = result.name
            print("ERROR: variable " + str(result) + " has no assigned value")
            sys.exit()

        if assign_op == "EQ":
            result_value = val_operand
            result.value = val_operand
        elif assign_op == "ADDEQ":
            result_value += val_operand
            result.value += val_operand
        elif assign_op == "SUBEQ":
            result_value -= val_operand
            result.value -= val_operand
        elif assign_op == "MULEQ":
            result_value *= val_operand
            result.value *= val_operand
        elif assign_op == "DIVEQ":
            result_value /= val_operand
            result.value /= val_operand
        elif assign_op == "MODEQ":
            result_value %= val_operand
            result.value %= val_operand

        self.modify_direction_value(dir_result, result_value)

    def __resolve_not(self, dir_operand, dir_result):
        sym_operand = self.get_direction_symbol(dir_operand)
        val_operand = self.get_direction_value(dir_operand)
        result = self.get_direction_symbol(dir_result)
        if val_operand != None and val_operand != "null" and sym_operand.type != "BOOL":
            result_value = False
            result.value = False
        elif val_operand == None or val_operand == "null":
            result_value = True
            result.value = True
        else:
            result_value = not val_operand
            result.value = not val_operand

        self.modify_direction_value(dir_result, result_value)

    def __resolve_param(self, dir_operand, index_result, func_name):
        val_operand = self.get_direction_value(dir_operand)
        result = int(index_result) - 1
        real_func_name = func_name[1]
        memory_func_name = func_name[0]

        param_searching = self.func_table.functions[real_func_name]["p"]

        if result < 0 or result > len(param_searching):
            print(
                "ERROR: "
                + str(index_result)
                + " is not a valid parameter index for function "
                + str(real_func_name)
            )
            sys.exit()

        param_searching = param_searching[result].name
        param_in_vartable = self.func_table.functions[real_func_name]["vt"]
        param_in_vartable = param_in_vartable.variables[param_searching]

        self.modify_direction_value(param_in_vartable.global_direction, val_operand)
        param_in_vartable.value = val_operand

    def __resolve_return(self, dir_operand, dir_result):
        val_operand = self.get_direction_value(dir_operand)
        val_result = self.get_direction_symbol(dir_result)

        self.modify_direction_value(dir_result, val_operand)
        val_result.value = val_operand

    def __resolve_write(self, dir_result):
        if dir_result == "empty":
            print()
        else:
            result_value = self.get_direction_value(dir_result)
            print(result_value)

    # TODO: No lo he probado lo suficiente
    def __resolve_read(self, dir_result):
        user_input = input()
        symbol = self.get_direction_symbol(dir_result)

        if symbol.type == "INT":
            user_input = user_input.replace(" ", "")
            try:
                user_input = int(user_input)
            except:
                print("ERROR: Not a valid INT input")
                sys.exit()
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

        elif symbol.type == "FLT":
            user_input = user_input.replace(" ", "")
            try:
                user_input = float(user_input)
            except:
                print("ERROR: Not a valid FLT input")
                sys.exit()
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

        elif symbol.type == "CHAR":
            # TODO: Ver como validar que sea un solo char
            user_input = user_input.replace(" ", "")
            if len(user_input) > 1:
                print("ERROR: Not a valid CHAR input")
                sys.exit()
            try:
                user_input = str(user_input[0])
                user_input = "'" + user_input + "'"
            except:
                print("ERROR: Not a valid CHAR input")
                sys.exit()
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

        elif symbol.type == "STR":
            try:
                user_input = str(user_input)
                user_input = '"' + user_input + '"'

            except:
                print("ERROR: Not a valid STR input")
                sys.exit()
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

        elif symbol.type == "BOOL":
            user_input = user_input.replace(" ", "")
            booleans = {"true": True, "false": False, "0": False}
            if user_input not in booleans:
                try:
                    user_input = int(user_input)
                    user_input = True if user_input > 0 else False
                except:
                    print("ERROR: Not a valid BOOL input")
                    sys.exit()
            else:
                user_input = booleans[user_input]

            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

    def __resolve_frog_method(self, operation, dir_frog, dir_result):
        valid_hats = {
            '"cowboy"': 1,
            '"cool"': 2,
            '"shoes"': 3,
            '"makeup"': 4,
            "'cowboy'": 1,
            "'cool'": 2,
            "'shoes'": 3,
            "'makeup'": 4,
        }
        frog = self.get_direction_value(dir_frog)

        if operation == "hat":
            hat = self.get_direction_value(dir_result)
            if hat not in valid_hats:
                hat = 0
            else:
                hat = valid_hats[hat]
            return Instruction(frog, operation, hat)
        else:
            times = self.get_direction_value(dir_result)
            return Instruction(frog, operation, times)

    def __print_all_memory(self):
        self.global_segment.print_memory_segment()
        # self.constant_segment.print_memory_segment()
        for segment in self.local_segment:
            segment.print_memory_segment()

    def run(self, quad_dir):
        era = False
        running = True
        instruction = 1
        saved_positions = []
        saved_functions = []
        game_instructions = []
        frozen_memory = []
        index_accessed = []

        while running:
            curr_quad = quad_dir[instruction]
            operation = curr_quad.operator.name
            curr_type = curr_quad.operator.type
            # print("--index--: ",instruction)
            # self.__print_all_memory()
            # print("---------------")
            # print("---------------")
            # print()
            # print()
            if curr_type in ["operation", "comparison", "matching"]:
                if type(curr_quad.operand_2) == Symbol:

                    if curr_quad.operand_1.address_flag:
                        dir_opnd_1 = self.get_direction_symbol(
                            curr_quad.operand_1.value
                        )
                        dir_opnd_1 = dir_opnd_1.global_direction
                    else:
                        dir_opnd_1 = curr_quad.operand_1.global_direction

                    if curr_quad.operand_2.address_flag:
                        dir_opnd_2 = self.get_direction_symbol(
                            curr_quad.operand_2.value
                        )
                        dir_opnd_2 = dir_opnd_2.global_direction
                    else:
                        dir_opnd_2 = curr_quad.operand_2.global_direction

                    result_id = curr_quad.result_id

                    if len(saved_functions) > 0:
                        f = saved_functions[-1]
                        f_name = f[1]
                        f_address = f[0]
                    else:
                        f_name = ""
                        f_address = ""

                    if result_id.global_direction == None:
                        if result_id.scope == f_name:
                            self.insert_symbol_in_segment(f_address, result_id)
                        else:
                            self.insert_symbol_in_segment(result_id.scope, result_id)
                    # print("--------")
                    # print(operation)
                    # print(result_id.name)
                    # print(result_id.global_direction)
                    # print(curr_quad.operand_1.value)
                    # print(curr_quad.operand_2.value)

                    # print("--------")
                    dir_result = result_id.global_direction

                    self.__resolve_op(operation, dir_opnd_1, dir_opnd_2, dir_result)

                else:
                    dir_opnd_1 = curr_quad.operand_1.global_direction
                    dir_opnd_2 = curr_quad.operand_2.symbol.global_direction
                    parent_name = curr_quad.operand_2.parent
                    result_id = curr_quad.result_id
                    if len(saved_functions) > 0:
                        f = saved_functions[-1]
                        f_name = f[1]
                        f_address = f[0]
                    else:
                        f_name = ""
                        f_address = ""
                    if result_id.global_direction == None:
                        if result_id.scope == f_name:
                            self.insert_symbol_in_segment(f_address, result_id)
                        else:
                            self.insert_symbol_in_segment(result_id.scope, result_id)
                    dir_result = result_id.global_direction
                    self.__resolve_address_op(
                        operation,
                        dir_opnd_1,
                        dir_opnd_2,
                        dir_result,
                        parent_name,
                        index_accessed.pop(),
                    )

            elif operation in set.union(SemanticTable.assignment_operations_op, {"EQ"}):
                if operation == "EQ" and curr_quad.operand_1.name == "READ":
                    dir_result = curr_quad.result_id.global_direction
                    self.__resolve_read(dir_result)
                    if curr_quad.result_id.object_atr_flag:
                        game_instructions.append(
                            self.__resolve_frog_method(
                                "hat",
                                curr_quad.result_id.object_atr_flag.global_direction,
                                dir_result,
                            )
                        )
                else:
                    operand_1 = curr_quad.operand_1
                    result_id = curr_quad.result_id

                    if result_id.global_direction == None:
                        if len(saved_functions) > 0:
                            f = saved_functions[-1]
                            f_name = f[1]
                            f_address = f[0]
                        else:
                            f_name = ""
                            f_address = ""
                        if result_id.scope == f_name:
                            self.insert_symbol_in_segment(f_address, result_id)
                        else:
                            self.insert_symbol_in_segment(result_id.scope, result_id)

                    if result_id.address_flag:
                        dir_result = self.get_direction_symbol(result_id.value)
                        # print(result_id.name)
                        # print(dir_result.global_direction)
                        dir_result = dir_result.global_direction
                    else:
                        dir_result = result_id.global_direction

                    if operand_1.address_flag:
                        dir_operand = self.get_direction_symbol(operand_1.value)
                        dir_operand = dir_operand.global_direction
                    else:
                        dir_operand = operand_1.global_direction

                    self.__resolve_eq(operation, dir_operand, dir_result)

                    if result_id.object_atr_flag:
                        game_instructions.append(
                            self.__resolve_frog_method(
                                "hat",
                                result_id.object_atr_flag.global_direction,
                                dir_result,
                            )
                        )

            elif operation == "NOT":
                operand_1 = curr_quad.operand_1
                result_id = curr_quad.result_id

                if result_id.global_direction == None:
                    if len(saved_functions) > 0:
                        f = saved_functions[-1]
                        f_name = f[1]
                        f_address = f[0]
                    else:
                        f_name = ""
                        f_address = ""
                    if result_id.scope == f_name:
                        self.insert_symbol_in_segment(f_address, result_id)
                    else:
                        self.insert_symbol_in_segment(result_id.scope, result_id)

                if result_id.address_flag:
                    dir_result = self.get_direction_symbol(result_id.value)
                    dir_result = dir_result.global_direction
                else:
                    dir_result = result_id.global_direction

                if operand_1.address_flag:
                    dir_operand = self.get_direction_symbol(operand_1.value)
                    dir_operand = dir_operand.global_direction
                else:
                    dir_operand = operand_1.global_direction

                self.__resolve_not(dir_operand, dir_result)

            elif operation == "VER":
                if curr_quad.operand_1.address_flag:
                    dir_opnd_1 = self.get_direction_symbol(curr_quad.operand_1.value)
                    dir_opnd_1 = dir_opnd_1.global_direction
                else:
                    dir_opnd_1 = curr_quad.operand_1.global_direction

                dir_opnd_2 = curr_quad.operand_2.global_direction
                result_id = curr_quad.result_id.global_direction
                self.__resolve_ver(dir_opnd_1, dir_opnd_2, result_id)
                index_accessed.append(self.get_direction_value(dir_opnd_1))

            elif operation == "GOTO":
                instruction = curr_quad.result_id.name - 1

            elif operation == "GOTOF":
                if self.get_direction_value(curr_quad.operand_1.global_direction):
                    instruction += 1
                    continue
                else:
                    instruction = curr_quad.result_id.name
                continue

            elif operation == "ENDOF":
                running = False
                continue

            elif operation == "WRITE":
                if curr_quad.result_id:
                    if curr_quad.result_id.address_flag:
                        dir_result = self.get_direction_symbol(
                            curr_quad.result_id.value
                        )
                        dir_result = dir_result.global_direction
                    else:
                        dir_result = curr_quad.result_id.global_direction
                    self.__resolve_write(dir_result)
                else:
                    self.__resolve_write("empty")

            elif operation == "ERA":
                if curr_quad.operator.scope == "main" and not era:
                    saved_functions.append(["main", "main"])

                frozen_memory.append(self.__save_local_scope(saved_functions[-1]))
                function_name = curr_quad.operand_1.name
                name = self.__function_instance(function_name)
                saved_functions.append([name, function_name])
                era = True

            elif operation == "PARAM":
                if curr_quad.operand_1.address_flag:
                    print
                    dir_operand = self.get_direction_symbol(curr_quad.operand_1.value)
                    dir_operand = dir_operand.global_direction
                else:
                    dir_operand = curr_quad.operand_1.global_direction
                dir_result = curr_quad.result_id.name
                func_name = saved_functions[-1]
                self.__resolve_param(dir_operand, dir_result, func_name)

            elif operation == "GOSUB":
                function = curr_quad.operand_1.name
                saved_positions.append(instruction + 1)
                instruction = curr_quad.result_id.name
                continue

            elif operation == "RETURN":
                if curr_quad.operand_1 and curr_quad.result_id:
                    if curr_quad.operand_1.address_flag:
                        dir_operand = self.get_direction_symbol(
                            curr_quad.operand_1.value
                        )
                        dir_operand = dir_opnd_1.global_direction
                    else:
                        dir_operand = curr_quad.operand_1.global_direction
                    dir_result = curr_quad.result_id.global_direction
                    self.__resolve_return(dir_operand, dir_result)
                else:
                    instruction += 1
                    continue

            elif operation == "ENDFUNC":
                instruction = saved_positions.pop()
                self.__erase_local_instance()
                saved_functions.pop()
                self.__unfreeze_local_scope(saved_functions[-1], frozen_memory.pop())
                era = False
                continue

            elif curr_type == "obj_method":
                if curr_quad.operand_1.address_flag:
                    dir_frog = self.get_direction_symbol(curr_quad.operand_1.value)
                    dir_frog = dir_frog.global_direction
                else:
                    dir_frog = curr_quad.operand_1.global_direction

                dir_result = curr_quad.result_id.global_direction
                game_instructions.append(
                    self.__resolve_frog_method(operation, dir_frog, dir_result)
                )

            instruction += 1
            if instruction > len(quad_dir):
                running = False

        return game_instructions
