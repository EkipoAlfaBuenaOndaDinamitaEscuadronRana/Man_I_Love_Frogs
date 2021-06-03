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

# CLASE VIRTUAL MACHINE
# Objeto que guarda segmentos de memoria y ejecuta cuadruplos


class VirtualMachine(object):

    ####################### INITS #######################

    def __init__(self, global_size, constant_size, local_size, func_table=None):
        self.__total_size = (
            global_size + constant_size + local_size
        )  # Guarda tamaño total de vm
        self.func_table = func_table  # Tabla de funciones
        self.global_segment = MemorySegment(
            "Global Segment", global_size, 0
        )  # Genera segmento de memoria global
        self.constant_segment = MemorySegment(
            "Constant Segment",
            constant_size,
            global_size,  # Genera segmento de memoria de constantes
        )
        self.declared_symbols = []  # Lista de simbolos en maquina virtual
        self.next_function_segment = (
            []
        )  # Guarda siguiente dirección de memoria disponible en segmento local

        if func_table:
            local_size_memory = global_size + constant_size
            # Guarda segmentos de memoria local
            self.local_segment = self.__build_local_segment(
                local_size, global_size + constant_size
            )
            # Guarda numero de segmentos en segmento local
            self.local_functions = len(self.local_segment)
            # Mete los datos de la tabla de funciones a memoria
            self.__func_table_assign_memory()

        else:
            self.local_segment = None
            self.local_functions = 0

    # Genera memoria local
    def __build_local_segment(
        self,
        local_size,
        local_start_direction,
    ):
        # Revisa cuantas funciones hay y divide los segmentos locales entre ello
        num_local_segments = len(self.func_table.functions)
        if not num_local_segments:
            return []

        # Genera direcciones de inicio de segmento local y tamaño de cada uno
        local_segment_size = local_size // num_local_segments
        local_memory_size = local_size // num_local_segments
        start_direction = local_start_direction

        # Crea segmento de memoria del main
        segments = []
        segments.append(MemorySegment("main", local_segment_size, start_direction))
        # Guarda sigueinte dirección disponible y la guarda
        start_direction += local_memory_size
        self.next_function_segment.append(start_direction)
        # Regresa lista de segmentos de memoria con segmento de memoria del main
        return segments

    # Mete las tablas de variables a su segmento de memoria
    def __func_table_assign_memory(self):
        functions = self.func_table.functions
        tables_init = ["Global Segment", "Constant Segment", "main"]
        # Para el segmento global, constante y el main
        for ft in functions:
            if ft in tables_init:
                # Saca su tabla de variables
                var_tab = functions[ft]["vt"]
                # Saca el diccionario de simbolos en la tabla
                vars = var_tab.variables
                # Inserta cada simbolo en la tabla a su segmento
                for k, v in vars.items():
                    self.insert_symbol_in_segment(ft, v)

    # Genera segmento de memoria de función para instancia de función
    def __function_instance(self, func_name):
        function_object = self.func_table.functions

        # Saca su tamaño de la tabla y lo multiplica por el numero de tipos de variables
        function_size = function_object[func_name]["s"] * 7

        # Se saca la dirección de inicio
        start_direction = self.next_function_segment.pop()

        # Valida que hay espacio en la memoria local para instanciar la función
        if function_size + start_direction < self.__total_size:
            # Se genera el nombre unico de la instancia
            # Se agrega su segmento de memoria al segmento local
            name = str(func_name) + "-" + str(start_direction)
            self.local_segment.append(
                MemorySegment(name, function_size, start_direction)
            )

            # Se actualiza la dirección de inicio del siguiente segmento de memoria
            start_direction += function_size
            self.next_function_segment.append(start_direction)

            # Consigue simbolos en tabla de variables de la función
            var_tab = function_object[func_name]["vt"]
            vars = var_tab.variables

            # Inserta las variables al segmento de memoria
            for k, v in vars.items():
                self.insert_symbol_in_segment(name, v)

            # Regresa nombre unico
            return name
        else:
            print("ERROR: Local Memory exceded, can't instance " + func_name)
            sys.exit()

    # Busca una función en el segmento local
    def __find_function_segment(self, func_name):
        for func_segment in self.local_segment:

            if func_segment.name == func_name:
                return func_segment

        return None

    # Inserta un simbolo en el segmento indicado
    def insert_symbol_in_segment(self, segment_name, symbol):
        self.declared_symbols.append(symbol)

        # Si el segmento es el global
        if segment_name == "Global Segment":
            return self.global_segment.insert_symbol(symbol)

        # Si el segmento es el constante
        elif segment_name == "Constant Segment":
            return self.constant_segment.insert_symbol(symbol)

        # Busca en el segmento local
        else:
            function_segment = self.__find_function_segment(segment_name)

            # The function was not found
            if function_segment == None:
                return False
            # Inserta a memoria
            return function_segment.insert_symbol(symbol)

    # Cuando se genera la dirección del indice de un arreglo
    def modify_address_symbol(self, array_access, result_value):
        # Inserta en segmento global
        segment_name = array_access.scope
        if segment_name == "Global Segment":
            return self.global_segment.modify_address(array_access, result_value)

        # Inserta en segmento constante
        elif segment_name == "Constant Segment":
            return self.constant_segment.modify_address(array_access, result_value)

        # Busca en el segmento local
        else:
            function_segment = self.__find_function_segment(segment_name)

            # The function was not found
            if function_segment == None:
                return False
            # Inserta simbolo a dirección indicada
            return function_segment.modify_address(array_access, result_value)

    # Regresa segmento de memoria al que le pertenece esa dirección
    def __get_local_segment(self, direction):
        current_segment_direction = (
            self.global_segment.size + self.constant_segment.size
        )
        for func in self.local_segment:

            func_size = func.size + func.initial_position - 1
            if direction <= func_size:
                return func

    # Regresa el simbolo en una dirección
    def get_direction_symbol(self, direction):
        global_size = self.global_segment.size
        constant_size = self.constant_segment.size
        # Direction en Global Segment
        if direction < global_size:
            return self.global_segment.search_symbol(direction)

        # Direction en Constant Segment
        elif direction < global_size + constant_size:
            return self.constant_segment.search_symbol(direction)

        # Direction excede tamaño de memoria
        elif direction > self.__total_size:
            print("ERROR: Address excedes memory size")
            sys.exit()

        # Direction en Local Segment
        else:
            segment = self.__get_local_segment(direction)
            return segment.search_symbol(direction)

    # Regresa el valor en una dirección
    def get_direction_value(self, direction):
        global_size = self.global_segment.size
        constant_size = self.constant_segment.size
        # Direction en Global Segment
        if direction < global_size:
            return self.global_segment.search_value(direction)

        # Direction en Constant Segment
        elif direction < global_size + constant_size:
            return self.constant_segment.search_value(direction)

        # Direction excede tamaño de memoria
        elif direction > self.__total_size:
            print("ERROR: Address excedes memory size")
            sys.exit()

        # Direction en Local Segment
        else:
            segment = self.__get_local_segment(direction)
            return segment.search_value(direction)

    # Modifica el valor en una dirección de memoria
    def modify_direction_value(self, direction, value):
        global_size = self.global_segment.size
        constant_size = self.constant_segment.size
        # Direction en Global Segment
        if direction < global_size:
            self.global_segment.modify_value(direction, value)

        # Direction en Constant Segment
        elif direction < global_size + constant_size:
            self.constant_segment.modify_value(direction, value)

        # Direction excede tamaño de memoria
        elif direction > self.__total_size:
            print("ERROR: Address excedes memory size")
            sys.exit()
        # Direction en Local Segment
        else:
            segment = self.__get_local_segment(direction)
            segment.modify_value(direction, value)

    ################## FUNCTION CALL PREPARATION ##################

    # Regresa un diccionario con valores de variables en segmento actual
    def __save_local_scope(self, scope):
        f_name = scope[1]
        f_unique = scope[0]
        segment = self.__find_function_segment(f_unique)
        return segment.save_local_memory()

    # Regresa los valores guardados a su dirección
    def __unfreeze_local_scope(self, scope, frozen_memory):
        f_name = scope[1]
        f_unique = scope[0]
        segment = self.__find_function_segment(f_unique)
        segment.backtrack_memory(frozen_memory)

    # Borra un segmento de memoria cuando termina de usarse
    def __erase_local_instance(self):
        # Saca el segmento de memoria de la lista
        local_segment = self.local_segment.pop()
        # Saca el valor de la siguiente dirección
        new_next = self.next_function_segment.pop()
        # Cambia la siguiente dirección a la nueva
        new_next = new_next - local_segment.size
        # Borra memoria local
        local_segment.erase_local_memory()
        # Guarda nueva dirección
        self.next_function_segment.append(new_next)

    ########################### RESOLVE ###########################

    # ......................... ARREGLOS ......................... #

    # Resuelve cuadruplo de instrucción VER
    def __resolve_ver(self, dir_opnd_1, dir_opnd_2, dir_result):
        # Valor en dirección de indice a accesar
        val_opnd_1 = self.get_direction_value(dir_opnd_1)

        # Valor en dirección de limite inferior
        val_opnd_2 = self.get_direction_value(dir_opnd_2)

        # Valor en dirección de limite inferior
        result = self.get_direction_value(dir_result)

        # Se valida que el indice tenga un valor
        if val_opnd_1 == None or val_opnd_1 == "null":
            sym_opnd_1 = self.get_direction_symbol(dir_opnd_1).name
            print("ERROR: variable " + str(sym_opnd_1) + " has no assigned value")
            sys.exit()

        # Se valida que se hayan encontrado los valores de los limites
        if (
            val_opnd_2 == None
            or val_opnd_2 == "null"
            or result == None
            or val_opnd_2 == "null"
        ):
            print("ERROR: array missing dimension value")
            sys.exit()

        # Se valida que el valor del indice este entre los limites
        if not (val_opnd_1 >= val_opnd_2) and (val_opnd_1 <= result):
            print("ERROR: Trying to acces an index that is out of bounds")
            sys.exit()

    # Resuelve la operación de agregar el desplazamiento a la dirección base
    def __resolve_address_op(
        self, operation, dir_opnd_1, dir_opnd_2, dir_result, parent_name, index
    ):
        # Valor de desplazamiento
        val_opnd_1 = self.get_direction_value(dir_opnd_1)
        # Simbolo del arreglo
        parent_sym = self.get_direction_symbol(dir_opnd_2)
        # Dirección en segmento del padre
        parent_dir = parent_sym.segment_direction
        # Simbolo que guarda la dirección
        result = self.get_direction_symbol(dir_result)

        # Valida que haya valores asignados a las variables
        if val_opnd_1 == None or val_opnd_1 == "null":
            sym_opnd_1 = self.get_direction_symbol(dir_opnd_1).name
            print("ERROR: variable " + str(sym_opnd_1) + " has no assigned value")
            sys.exit()

        if dir_opnd_2 == None or parent_dir == None:
            print("ERROR: Variable " + str(parent_sym.name) + " has not been declared")
            sys.exit()

        # Valida que sea una suma
        if operation == "ADD":
            # Dirección global + desplazamiento
            result_value = val_opnd_1 + int(dir_opnd_2)
            # Dirección de segmento + desplazamiento
            child_dir = val_opnd_1 + int(parent_dir)
            # Modifica valor de simbolo y valor en tabla para variable que guarda dirección
            result.value = result_value
            self.modify_direction_value(dir_result, result_value)
            # Crea el simbolo del indice del arreglo
            array_access = Symbol(
                str(parent_name) + "[ " + str(index) + " ]",
                parent_sym.type,
                parent_sym.scope,
            )
            # Inserta simbolo de indice a memoria
            self.modify_address_symbol(array_access, child_dir)

    # ......................... FUNCIONES ......................... #

    # Resuelve la asignación a parametros
    def __resolve_param(self, dir_operand, index_result, func_name):
        # Parametro que se manda
        val_operand = self.get_direction_value(dir_operand)
        # Indice de parametro que se busca
        result = int(index_result) - 1
        real_func_name = func_name[1]
        memory_func_name = func_name[0]

        # Busca la lista de parametros en la tabla
        param_searching = self.func_table.functions[real_func_name]["p"]

        # Se valida que el indice que buscamos este en la lista
        if result < 0 or result > len(param_searching):
            print(
                "ERROR: "
                + str(index_result)
                + " is not a valid parameter index for function "
                + str(real_func_name)
            )
            sys.exit()

        # Agarra el nombre del parametro y lo busca en la tabla de variables
        param_searching = param_searching[result].name
        param_in_vartable = self.func_table.functions[real_func_name]["vt"]
        param_in_vartable = param_in_vartable.variables[param_searching]

        # Modifica el valor del parametro al valor que se mando
        self.modify_direction_value(param_in_vartable.global_direction, val_operand)
        param_in_vartable.value = val_operand

    # Asigna valor de retorno a la variable de la función en la tabla global
    def __resolve_return(self, dir_operand, dir_result):
        val_operand = self.get_direction_value(dir_operand)
        val_result = self.get_direction_symbol(dir_result)

        self.modify_direction_value(dir_result, val_operand)
        val_result.value = val_operand

    # ......................... OPERACIONES ......................... #

    # Resuelve operaciones aritmeticas y booleanas
    def __resolve_op(self, operation, dir_opnd_1, dir_opnd_2, dir_result):
        sym_opnd_1 = self.get_direction_symbol(dir_opnd_1)
        sym_opnd_2 = self.get_direction_symbol(dir_opnd_2)
        sym_result = self.get_direction_symbol(dir_result)

        type_op_1 = sym_opnd_1.type
        type_op_2 = sym_opnd_2.type
        val_opnd_1 = self.get_direction_value(dir_opnd_1)
        val_opnd_2 = self.get_direction_value(dir_opnd_2)

        # Hace operaciones en las que no es necesario tener un valor en operando
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
            # Valida que los operandos tengan valor
            if val_opnd_1 == None or val_opnd_1 == "null":
                sym_opnd_1 = sym_opnd_1.name
                print("ERROR: variable " + str(sym_opnd_1) + " has no assigned value")
                sys.exit()

            if val_opnd_2 == None or val_opnd_2 == "null":
                sym_opnd_2 = sym_opnd_2.name
                print("ERROR: variable " + str(sym_opnd_2) + " has no assigned value")
                sys.exit()

            if type_op_1 == "CHAR" and (type_op_2 == "INT" or type_op_2 == "FLT"):
                val_opnd_1 = ord(val_opnd_1[1])
            elif type_op_2 == "CHAR" and (type_op_1 == "INT" or type_op_1 == "FLT"):
                val_opnd_2 = ord(val_opnd_2[1])

            # +
            if operation == "ADD":
                # Suma entre strings quita los "" que los separan
                if type_op_1 == "STR" and type_op_2 == "STR":
                    if val_opnd_1[0] != val_opnd_2[0]:
                        val_opnd_2[-1] = val_opnd_1[-1]
                    result_value = val_opnd_1[:-1] + val_opnd_2[1:]
                    sym_result.value = val_opnd_1[:-1] + val_opnd_2[1:]
                else:

                    result_value = val_opnd_1 + val_opnd_2
                    sym_result.value = val_opnd_1 + val_opnd_2
            # -
            elif operation == "SUB":
                result_value = val_opnd_1 - val_opnd_2
                sym_result.value = val_opnd_1 - val_opnd_2
            # *
            elif operation == "MUL":
                result_value = val_opnd_1 * val_opnd_2
                sym_result.value = val_opnd_1 * val_opnd_2
            # /
            elif operation == "DIV":
                if val_opnd_2 == 0:
                    print("ERROR: Trying to divide by cero")
                    sys.exit()
                result_value = val_opnd_1 / val_opnd_2
                sym_result.value = val_opnd_1 / val_opnd_2
            # %
            elif operation == "MOD":
                if val_opnd_2 == 0:
                    print("ERROR: Trying to divide by cero")
                    sys.exit()
                result_value = val_opnd_1 % val_opnd_2
                sym_result.value = val_opnd_1 % val_opnd_2
            # <
            elif operation == "LT":
                result_value = val_opnd_1 < val_opnd_2
                sym_result.value = val_opnd_1 < val_opnd_2
            # >
            elif operation == "GT":
                result_value = val_opnd_1 > val_opnd_2
                sym_result.value = val_opnd_1 > val_opnd_2
            # <=
            elif operation == "LTE":
                result_value = val_opnd_1 <= val_opnd_2
                sym_result.value = val_opnd_1 <= val_opnd_2
            # >=
            elif operation == "GTE":
                result_value = val_opnd_1 >= val_opnd_2
                sym_result.value = val_opnd_1 >= val_opnd_2

        # Modifica valor en dirección resultante
        self.modify_direction_value(dir_result, result_value)

    # Resuelve operaciones de asignación y asignación compuesta
    def __resolve_eq(self, assign_op, dir_opnd, dir_result):
        val_operand = self.get_direction_value(dir_opnd)
        result = self.get_direction_symbol(dir_result)
        result_value = self.get_direction_value(dir_result)

        # Valida que el las variables tengan valores si es asignación compuesta
        if assign_op != "EQ" and (val_operand == None or val_operand == "null"):
            sym_opnd = self.get_direction_symbol(dir_opnd).name
            print("ERROR: variable " + str(sym_opnd) + " has no assigned value")
            sys.exit()

        if assign_op != "EQ" and (result_value == None or result_value == "null"):
            result = result.name
            print("ERROR: variable " + str(result) + " has no assigned value")
            sys.exit()

        # =
        if assign_op == "EQ":
            result_value = val_operand
            result.value = val_operand
        # +=
        elif assign_op == "ADDEQ":
            result_value += val_operand
            result.value += val_operand
        # -=
        elif assign_op == "SUBEQ":
            result_value -= val_operand
            result.value -= val_operand
        # *=
        elif assign_op == "MULEQ":
            result_value *= val_operand
            result.value *= val_operand
        # /=
        elif assign_op == "DIVEQ":
            # Valida que no se pueda divir por cero
            if val_operand == 0:
                print("ERROR: Trying to divide by cero")
                sys.exit()
            result_value /= val_operand
            result.value /= val_operand
        # %=
        elif assign_op == "MODEQ":
            # Valida que no se pueda dividir por cero
            if val_operand == 0:
                print("ERROR: Trying to divide by cero")
                sys.exit()
            result_value %= val_operand
            result.value %= val_operand

        # Modifica valor resultante de variable receptora
        self.modify_direction_value(dir_result, result_value)

    # Resuelve operaciones de NOT
    def __resolve_not(self, dir_operand, dir_result):
        sym_operand = self.get_direction_symbol(dir_operand)
        val_operand = self.get_direction_value(dir_operand)
        result = self.get_direction_symbol(dir_result)
        # Si el operando tiene un valor no booleano el not es falso
        if (
            val_operand != None
            and val_operand != "null"
            and sym_operand.type != "BOOL"
            and val_operand != 0
        ):
            result_value = False
            result.value = False
        # Si el valor es None, null ó 0 el not es verdadero
        elif val_operand == None or val_operand == "null" or val_operand == 0:
            result_value = True
            result.value = True
        else:
            # Si ya es booleano se hace el not a su valor
            result_value = not val_operand
            result.value = not val_operand

        # Se guarda el valor del resultado
        self.modify_direction_value(dir_result, result_value)

    # ......................... INPUT / OUTPUT ......................... #

    # Imprime expresión que se busca
    def __resolve_write(self, dir_result):
        if dir_result == "empty":
            print()
        else:
            result_value = self.get_direction_value(dir_result)
            print(result_value)

    # Asigna input de usuario a dirección
    def __resolve_read(self, dir_result):
        user_input = input()
        symbol = self.get_direction_symbol(dir_result)

        # Si se busca asignar a un INT intenta convertirlo a INT y asignarlo
        if symbol.type == "INT":
            user_input = user_input.replace(" ", "")
            try:
                user_input = int(user_input)
            except:
                print("ERROR: Not a valid INT input")
                sys.exit()
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

        # Si se busca asignar a un FLT intenta convertirlo a FLT y asignarlo
        elif symbol.type == "FLT":
            user_input = user_input.replace(" ", "")
            try:
                user_input = float(user_input)
            except:
                print("ERROR: Not a valid FLT input")
                sys.exit()
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

        # Si se busca asignar a un CHAR valida que sea un solo caracter,
        # convertirlo a STR y asignar solo la primera casilla del input
        elif symbol.type == "CHAR":
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
        # Si se busca asignar a un STR se busca convertir a string, agregarle comillas y asignarlo
        elif symbol.type == "STR":
            try:
                user_input = str(user_input)
                user_input = '"' + user_input + '"'

            except:
                print("ERROR: Not a valid STR input")
                sys.exit()
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input
        # Si es un BOOL
        elif symbol.type == "BOOL":
            user_input = user_input.replace(" ", "")
            booleans = {"true": True, "false": False, "0": False}
            # Se valida que el input sea true, false o cero,
            if user_input not in booleans:
                # Si el valor no esta en el diccionario de BOOL se intenta validar
                # que sea un INT y si es > 0 se asigna TRUE
                try:
                    user_input = int(user_input)
                    user_input = True if user_input > 0 else False
                except:
                    print("ERROR: Not a valid BOOL input")
                    sys.exit()
            else:
                user_input = booleans[user_input]
            # Se asigna valor
            self.modify_direction_value(dir_result, user_input)
            symbol.value = user_input

    # ......................... MTD OBJ ......................... #

    def __resolve_frog_method(self, operation, dir_frog, dir_result):
        # Diccionario de accesorios de rana
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
        # Se busca el valor / nombre del objeto
        frog = self.get_direction_value(dir_frog)

        # Si la operaicón es de cambiar atributo
        if operation == "hat":
            # Valida que este en diccionario y si no es el default
            hat = self.get_direction_value(dir_result)
            if hat not in valid_hats:
                hat = 0
            else:
                hat = valid_hats[hat]
            # Regresa instrucción
            return Instruction(frog, operation, hat)
        else:
            # Regresa instrucción de operando
            times = self.get_direction_value(dir_result)
            return Instruction(frog, operation, times)

    ########################### MAIN ###########################

    # Imprime la memoria para debugging
    def __print_all_memory(self):
        self.global_segment.print_memory_segment()
        self.constant_segment.print_memory_segment()
        for segment in self.local_segment:
            segment.print_memory_segment()

    # Itera sobre los quadruplos y resuelve la instrucción
    def run(self, quad_dir):

        era = False  # Avisa si estamos llamando a una función
        running = True  # Lee mientras no lleguemos al ENDOF
        instruction = 1  # Inicia en el primer cuadruplo
        saved_positions = []  # Guarda indice cuando se llama una función
        saved_functions = (
            []
        )  # Stack con nombre de función y nombre unico de su espacio de meoria
        game_instructions = []  # Guarda las instrucciones del juego
        frozen_memory = (
            []
        )  # Guarda diccionario de direcciones + su valor antes de hacer llamada
        index_accessed = []  # Guarda indice de dimension a accesar

        # Mientras no sea ENDOF
        while running:
            # Saca cuadruplo en dirección actual y el nombre / tipo del operando
            curr_quad = quad_dir[instruction]
            operation = curr_quad.operator.name
            curr_type = curr_quad.operator.type

            # Si es una expresión aritmetica o booleana
            if curr_type in ["operation", "comparison", "matching"]:
                # Si es una expresión normal
                if type(curr_quad.operand_2) == Symbol:
                    # Checa si el operando_1 es una dirección
                    if curr_quad.operand_1.address_flag:
                        # Si es el caso busca el valor en la dirección
                        dir_opnd_1 = self.get_direction_symbol(
                            curr_quad.operand_1.value
                        )
                        dir_opnd_1 = dir_opnd_1.global_direction
                    else:
                        # Si no solo asigna su dirección
                        dir_opnd_1 = curr_quad.operand_1.global_direction

                    # Checa si el operando_2 es una dirección
                    if curr_quad.operand_2.address_flag:
                        # Si es el caso busca el valor en la dirección
                        dir_opnd_2 = self.get_direction_symbol(
                            curr_quad.operand_2.value
                        )
                        dir_opnd_2 = dir_opnd_2.global_direction
                    else:
                        # Si no solo asigna su dirección
                        dir_opnd_2 = curr_quad.operand_2.global_direction

                    # Agarra simbolo de resultado
                    result_id = curr_quad.result_id

                    # Si el simbolo no tiene dirección de memoria
                    if result_id.global_direction == None:
                        if len(saved_functions) > 0:
                            # Busca nombre del contexto actual
                            f = saved_functions[-1]
                            f_name = f[1]
                            f_address = f[0]
                        else:
                            f_name = ""
                            f_address = ""
                        # si la variable es del scope de la función actual
                        if result_id.scope == f_name:
                            # Se inserta en segmento actual
                            self.insert_symbol_in_segment(f_address, result_id)
                        else:
                            # Se inserta en su propio scope
                            self.insert_symbol_in_segment(result_id.scope, result_id)
                    # Consigue su dirección
                    dir_result = result_id.global_direction
                    # Resuelve operación
                    self.__resolve_op(operation, dir_opnd_1, dir_opnd_2, dir_result)
                # Cuando la operación tiene un BASE ADDRESS como operando
                else:
                    # Dirección operando de desplazamiento
                    dir_opnd_1 = curr_quad.operand_1.global_direction
                    # Dirección de simbolo padre de dirección base
                    dir_opnd_2 = curr_quad.operand_2.symbol.global_direction
                    # Nombre del simbolo padre de la dirección base
                    parent_name = curr_quad.operand_2.parent
                    # Agarra simbolo de resultado
                    result_id = curr_quad.result_id

                    # Si el simbolo no tiene dirección de memoria
                    if result_id.global_direction == None:
                        if len(saved_functions) > 0:
                            # Busca nombre del contexto actual
                            f = saved_functions[-1]
                            f_name = f[1]
                            f_address = f[0]
                        else:
                            f_name = ""
                            f_address = ""
                        # si la variable es del scope de la función actual
                        if result_id.scope == f_name:
                            # Se inserta en segmento actual
                            self.insert_symbol_in_segment(f_address, result_id)
                        else:
                            # Se inserta en su propio scope
                            self.insert_symbol_in_segment(result_id.scope, result_id)
                    # Consigue su dirección
                    dir_result = result_id.global_direction
                    # Resuelve operación de dirección
                    self.__resolve_address_op(
                        operation,
                        dir_opnd_1,
                        dir_opnd_2,
                        dir_result,
                        parent_name,
                        index_accessed.pop(),
                    )
            # Si es una expresión de asignación o asignación compuesta
            elif operation in set.union(SemanticTable.assignment_operations_op, {"EQ"}):
                # Si estamos haciendo un read lo llama
                if operation == "EQ" and curr_quad.operand_1.name == "READ":
                    dir_result = curr_quad.result_id.global_direction
                    self.__resolve_read(dir_result)
                    # Si estamos asignando a un atributo objeto
                    if curr_quad.result_id.object_atr_flag:
                        # Genera instrucción
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

                    # Si el simbolo no tiene dirección de memoria
                    if result_id.global_direction == None:
                        if len(saved_functions) > 0:
                            # Busca nombre del contexto actual
                            f = saved_functions[-1]
                            f_name = f[1]
                            f_address = f[0]
                        else:
                            f_name = ""
                            f_address = ""
                        # si la variable es del scope de la función actual
                        if result_id.scope == f_name:
                            # Se inserta en segmento actual
                            self.insert_symbol_in_segment(f_address, result_id)
                        else:
                            # Se inserta en su propio scope
                            self.insert_symbol_in_segment(result_id.scope, result_id)

                    # Checa si el resultado es una dirección
                    if result_id.address_flag:
                        # Si es el caso busca el valor en la dirección
                        dir_result = self.get_direction_symbol(result_id.value)
                        dir_result = dir_result.global_direction
                    else:
                        # Si no solo asigna su dirección
                        dir_result = result_id.global_direction

                    # Checa si el operando_1 es una dirección
                    if operand_1.address_flag:
                        # Si es el caso busca el valor en la dirección
                        dir_operand = self.get_direction_symbol(operand_1.value)
                        dir_operand = dir_operand.global_direction
                    else:
                        # Si no solo asigna su dirección
                        dir_operand = operand_1.global_direction

                    # Resuelve operación
                    self.__resolve_eq(operation, dir_operand, dir_result)
                    # Si estamos asignando a un atributo objeto
                    if result_id.object_atr_flag:
                        # Genera instrucción
                        game_instructions.append(
                            self.__resolve_frog_method(
                                "hat",
                                result_id.object_atr_flag.global_direction,
                                dir_result,
                            )
                        )
            # Si es una expresión de not
            elif operation == "NOT":
                operand_1 = curr_quad.operand_1
                result_id = curr_quad.result_id
                # Si el simbolo no tiene dirección de memoria
                if result_id.global_direction == None:
                    if len(saved_functions) > 0:
                        # Busca nombre del contexto actual
                        f = saved_functions[-1]
                        f_name = f[1]
                        f_address = f[0]
                    else:
                        f_name = ""
                        f_address = ""
                    # si la variable es del scope de la función actual
                    if result_id.scope == f_name:
                        # Se inserta en segmento actual
                        self.insert_symbol_in_segment(f_address, result_id)
                    else:
                        # Se inserta en su propio scope
                        self.insert_symbol_in_segment(result_id.scope, result_id)

                # Checa si el resultado es una dirección
                if result_id.address_flag:
                    # Si es el caso busca el valor en la dirección
                    dir_result = self.get_direction_symbol(result_id.value)
                    dir_result = dir_result.global_direction
                else:
                    # Si no solo asigna su dirección
                    dir_result = result_id.global_direction

                # Checa si el operando_1 es una dirección
                if operand_1.address_flag:
                    # Si es el caso busca el valor en la dirección
                    dir_operand = self.get_direction_symbol(operand_1.value)
                    dir_operand = dir_operand.global_direction
                else:
                    # Si no solo asigna su dirección
                    dir_operand = operand_1.global_direction
                # Resuelve operación
                self.__resolve_not(dir_operand, dir_result)
            # Si es una operación write
            elif operation == "WRITE":
                # Si no es un write sin expresión
                if curr_quad.result_id.name != "empty":
                    # Checa si el resultado es una dirección
                    if curr_quad.result_id.address_flag:
                        # Si es el caso busca el valor en la dirección
                        dir_result = self.get_direction_symbol(
                            curr_quad.result_id.value
                        )
                        dir_result = dir_result.global_direction
                    else:
                        # Si no solo asigna su dirección
                        dir_result = curr_quad.result_id.global_direction
                    # Resuelve operación
                    self.__resolve_write(dir_result)
                else:
                    # Resuelve operación
                    self.__resolve_write(curr_quad.result_id.name)
            # Si es una instrucción GOTO
            elif operation == "GOTO":
                # Nos movemos al cuadruplo de ese indice
                instruction = curr_quad.result_id.name
                continue
            # Si es una instrucción GOTOF
            elif operation == "GOTOF":
                # Si la expresión es verdadera avanzamos uno
                if self.get_direction_value(curr_quad.operand_1.global_direction):
                    instruction += 1
                    continue
                else:
                    # Si no vamos al cuadruplo del indice
                    instruction = curr_quad.result_id.name
                continue
            # Si es una instrucción VER
            elif operation == "VER":
                # Checa si el operando_1 es una dirección
                if curr_quad.operand_1.address_flag:
                    # Si es el caso busca el valor en la dirección
                    dir_opnd_1 = self.get_direction_symbol(curr_quad.operand_1.value)
                    dir_opnd_1 = dir_opnd_1.global_direction
                else:
                    # Si no solo asigna su dirección
                    dir_opnd_1 = curr_quad.operand_1.global_direction

                dir_opnd_2 = curr_quad.operand_2.global_direction
                result_id = curr_quad.result_id.global_direction
                # Resuelve instrucción
                self.__resolve_ver(dir_opnd_1, dir_opnd_2, result_id)
                # Guarda el valor del indice a accesar
                index_accessed.append(self.get_direction_value(dir_opnd_1))
            # Si es una instrucción VER
            elif operation == "ERA":
                # Si estamos en main y no hay una llamada activa
                if curr_quad.operator.scope == "main" and not era:
                    # Guarda main como el scope anterior
                    saved_functions.append(["main", "main"])
                # Agrega los valores en memoria actuales a la memoria congelada
                frozen_memory.append(self.__save_local_scope(saved_functions[-1]))
                # Sacamos el nombre de la función
                function_name = curr_quad.operand_1.name
                # Generamos su espacio de memoria
                name = self.__function_instance(function_name)
                # Guardamos el nombre de la función y el nombre de su scope
                saved_functions.append([name, function_name])
                # Indicamos inicio de llamada
                era = True
            # si es una instrucción PARAM
            elif operation == "PARAM":
                # Checa si el operando_1 es una dirección
                if curr_quad.operand_1.address_flag:
                    # Si es el caso busca el valor en la dirección
                    dir_operand = self.get_direction_symbol(curr_quad.operand_1.value)
                    dir_operand = dir_operand.global_direction
                else:
                    # Si no solo asigna su dirección
                    dir_operand = curr_quad.operand_1.global_direction
                # Saca el indice del parametro que queremos accesar
                dir_result = curr_quad.result_id.name
                # Sacamos los datos de la función que se esta llamando
                func_name = saved_functions[-1]
                # Asignamos valores a parametro
                self.__resolve_param(dir_operand, dir_result, func_name)
            # Instrucción de tipo GOSUB
            elif operation == "GOSUB":
                # Guarda la posición a la que se regresa dspues de la llamada
                saved_positions.append(instruction + 1)
                # Va al indice de la función
                instruction = curr_quad.result_id.name
                continue
            # Instrucción de tipo RETURN
            elif operation == "RETURN":
                # Si existe valor de retorno
                if curr_quad.operand_1 and curr_quad.result_id:
                    # Checa si el operando_1 es una dirección
                    if curr_quad.operand_1.address_flag:
                        # Si es el caso busca el valor en la dirección
                        dir_operand = self.get_direction_symbol(
                            curr_quad.operand_1.value
                        )
                        dir_operand = dir_opnd_1.global_direction
                    else:
                        # Si no solo asigna su dirección
                        dir_operand = curr_quad.operand_1.global_direction
                    # Saca la dirección de la variable de la función
                    dir_result = curr_quad.result_id.global_direction
                    # Resuelve asignación
                    self.__resolve_return(dir_operand, dir_result)
                else:
                    # Si es VOID pasamos a la siguiente instrucción
                    instruction += 1
                    continue
            # Instrucción de tipo ENDFUNC
            elif operation == "ENDFUNC":
                # Cambia el indice a la posición que guardamos
                instruction = saved_positions.pop()
                # Borra instancia local
                self.__erase_local_instance()
                # Saca la función del stack de llamadas
                saved_functions.pop()
                # Vuelve a asignar los valores que congelamos de la instancia anterior
                self.__unfreeze_local_scope(saved_functions[-1], frozen_memory.pop())
                # Indica que se acabo la llamada
                era = False
                continue
            # Insutrucción tipo METODO OBJETO
            elif curr_type == "obj_method":
                # Checa si el operando_1 es una dirección
                if curr_quad.operand_1.address_flag:
                    # Si es el caso busca el valor en la dirección
                    dir_frog = self.get_direction_symbol(curr_quad.operand_1.value)
                    dir_frog = dir_frog.global_direction
                else:
                    # Si no solo asigna su dirección
                    dir_frog = curr_quad.operand_1.global_direction

                dir_result = curr_quad.result_id.global_direction
                # Genera instrucción
                game_instructions.append(
                    self.__resolve_frog_method(operation, dir_frog, dir_result)
                )
            # Acaba la iteración de cuadruplos
            elif operation == "ENDOF":
                running = False
                continue
            # Se mueve a la siguiente instrucción
            instruction += 1
            # Valida que sea valida y si no acaba
            if instruction > len(quad_dir):
                running = False
        # Regresa instrucciónes acumuladas al juego
        return game_instructions
