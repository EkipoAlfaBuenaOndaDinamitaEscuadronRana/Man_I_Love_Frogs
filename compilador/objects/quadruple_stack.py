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


class QuadrupleStack(object):
    # INICIALIZACIÓN
    # init
    def __init__(self):
        self.qstack = {}
        self.count_prev = 0
        self.count = 1
        self.jumpStack = []
        self.jumpStackR = []
        self.funcjump = {}
        self.param_count = 0
        self.temp_count = 1
        self.array_stack = []
        self.wait_to_call = []

    # para borrar el contendio cuando se empieza a leer un programa
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

    # INSERTAR / RESOLVER QUADRUPLOS
    # Insertar un quadruplo al stack
    def push_quad(self, quadruple, scope):
        quadruple.scope = scope
        self.qstack[self.count] = quadruple
        self.count_prev += 1
        self.count += 1

    # Para cuando los quadruplos vienen en lista
    def push_list(self, list, scope, ft):
        for elem in list:
            self.push_quad(modify_quad_object(elem, ft), scope)

    # Manda a resolver los quadruplos
    def solve_expression(self, expresion, ft):
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
        sol = Quadruple.arithmetic_expression(expresion, self.temp_count)
        if type(sol) == str:

            print(sol)
            sys.exit()
        else:
            self.get_last_temporal(sol, ft)
            return sol

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
                        ft.push_temporal(temp_obj)
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
                            ft.push_temporal(temp_obj)
                        temp = int(temp[2:-1])
                        if type(q.operand_2) == BaseAddress:
                            if temp >= self.temp_count:
                                self.temp_count = temp + 1
                            else:
                                flag = True

        if flag:
            self.temp_count += 1

    def array_access(self, symbol, scope, ft):
        # for k,v in symbol.items():
        #     print(k)
        #     if k == "dim":
        #         for e in v:
        #             print(get_symbol_formatted(e))

        #     else:
        #         print(get_symbol_formatted(v))

        # 1: ya se hizo, es en el ID validar que exista
        #    y que tenga dimensiones y asi

        # 2: En primer [
        #    inicializa DIM a 1
        #    PilaDim(id,DIM)
        #    get Node of Dim 1
        #    POper fake bottom

        DIM_COUNT = 1
        array_id = symbol["name"]
        DIM = symbol["dim"]
        if array_id.get_dimension_nodes_len() != len(DIM):
            print(
                'ERROR: wrong dimensions sent to variable "' + str(array_id.name) + '"'
            )
            sys.exit()

        # 3: despues de exp
        #    QUAD -> Ver exp LI LS
        #    if si hay un next node
        #    aux = exp
        #    QUAD -> * aux mdim tj
        #    pusho(tj)
        #    if dim > 1
        #    aux2 = pop o
        #    aux1 = pop p
        #    QUAD -> + aux1 aux2 Tk

        # 4: en la comma (entre dim)
        #    DIM++
        #    update dim en pila de DIM
        #    move to next node

        for d in DIM:
            if self.expresion_or_id(d, "INT", "index"):
                exp_sent = d[0]
                if exp_sent.type == "NULL":
                    print("ERROR: using a non-int value to try to access an array")
                    sys.exit()
            else:
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

                self.push_list(self.solve_expression(d, ft), scope, ft)
                exp_sent = self.qstack[self.count_prev].result_id
                if (
                    not Symbol.check_type_compatibility("INT", exp_sent.type)
                    or exp_sent.type == "NULL"
                ):
                    print("ERROR: using a non-int value to try to access an array")
                    sys.exit()
            limI = Symbol(
                array_id.dimension_nodes[DIM_COUNT]["LI"], "INT", "Constant Segment"
            )
            limS = Symbol(
                array_id.dimension_nodes[DIM_COUNT]["LS"], "INT", "Constant Segment"
            )
            ft.insert_to_constant_table([limI, limS])
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

            self.array_stack.append(exp_sent)
            if DIM_COUNT < len(DIM):
                temp = Symbol(str("T" + str(self.temp_count)), "INT", scope)
                ft.push_temporal(temp)

                m = Symbol(
                    int(array_id.dimension_nodes[DIM_COUNT]["M"]),
                    "INT",
                    "Constant Segment",
                )
                ft.insert_to_constant_table([m])

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
                self.temp_count += 1
                self.array_stack.append(self.qstack[self.count_prev].result_id)
            if DIM_COUNT > 1:
                aux_2 = self.array_stack.pop()
                aux_1 = self.array_stack.pop()
                temp = Symbol(str("T" + str(self.temp_count)), "INT", scope)
                ft.push_temporal(temp)
                self.push_quad(
                    modify_quad_object(
                        Quadruple(
                            Symbol("ADD", "operation", scope), aux_1, aux_2, temp
                        ),
                        ft,
                    ),
                    scope,
                )
                self.temp_count += 1
                self.array_stack.append(self.qstack[self.count_prev].result_id)
            DIM_COUNT += 1

        # 5: despues de que se acaba ]
        #    Aux1=pilaO.pop
        #    QUAD -> + aux1 K Ti
        #    + ti virtual addres Tn
        #    PilaO.Push((Tn))
        #    Pop Fake Botom
        aux_1 = self.array_stack.pop()
        temp = Symbol(str("T" + str(self.temp_count)), "INT", scope)
        ft.push_temporal(temp)
        m = Symbol(
            int(array_id.dimension_nodes[DIM_COUNT - 1]["M"]),
            "INT",
            "Constant Segment",
        )
        ft.insert_to_constant_table([m])
        self.push_quad(
            modify_quad_object(
                Quadruple(Symbol("ADD", "operation", scope), aux_1, m, temp), ft
            ),
            scope,
        )

        self.temp_count += 1
        self.array_stack.append(self.qstack[self.count_prev].result_id)
        aux_1 = self.array_stack.pop()
        temp = Symbol(
            "(" + str("T" + str(self.temp_count)) + ")", "INT", scope, address_flag=True
        )
        ft.push_temporal(temp)
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
        self.temp_count += 1
        self.array_stack.append(self.qstack[self.count_prev].result_id)

    # SET / GETS
    # Para poder guardar donde esta el inicio de una funcion
    def set_function_location(self, name):
        self.funcjump[name] = self.count

    # Para poder saber donde esta el inicio de una funcion
    def get_function_location(self, name):
        return Symbol(self.funcjump[name], "address", name)

    # Para cuando acabas de validar que sea el numero correcto
    # de parametros para la duncion actual
    def reset_param_count(self):
        self.param_count = 0

    def reset_temp_count(self):
        self.temp_count = 1

    # Para cuando saber el numero de parametros de entrada que
    # se estan mandando
    def get_param_count(self):
        return self.param_count

    # Funciones para diferentes estatutos y llenado de saltos
    # Funcion que valida tipos e identifica si se esta mandando una
    # constante / variable o una expresion
    def expresion_or_id(self, param, type, error_message):
        if len(param) == 1:
            param = param[0]
            if Symbol.check_type_compatibility(type, param.type):
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
            if Symbol.check_type_compatibility(
                type, self.qstack[self.count_prev].result_id.type
            ):
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

    # Regresa el quadruplo de parametros
    def validate_parameters(self, func_param, sent_param, scope):
        if self.param_count < len(func_param):
            current_func_param = func_param[self.param_count]
            if self.expresion_or_id(sent_param, current_func_param.type, "Parameter"):
                sent_param = sent_param[0]
                self.param_count += 1
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
                self.param_count += 1

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
            # esto es si no es un void
            find_return_symbol = ft.get_function_variable_table("Global Segment")
            find_return_symbol = find_return_symbol.get_var_symbol(scope)
            if self.expresion_or_id(exp, type, "Return"):
                exp = exp[0]
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
            # esto es si si es void
            self.push_quad(
                Quadruple(Symbol("RETURN", "VOID", scope), None, None, None), scope
            )

        self.push_quad(
            Quadruple(
                Symbol("GOTO", "instruction", scope), None, None, "MISSING_ADDRESS"
            ),
            scope,
        )
        self.jumpStackR.append(self.count_prev)

    def parche_guadalupano(self, func_var, scope, ft):
        if func_var.type != "VOID":
            temp = Symbol(str("T" + str(self.temp_count)), func_var.type, scope)
            ft.push_temporal(temp)

            self.push_quad(
                modify_quad_object(
                    Quadruple(Symbol("EQ", "assignment", scope), func_var, None, temp),
                    ft,
                ),
                scope,
            )
            self.temp_count += 1

    def write_quad(self, exp, scope):
        if len(exp) == 1:
            exp = exp[0]
        else:
            exp = self.qstack[self.count_prev].result_id
        a = Quadruple(Symbol("WRITE", "instruction", scope), None, None, exp)
        return a

    def read_quad(self, vars, scope):
        if len(vars) > 1:
            r = vars.pop(0)
            for v in vars:
                self.push_quad(
                    Quadruple(Symbol("EQ", "assignment", scope), r, None, v), scope
                )
        else:
            print("ERROR: Error in read asignation")
            sys.exit()

    def object_method_quad(self, data, scope, ft):
        if len(data) == 3:
            if data[2].type == "parentheses":
                s = Symbol(1, "INT", "Constant Segment")
                ft.insert_to_constant_table([s])
                self.push_quad(
                    modify_quad_object(Quadruple(data[1], data[0], None, s), ft),
                    scope,
                )
            else:
                if Symbol.check_type_compatibility("INT", data[2].type):
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

    # LLena el go to cuando se llega al final de una funcion
    def return_jump_fill(self, scope):
        if len(self.jumpStackR) > 0:
            if self.jumpStackR[-1] == self.count_prev:
                self.qstack.pop(self.count_prev)
                self.count_prev -= 1
                self.count -= 1
                self.jumpStackR.pop()

            while len(self.jumpStackR) > 0:
                end = self.jumpStackR.pop()
                self.fill(end, scope)

    # Para llenar el quadruplo de go to main
    def go_to_main(self, scope):
        end = self.jumpStack.pop()
        self.fill(end, scope)

    def ciclo_cero(self, scope, ft):
        if len(self.wait_to_call) > 0:
            self.push_list(
                self.solve_expression(
                    self.wait_to_call.pop(),
                    ft,
                ),
                scope,
                ft,
            )

    def ciclo_1(self):
        # Esta va antes de las expresiones del while
        self.jumpStack.append(self.count)

    def ciclo_2(self, scope):
        if not Symbol.check_type_compatibility(
            "BOOL", self.qstack[self.count_prev].result_id.type
        ):
            print("ERROR: Expresion in loop is not a boolean")
            sys.exit()
        else:
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

    def ciclo_3(self, scope):
        # Le avisa al inicio a donde ir si se acaba y al final a donde ir si sigue

        end = self.jumpStack.pop()
        ret = self.jumpStack.pop()
        self.push_quad(
            Quadruple(
                Symbol("GOTO", "instruction"), None, None, Symbol(ret, "address", scope)
            ),
            scope,
        )
        self.fill(end, scope)

    def if_1(self, scope):
        # ESTE VA DESPUES DEL COLON
        if not Symbol.check_type_compatibility(
            "BOOL", self.qstack[self.count_prev].result_id.type
        ):
            print("ERROR: Expresion in loop is not a boolean")
            sys.exit()
        else:
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

    def if_2(self, scope):
        # ESTE VA CUANDO SE CIERRAN EL IF TOTAL
        end = self.jumpStack.pop()
        self.fill(end, scope)

    def if_3(self, scope):
        # ESTE VA EN EL ELSE
        self.push_quad(
            Quadruple(
                Symbol("GOTO", "instruction", scope), None, None, "MISSING_ADDRESS"
            ),
            scope,
        )
        not_true = self.jumpStack.pop()
        self.jumpStack.append(self.count_prev)
        self.fill(not_true, scope)

    # Mete el address indicado en el go_to
    def fill(self, index, scope):
        if self.qstack[index].result_id == "MISSING_ADDRESS":
            self.qstack[index].result_id = Symbol(self.count, "address", scope)
        else:
            print("ERROR: Error filling jump quadruple")
            sys.exit()

    # Prints y returns
    def print_quad(self, q):
        print(get_quad_formatted(q))

    def print_quads(self):
        print(get_quad_stack_formatted(self.qstack))

    def get_qstack(self):
        return self.qstack

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

    def return_quads_test(self):
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
                + r"\n"
            )
        return rq
