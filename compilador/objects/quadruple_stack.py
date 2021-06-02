from typing import SupportsComplex
from router_solver import *
import compilador.objects.quadruple
from compilador.objects.quadruple import *
import compilador.objects.base_address
from compilador.objects.base_address import *
import compilador.helpers.helper_functions
from compilador.helpers.helper_functions import *
import re
import sys


# CLASE QUADRUPLE STACK
# Objeto que guarda stack de quadruplos y sus indices


class QuadrupleStack(object):
    ####################### INITS #######################

    def __init__(self):
        self.qstack = {}  # Diccionario con indices y cuadruplos
        self.count_prev = 0  # Contador con valor real de indice
        self.count = 1  # Contador que siempre va un paso adelante
        self.jumpStack = []  # Lista de indices para rellenar direcciones
        self.jumpStackR = []  # Lista de indices para rellenar direcciones en return
        self.funcjump = {}  # Diccionario con nombre de función e indice de inicio
        self.param_count = 0  # Conteo de parametros siendo procesados
        self.temp_count = 1  # Contador de temporales
        self.array_stack = []  # Stack de temporales con dirección resultante de arreglo
        self.wait_to_call = []  # Guarda lista de simbolos que todavia no se procesasn

    # Reinica los valores para cuando compilan cosas consecutivamente
    def reset_quad(self):
        self.qstack = {}
        self.count_prev = 0
        self.count = 1
        self.jumpStack = []
        self.jumpStackR = []
        self.funcjump = {}
        self.param_count = 0
        self.temp_count = 1
        self.array_stack = []

    # Reinica el contador de parametros al terminar validación
    def reset_param_count(self):
        self.param_count = 0

    # Reinicia el contador de temporales cuando cambiamos de contexto
    def reset_temp_count(self):
        self.temp_count = 1

    ####################### PUSH #######################

    # Agrega un cuadruplo al stack
    def push_quad(self, quadruple, scope):
        quadruple.scope = scope
        self.qstack[self.count] = quadruple
        self.count_prev += 1
        self.count += 1

    # Recibe una lista de cuaruplos y los agrega al stack
    def push_list(self, list, scope, ft):
        for elem in list:
            self.push_quad(modify_quad_object(elem, ft), scope)

    ####################### SETS / GETS #######################

    # Guarda el indice de inicio de una función
    def set_function_location(self, name):
        self.funcjump[name] = self.count

    # Regresa el indice de inicio de una función
    def get_function_location(self, name):
        return Symbol(self.funcjump[name], "address", name)

    # Regresa el contador actual de parametros
    def get_param_count(self):
        return self.param_count

    ####################### QUADRUPLE OPERATIONS #######################

    # Recibe lista de simbolos y manda a resolver la expresión
    def solve_expression(self, expresion, ft):
        # Revisa si se reciben datos en formato dimensionado y lo cambia
        # por el simbolo en el que se guarda el acceso a ese dato
        i = len(expresion) - 1
        while i > -1:
            if expresion[i].is_dimensioned():
                if (i > 0 and expresion[i - 1].name != "OSB") or i == 0:
                    stack = []
                    count = i
                    arr_name = expresion[count]
                    expresion[count] = self.array_stack.pop()
                    count += 1
                    for x in range(arr_name.get_dimension_size()):
                        stack.append(expresion[count])
                        expresion.pop(count)
                        while count >= 0 and count < len(expresion) and len(stack) > 0:
                            if expresion[count].name == "OSB":
                                stack.append(expresion[count])
                            elif expresion[count].name == "CSB":
                                stack.pop()
                            expresion.pop(count)
            i -= 1
        # Llama a resolver la expresión a los cuadruplos
        sol = Quadruple.arithmetic_expression(expresion, self.temp_count)

        # Si recibe un error lo imprime y termina la ejecución
        if type(sol) == str:
            print(sol)
            sys.exit()
        else:
            # Cambia el valor del conteo de temporales al ultimo temporal
            self.get_last_temporal(sol, ft)
            return sol

    # Busca el valor del ultimo temporal en el stack
    def get_last_temporal(self, list, ft):
        r = r"T(\d+)"
        r2 = r"\(T(\d+)\)"
        flag = False

        for q in list:
            temp_obj = q.result_id
            temp = q.result_id.name
            result = re.match(r, temp)
            if result:
                if result.start() == 0 and result.end() == (len(str(temp))):
                    if not ft.lookup_temporal(temp_obj):
                        ft.set_temporal(temp_obj)
                    temp = int(temp[1:])
                    if temp >= self.temp_count:
                        self.temp_count = temp + 1
                    else:
                        flag = True
            else:
                result = re.match(r2, temp)
                if result:
                    if result.start() == 0 and result.end() == (len(str(temp))):
                        if not ft.lookup_temporal(temp_obj):
                            ft.set_temporal(temp_obj)
                        temp = int(temp[2:-1])
                        if type(q.operand_2) == BaseAddress:
                            if temp >= self.temp_count:
                                self.temp_count = temp + 1
                            else:
                                flag = True

        if flag:
            self.temp_count += 1

    # Generación de cuaruplos de acceso a arreglos
    def array_access(self, symbol, scope, ft):
        # 1: ya se hizo, es en el ID validar que exista
        #    y que tenga dimensiones

        # 2: Al llegar a primera dimension

        # Inicializa DIM_COUNT a 1
        DIM_COUNT = 1
        #    Agarra nombre variable dimensionada
        array_id = symbol["name"]

        # Agarra los datos de las dimensiones y valida que sea igual a las
        # dimensiones de la variable que se llamo
        DIM = symbol["dim"]
        if array_id.get_dimension_size() != len(DIM):
            print(
                'ERROR: wrong dimensions sent to variable "' + str(array_id.name) + '"'
            )
            sys.exit()

        # Para cada dimensión del arrelglo
        for d in DIM:
            # Valida que lo que se mando sea un INT
            # Cuando es solo un valor
            if self.expresion_or_id(d, "INT", "index"):
                exp_sent = d[0]
                if exp_sent.type == "NULL":
                    print("ERROR: using a non-int value to try to access an array")
                    sys.exit()
            else:
                # Cuando es una expresión
                # Si hay dimensiones las resuelve
                # Si hay expresion la resuelve
                i = 0
                while i < len(d):
                    count = i
                    if d[i].is_dimensioned():
                        stack = []
                        array_content = []
                        array_content.append(d[count])
                        count += 1
                        stack.append(d[count])
                        while len(stack) > 0 and count < len(d):
                            if d[count].name == "OSB":
                                stack.append(d[count])
                            elif d[count].name == "CSB":
                                stack.pop()
                            array_content.append(d[count])
                            count += 1
                        self.array_access(
                            format_array_dimensions(array_content), scope, ft
                        )
                    i += count + 1
                # Manda a resolver el cuadruplo
                self.push_list(self.solve_expression(d, ft), scope, ft)
                # Asigna el valor del resultado del ultimo cuadruplo
                exp_sent = self.qstack[self.count_prev].result_id
                # Valida que sea de tipo INT
                if (
                    not Symbol.check_type_compatibility("INT", exp_sent.type)
                    or exp_sent.type == "NULL"
                ):
                    print("ERROR: using a non-int value to try to access an array")
                    sys.exit()
            # Agarra los limites del nodo de dimensiones de la dimension
            limI = Symbol(
                array_id.dimension_nodes[DIM_COUNT]["LI"], "INT", "Constant Segment"
            )
            limS = Symbol(
                array_id.dimension_nodes[DIM_COUNT]["LS"], "INT", "Constant Segment"
            )
            # Los mete a la tabla de constantes
            ft.insert_to_constant_table([limI, limS])

            # 3: despues de leer expresión

            # Genera cuadruplo VER con expresion que se mando y limites
            self.push_quad(
                modify_quad_object(
                    Quadruple(
                        Symbol("VER", "instructions", scope),
                        exp_sent,
                        limI,
                        limS,
                    ),
                    ft,
                ),
                scope,
            )

            # Se guarda la expresión que se mando
            self.array_stack.append(exp_sent)

            # Si hay otra dimensión
            if DIM_COUNT < len(DIM):
                temp = Symbol(str("T" + str(self.temp_count)), "INT", scope)
                ft.set_temporal(temp)
                # Saca la M de la dimensión
                m = Symbol(
                    int(array_id.dimension_nodes[DIM_COUNT]["M"]),
                    "INT",
                    "Constant Segment",
                )
                ft.insert_to_constant_table([m])

                # Genera cuadruplo de expresion * Mn
                self.push_quad(
                    modify_quad_object(
                        Quadruple(
                            Symbol("MUL", "operation", scope),
                            self.array_stack.pop(),
                            m,
                            temp,
                        ),
                        ft,
                    ),
                    scope,
                )
                # Indica que se agrego un temporal y se agrega el resultado
                # para agregar el offset al resultado de la otra dimensión
                self.temp_count += 1
                self.array_stack.append(self.qstack[self.count_prev].result_id)
            # Si no es la primera dimensión
            if DIM_COUNT > 1:
                aux_2 = self.array_stack.pop()
                aux_1 = self.array_stack.pop()
                temp = Symbol(str("T" + str(self.temp_count)), "INT", scope)
                ft.set_temporal(temp)
                # Genera cuadruplo de (expresion_anterior * Mn-1) + expresion actual
                self.push_quad(
                    modify_quad_object(
                        Quadruple(
                            Symbol("ADD", "operation", scope), aux_1, aux_2, temp
                        ),
                        ft,
                    ),
                    scope,
                )
                # Indica que se genero un temporal
                self.temp_count += 1
                # Guarda resultado de dimensión
                self.array_stack.append(self.qstack[self.count_prev].result_id)
            # 4 : Al llegar a otra dimension
            # Pasa a la siguiente dimension
            DIM_COUNT += 1

        # 5: al acabar de leer las dimensiones
        # Agarra expresión acumulada
        aux_1 = self.array_stack.pop()
        temp = Symbol(str("T" + str(self.temp_count)), "INT", scope)
        ft.set_temporal(temp)

        # Se le agrega K que en nuestro caso siempre es 0
        m = Symbol(
            int(array_id.dimension_nodes[DIM_COUNT - 1]["M"]),
            "INT",
            "Constant Segment",
        )
        ft.insert_to_constant_table([m])

        # Genera cuadruplo de expresion acumulada + K
        self.push_quad(
            modify_quad_object(
                Quadruple(Symbol("ADD", "operation", scope), aux_1, m, temp), ft
            ),
            scope,
        )

        # Indica que generamos otro temporal
        self.temp_count += 1
        # Se agrega el resultado a la pila y se saca
        self.array_stack.append(self.qstack[self.count_prev].result_id)
        aux_1 = self.array_stack.pop()

        # Se genera cuadruplo de desplazamiento + dirección base
        temp = Symbol(
            "(" + str("T" + str(self.temp_count)) + ")",
            "INT",
            scope,
            address_flag=array_id.type,
        )
        ft.set_temporal(temp)
        self.push_quad(
            modify_quad_object(
                Quadruple(
                    Symbol("ADD", "operation", scope),
                    aux_1,
                    BaseAddress(
                        str(str(array_id.name) + "-BA"),
                        array_id,
                        array_id.name,
                        array_id.type,
                        array_id.scope,
                        array_id.address[0],
                    ),
                    temp,
                ),
                ft,
            ),
            scope,
        )
        # Se indica que se genero un temporal
        self.temp_count += 1
        # Se guarda el valor resultante en la pila
        self.array_stack.append(self.qstack[self.count_prev].result_id)

    # Funcion que valida tipos e identifica si se esta mandando una
    # constante / variable o una expresion
    def expresion_or_id(self, param, type, error_message):
        # Si la expresión solo es de un dato
        if len(param) == 1:
            param = param[0]
            # Valida si es una dirección y si si compara con el tipo
            # del objeto al que apunta y no su propio
            if param.address_flag:
                param = param.address_flag
            else:
                param = param.type
            # Valida compatibilidad de tipos
            if Symbol.check_type_compatibility(type, param):
                return True
            else:

                print(
                    "ERROR: "
                    + error_message
                    + " sent isn't same type as "
                    + error_message
                    + " declared"
                )
                sys.exit()
        else:
            # Si es una expresión checa el resultado del ultimo cuadruplo
            # Valida si es una dirección y si si compara con el tipo
            # del objeto al que apunta y no su propio
            if self.qstack[self.count_prev].result_id.address_flag:
                exp = self.qstack[self.count_prev].result_id.address_flag
            else:
                exp = self.qstack[self.count_prev].result_id.type
            # Valida compatibilidad de tipos
            if Symbol.check_type_compatibility(type, exp):
                return False
            else:
                print(
                    "ERROR: "
                    + error_message
                    + " sent isn't same type as "
                    + error_message
                    + " declared"
                )
                sys.exit()

    # Regresa el cuadruplo de parametros
    def validate_parameters(self, func_param, sent_param, scope):
        # Valida que no hayamos contado más parametros de los que
        # tiene la función
        if self.param_count < len(func_param):
            # Agarra el parametro en el indice que buscamos
            current_func_param = func_param[self.param_count]
            # Si es un id
            if self.expresion_or_id(sent_param, current_func_param.type, "Parameter"):
                # Lo saca de la lista, incrementa conteo de parametros
                sent_param = sent_param[0]
                self.param_count += 1
                # Regresa cuadruplo de parametros
                return Quadruple(
                    Symbol("PARAM", sent_param.type, scope),
                    sent_param,
                    None,
                    Symbol(
                        self.param_count,
                        current_func_param.type,
                        current_func_param.scope,
                    ),
                )
            else:
                # Si es una expresión agarra el resultado del último cuadruplo
                self.param_count += 1
                # Regresa cuadruplo de parametros
                return Quadruple(
                    Symbol("PARAM", self.qstack[self.count_prev].result_id.type, scope),
                    self.qstack[self.count_prev].result_id,
                    None,
                    Symbol(
                        self.param_count,
                        current_func_param.type,
                        current_func_param.scope,
                    ),
                )

        else:
            print("ERROR: sent a numer of parameters greater than declared")
            sys.exit()

    # Crea el quadruplo de return
    def return_in_function(self, type, scope, exp=None, ft=None):
        if exp:
            # Si busca regresar una expresión
            # Busca el simbolo su variable en la tabla de variables global
            find_return_symbol = ft.get_function_variable_table("Global Segment")
            find_return_symbol = find_return_symbol.get_var_symbol(scope)
            # Si es un id
            if self.expresion_or_id(exp, type, "Return"):
                # Lo saca de la lista
                exp = exp[0]
                # Genera e incerta el cuadruplo de return con el valor
                self.push_quad(
                    modify_quad_object(
                        Quadruple(
                            Symbol("RETURN", exp.type, scope),
                            exp,
                            None,
                            find_return_symbol,
                        ),
                        ft,
                    ),
                    scope,
                )
            else:
                # Si es una expresión
                # Genera e inserta el cuadruplo con el valor de retorno del
                # cuadruplo anterior
                self.push_quad(
                    modify_quad_object(
                        Quadruple(
                            Symbol(
                                "RETURN",
                                self.qstack[self.count_prev].result_id.type,
                                scope,
                            ),
                            self.qstack[self.count_prev].result_id,
                            None,
                            find_return_symbol,
                        ),
                        ft,
                    ),
                    scope,
                )
        else:
            # Si la función es VOID
            # Genera cuadruplo con return vacio
            self.push_quad(
                Quadruple(Symbol("RETURN", "VOID", scope), None, None, None), scope
            )
        # Genera cuadruplo de GOTO para ir a ENDFUNC
        self.push_quad(
            Quadruple(
                Symbol("GOTO", "instruction", scope), None, None, "MISSING_ADDRESS"
            ),
            scope,
        )
        # Guarda el indice de GOTO para rellenar cuando acabemos de leer la función
        self.jumpStackR.append(self.count_prev)

    # Cuando se llama una función
    def parche_guadalupano(self, func_var, scope, ft):
        # Valida que la función deba de regresar algo
        if func_var.type != "VOID":
            temp = Symbol(str("T" + str(self.temp_count)), func_var.type, scope)
            ft.set_temporal(temp)
            # Agrega cuadruplo para asignar valor del valor que tiene
            # la variable de la función en la tabla global
            # y lo asigna a un temporal para no perder el resultado
            self.push_quad(
                modify_quad_object(
                    Quadruple(Symbol("EQ", "assignment", scope), func_var, None, temp),
                    ft,
                ),
                scope,
            )
            # Indica que se genero un temporal
            self.temp_count += 1

    # Cuaderuplo de write
    def write_quad(self, scope, exp=None):
        # Si se manda una expresión
        if exp != None:
            # Valida si es un id o o la expresión
            if len(exp) == 1:
                # Si es un solo dato lo saca de la lista
                exp = exp[0]
            else:
                # Si es una expresión agarra el resultado del cudaruplo anterior
                exp = self.qstack[self.count_prev].result_id
        else:
            # Si no hay expresión y es un write vacio se llena con empty
            exp = Symbol("empty", "STR", scope)
        # Regresa cuadruplo de write
        return Quadruple(Symbol("WRITE", "instruction", scope), None, None, exp)

    # Cuadruplo de read
    def read_quad(self, vars, scope):
        # Valida que se haya mandado el valor al que asignaremos el read
        if len(vars) > 1:
            # Saca el simbolo de read
            r = vars.pop(0)
            # Por cada simbolo en la lista
            for v in vars:
                # Genera un cuadruplo e asignación tipo read
                self.push_quad(
                    Quadruple(Symbol("EQ", "assignment", scope), r, None, v), scope
                )
        else:
            print("ERROR: Error in read asignation")
            sys.exit()

    # Cuadruplos de metodos de objeto
    def object_method_quad(self, data, scope, ft):
        # Si se mandan datos validos
        if len(data) == 3:
            # Si no se mando un valor de movimientos
            if data[2].type == "parentheses":
                s = Symbol(1, "INT", "Constant Segment")
                ft.insert_to_constant_table([s])
                # Genera e incerta cuadruplo de un solo movimiento
                self.push_quad(
                    modify_quad_object(Quadruple(data[1], data[0], None, s), ft),
                    scope,
                )
            else:
                # Valida que se mando un entero
                if Symbol.check_type_compatibility("INT", data[2].type):
                    # Genera e incerta cuadruplo con numero de movimientos
                    self.push_quad(
                        modify_quad_object(
                            Quadruple(data[1], data[0], None, data[2]), ft
                        ),
                        scope,
                    )
                else:
                    print("ERROR: Error parameter in object method not INT type")
                    sys.exit()
        else:
            print("ERROR: Error in object method call")
            sys.exit()

    ####################### PUNTOS NEURALGICOS #######################
    # Rellena el cuadruplo GOTO con el indice de inicio del main
    def go_to_main(self, scope):
        end = self.jumpStack.pop()
        self.fill(end, scope)

    # Genera cuadruplos para for simple
    def for_simple(self, exp, scope, ft):
        # Checa si se manda un solo dato o una expresión
        if self.expresion_or_id(exp, "INT", "Times"):
            exp = exp[0]
        else:
            exp = self.qstack[self.count_prev].result_id
        s = Symbol(0, "INT", "Constant Segment")
        ft.insert_to_constant_table([s])
        # Se genera temporal que va a guardar el conteo de iteraciones
        temp_reuse = Symbol(str("T" + str(self.temp_count)), "INT", scope)
        ft.set_temporal(temp_reuse)
        # Genera e incerta cuadruplo inicialización de variable temporal con cero
        self.push_quad(
            modify_quad_object(
                Quadruple(Symbol("EQ", "assignment", scope), s, None, temp_reuse), ft
            ),
            scope,
        )
        self.temp_count += 1
        # Llama primer punto neuralgico
        self.ciclo_1()
        temp = Symbol(str("T" + str(self.temp_count)), "BOOL", scope)
        ft.set_temporal(temp)
        # Genera e incerta cuadruplo de comparaicón de contador con la expresión que se mando
        self.push_quad(
            modify_quad_object(
                Quadruple(Symbol("LT", "comparison", scope), temp_reuse, exp, temp), ft
            ),
            scope,
        )
        self.temp_count += 1
        # Llama segundo punto neuralgico
        self.ciclo_2(scope)
        s = Symbol(1, "INT", "Constant Segment")
        ft.insert_to_constant_table([s])
        # Guarda el incremento al temporal para ponerlo al final del ciclo
        self.wait_to_call.append(
            modify_quad_object(
                Quadruple(Symbol("ADDEQ", "assignment", scope), s, None, temp_reuse), ft
            )
        )

    # Saca la asignación guardada
    def ciclo_cero(self, scope, ft):
        # Genera y/o incerta el cuadruplo de incremento al final
        # del bloque del ciclo
        if len(self.wait_to_call) > 0:
            call = self.wait_to_call.pop()
            if type(call) == Quadruple:
                self.push_quad(call, scope)
            else:
                self.push_list(
                    self.solve_expression(
                        call,
                        ft,
                    ),
                    scope,
                    ft,
                )

    # Se guarda el indice del inicio del ciclo para indicar en un GOTO después
    def ciclo_1(self):
        self.jumpStack.append(self.count)

    # Valida que la expresión sea de tipo BOOL
    def ciclo_2(self, scope):
        if not Symbol.check_type_compatibility(
            "BOOL", self.qstack[self.count_prev].result_id.type
        ):
            print("ERROR: Expresion in loop is not a boolean")
            sys.exit()
        else:
            # Genera e incerta cuadruplo de GOTOF y guarda si indice
            # para rellenar cuando llegue al final del bloque
            result = self.qstack[self.count_prev].result_id
            self.push_quad(
                Quadruple(
                    Symbol("GOTOF", "instruction", scope),
                    result,
                    None,
                    "MISSING_ADDRESS",
                ),
                scope,
            )
            self.jumpStack.append(self.count_prev)

    # Rellena direciónes y genera GOTO al inicio del ciclo
    def ciclo_3(self, scope):
        # Saca el valor del indice inicio, genera e incerta el cuadruplo de GOTO
        end = self.jumpStack.pop()
        ret = self.jumpStack.pop()
        self.push_quad(
            Quadruple(
                Symbol("GOTO", "instruction"), None, None, Symbol(ret, "address", scope)
            ),
            scope,
        )
        # Rellena el GOTOF con el indice del final del ciclo
        self.fill(end, scope)

    # Validación para despues de leer expresión de condicional
    def if_1(self, scope):
        # Revisa que la expresión sea booleana
        if not Symbol.check_type_compatibility(
            "BOOL", self.qstack[self.count_prev].result_id.type
        ):
            print("ERROR: Expresion in loop is not a boolean")
            sys.exit()
        else:
            # Genera e incerta el cuadruplo de GOTOF para ir al siguiente bloque o al final
            result = self.qstack[self.count_prev].result_id
            self.push_quad(
                Quadruple(
                    Symbol("GOTOF", "instruction", scope),
                    result,
                    None,
                    "MISSING_ADDRESS",
                ),
                scope,
            )
            # Guarda su indice
            self.jumpStack.append(self.count_prev)

    # Rellena ultimo GOTOF con el valor del final de la expresión
    def if_2(self, scope):
        end = self.jumpStack.pop()
        self.fill(end, scope)

    # Genera cuadruplo cuando la condicional tiene else
    def if_3(self, scope):
        # Genera cuadruplo de GOTO para cuando la expresión es verdadera ir al final
        self.push_quad(
            Quadruple(
                Symbol("GOTO", "instruction", scope), None, None, "MISSING_ADDRESS"
            ),
            scope,
        )
        # Rellena cuadruplo de GOTOF para indicar donde comienza siguiente condicional
        not_true = self.jumpStack.pop()
        # Guarda indice de GOTO a rellenar con el indice del fin de la expresión
        self.jumpStack.append(self.count_prev)
        self.fill(not_true, scope)

    # LLena el go to cuando se llega al final de una funcion
    def return_jump_fill(self, scope):
        # Checa si hay return por rellenar
        if len(self.jumpStackR) > 0:
            # Checa si el return esta seguido al ENDFUNC
            # si es el caso borra el GOTO porque es redundante
            if self.jumpStackR[-1] == self.count_prev:
                self.qstack.pop(self.count_prev)
                self.count_prev -= 1
                self.count -= 1
                self.jumpStackR.pop()
            # Rellena todos los GOTO despues del return con indice de ENDFUNC
            while len(self.jumpStackR) > 0:
                end = self.jumpStackR.pop()
                self.fill(end, scope)

    # Mete el indice actual al cuadruplo del inidce indicado
    def fill(self, index, scope):
        if self.qstack[index].result_id == "MISSING_ADDRESS":
            self.qstack[index].result_id = Symbol(self.count, "address", scope)
        else:
            print("ERROR: Error filling jump quadruple")
            sys.exit()

    ####################### PRINTS #######################

    # Imprime un cuadruplo individual
    def print_quad(self, q):
        print(get_quad_formatted(q))

    # Imprime todo el stack de cuadruplos
    def print_quads(self):
        print(get_quad_stack_formatted(self.qstack))

    # Regresa los cuadruplos en formato string
    def return_quads(self):
        rq = ""
        for k, v in self.qstack.items():
            rq += (
                str(int(k)).zfill(2)
                + " | "
                + str(
                    "-"
                    if v.operator == None
                    else (
                        v.operator.name
                        if (
                            type(v.operator) == Symbol
                            or type(v.operator) == BaseAddress
                        )
                        else v.operator
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_1 == None
                    else (
                        v.operand_1.name
                        if (
                            type(v.operand_1) == Symbol
                            or type(v.operand_1) == BaseAddress
                        )
                        else v.operand_1
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_2 == None
                    else (
                        v.operand_2.name
                        if (
                            type(v.operand_2) == Symbol
                            or type(v.operand_2) == BaseAddress
                        )
                        else v.operand_2
                    )
                )
                + " "
                + str(
                    "-"
                    if v.result_id == None
                    else (
                        v.result_id.name
                        if (
                            type(v.result_id) == Symbol
                            or type(v.result_id) == BaseAddress
                        )
                        else v.result_id
                    )
                )
                + "\n"
            )
        return rq
