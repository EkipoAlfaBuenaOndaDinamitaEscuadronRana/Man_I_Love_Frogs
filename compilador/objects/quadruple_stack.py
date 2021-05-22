from typing import SupportsComplex
from router_solver import *
import compilador.objects.quadruple
from compilador.objects.quadruple import *
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
        self.temp_count = 0

    # para borrar el contendio cuando se empieza a leer un programa
    def reset_quad(self):
        self.qstack = {}
        self.count_prev = 0
        self.count = 1
        self.jumpStack = []
        self.jumpStackR = []
        self.funcjump = {}
        self.param_count = 0
        self.temp_count = 0

    # INSERTAR / RESOLVER QUADRUPLOS
    # Insertar un quadruplo al stack
    def push_quad(self, quadruple, scope):
        quadruple.scope = scope
        self.qstack[self.count] = quadruple
        self.count_prev += 1
        self.count += 1

    # Para cuando los quadruplos vienen en lista
    def push_list(self, list, scope):
        for elem in list:
            self.push_quad(elem, scope)

    # Manda a resolver los quadruplos
    def solve_expression(self, expresion):
        sol = Quadruple.arithmetic_expression(expresion, self.temp_count)
        if type(sol) == str:
            print(sol)
            sys.exit()
        else:
            last_temp = sol.pop()
            # print(str(self.count) + "---BEFORE-----")
            # print(last_temp)
            # print()
            # print(self.temp_count)
            if len(sol) > 1:
                 self.temp_count = last_temp - 1
            else:
                self.temp_count = last_temp


            # print("---AFTER-----")
            # print(last_temp)
            # print()
            # print(self.temp_count)
            return sol

    # SET / GETS
    # Para poder guardar donde esta el inicio de una funcion
    def set_function_location(self, name):
        self.funcjump[name] = self.count

    # Para poder saber donde esta el inicio de una funcion
    def get_function_location(self, name):
        return Symbol(self.funcjump[name], "address")

    # Para cuando acabas de validar que sea el numero correcto
    # de parametros para la duncion actual
    def reset_param_count(self):
        self.param_count = 0

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
                    Symbol("param" + str(self.param_count),current_func_param.type, scope)
                )
            else:
                self.param_count += 1

                return Quadruple(
                    Symbol("PARAM", self.qstack[self.count_prev].result_id.type, scope),
                    self.qstack[self.count_prev].result_id,
                    None,
                    Symbol(("param" + str(self.param_count)),current_func_param.type, scope),
                )

        else:
            print("ERROR: sent a numer of parameters greater than declared")
            sys.exit()

    # Crea el quadruplo de return
    def return_in_function(self, type, scope,exp=None):
        if exp:
            # esto es si no es un void
            if self.expresion_or_id(exp, type, "Return"):
                exp = exp[0]
                self.push_quad(Quadruple(Symbol("RETURN",exp.type, scope),
                                         exp, 
                                         None, 
                                         None), scope)
            else:
                self.push_quad(
                    Quadruple(
                        Symbol("RETURN",self.qstack[self.count_prev].result_id.type, scope),
                        self.qstack[self.count_prev].result_id,
                        None,
                        None),scope)
        else:
            # esto es si si es void
            self.push_quad(Quadruple(Symbol("RETURN", "VOID", scope), None, None, None), scope)

        self.push_quad(Quadruple(Symbol("GOTO", "instruction", scope), None, None, "MISSING_ADDRESS"), scope)
        self.jumpStackR.append(self.count_prev)

    def parche_guadalupano(self, func_var, scope):
        self.push_quad(Quadruple(Symbol("EQ", "assignment", scope), func_var, None, Symbol(str("T" + str(self.temp_count)), func_var.type, scope)), scope)
        self.temp_count += 1


    def write_quad(self, exp, scope):
        if len(exp) == 1:
            exp = exp[0]
        else:
            exp = self.qstack[self.count_prev].result_id

        return Quadruple(Symbol("WRITE", "instruction", scope), None, None, exp)

    def read_quad(self, vars, scope):
        if len(vars) > 2:
            r = vars.pop(0)
            for v in vars:
                self.push_quad(Quadruple(Symbol("EQ", "assignment", scope), r, None, v), scope)
        else:
            print("ERROR: Error in read asignation")
            sys.exit()

    def object_method_quad(self, data, scope):
        if len(data) == 3:
            if data[2].type == "parentheses":
                self.push_quad(Quadruple(data[1], data[0], None, Symbol("1", "INT", "Constant Segment")), scope)
            else:
                if Symbol.check_type_compatibility("INT", data[2].type):
                    self.push_quad(Quadruple(data[1], data[0], None, data[2]), scope)
                else:
                    print("ERROR: Error parameter in object method not INT type")
                    sys.exit()
        else:
            print("ERROR: Error in object method call")
            sys.exit()

    # LLena el go to cuando se llega al final de una funcion
    def return_jump_fill(self):
        if len(self.jumpStackR) > 0:
            if self.jumpStackR[-1] == self.count_prev:
                self.qstack.pop(self.count_prev)
                self.count_prev -= 1
                self.count -= 1
                self.jumpStackR.pop()

            while len(self.jumpStackR) > 0:
                end = self.jumpStackR.pop()
                self.fill(end)

    # Para llenar el quadruplo de go to main
    def go_to_main(self):
        end = self.jumpStack.pop()
        self.fill(end)

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
            self.push_quad(Quadruple(Symbol("GOTOF", "instruction", scope), result, None, "MISSING_ADDRESS"), scope)
            self.jumpStack.append(self.count_prev)

    def ciclo_3(self, scope):
        # Le avisa al inicio a donde ir si se acaba y al final a donde ir si sigue
        end = self.jumpStack.pop()
        ret = self.jumpStack.pop()
        self.push_quad(Quadruple(Symbol("GOTO", "instruction"), None, None, ret), scope)
        self.fill(end)

    def if_1(self, scope):
        # ESTE VA DESPUES DEL COLON
        if not Symbol.check_type_compatibility(
            "BOOL", self.qstack[self.count_prev].result_id.type
        ):
            print("ERROR: Expresion in loop is not a boolean")
            sys.exit()
        else:
            result = self.qstack[self.count_prev].result_id
            self.push_quad(Quadruple(Symbol("GOTOF", "instruction", scope), result, None, "MISSING_ADDRESS"), scope)
            self.jumpStack.append(self.count_prev)

    def if_2(self):
        # ESTE VA CUANDO SE CIERRAN EL IF TOTAL
        end = self.jumpStack.pop()
        self.fill(end)

    def if_3(self, scope):
        # ESTE VA EN EL ELSE
        self.push_quad(Quadruple(Symbol("GOTO", "instruction", scope), None, None, "MISSING_ADDRESS"), scope)
        not_true = self.jumpStack.pop()
        self.jumpStack.append(self.count_prev)
        self.fill(not_true)

    # Mete el address indicado en el go_to
    def fill(self, index):
        if self.qstack[index].result_id == "MISSING_ADDRESS":
            self.qstack[index].result_id = Symbol(self.count, "address")

        else:
            print("ERROR: Error filling jump quadruple")
            sys.exit()

    # Prints y returns
    def print_quad(self, q):
        print(get_quad_formatted(q))

    def print_quads(self):
        print(get_quad_stack_formatted(self.qstack))

    def return_quads(self):
        rq = ""
        for k, v in self.qstack.items():
            rq += (
                str(int(k)).zfill(2)
                + " | "
                + str(
                    "-"
                    if v.operator == None
                    else (v.operator.name if type(v.operator) == Symbol else v.operator)
                )
                + " "
                + str(
                    "-"
                    if v.operand_1 == None
                    else (
                        v.operand_1.name if type(v.operand_1) == Symbol else v.operand_1
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_2 == None
                    else (
                        v.operand_2.name if type(v.operand_2) == Symbol else v.operand_2
                    )
                )
                + " "
                + str(
                    "-"
                    if v.result_id == None
                    else (
                        v.result_id.name if type(v.result_id) == Symbol else v.result_id
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
                    else (v.operator.name if type(v.operator) == Symbol else v.operator)
                )
                + " "
                + str(
                    "-"
                    if v.operand_1 == None
                    else (
                        v.operand_1.name if type(v.operand_1) == Symbol else v.operand_1
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_2 == None
                    else (
                        v.operand_2.name if type(v.operand_2) == Symbol else v.operand_2
                    )
                )
                + " "
                + str(
                    "-"
                    if v.result_id == None
                    else (
                        v.result_id.name if type(v.result_id) == Symbol else v.result_id
                    )
                )
                + r"\n"
            )
        return rq
