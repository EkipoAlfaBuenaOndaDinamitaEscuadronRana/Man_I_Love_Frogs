from re import A
from quadruple import *
import sys


class QuadrupleStack(object):
    def __init__(self):
        self.qstack = {}
        self.count_prev = 0
        self.count = 1
        self.jumpStack = []
        self.jumpStackR = []
        self.funcjump = {}
        self.param_count = 0

    def reset_quad(self):
        self.qstack = {}
        self.count_prev = 0
        self.count = 1
        self.jumpStack = []
        self.funcjump = {}
        self.param_count = 0

    def push_quad(self, quadruple):
        self.qstack[self.count] = quadruple
        # print("push_quad")
        # self.print_quads()
        self.count_prev += 1
        self.count += 1

    def push_list(self, list):
        for elem in list:
            self.push_quad(elem)

    def solve_expression(self, expresion):
        sol = Quadruple.arithmetic_expression(expresion, self.count)
        if type(sol) == str:
            print(sol)
            sys.exit()
        else:
            return sol

    def set_function_location(self, name):
        self.funcjump[name] = self.count

    def get_function_location(self, name):
        return self.funcjump[name]

    def reset_param_count(self):
        self.param_count = 0

    def get_param_count(self):
        return self.param_count

    def expresion_or_id(self, param, type, error_message):
        if len(param) == 1:
            param = param[0]
            # Busca que los tipos sean iguales pero pues podrian ser compatibles? si le mando un int a
            # un float deberia de funcionar creo?? hmmm dificil dificil
            if symbol.Symbol.check_type_compatibility(type, param.type):
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

            if symbol.Symbol.check_type_compatibility(
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

    def go_to_main(self):
        end = self.jumpStack.pop()
        self.fill(end)

    def validate_parameters(self, func_param, sent_param):
        if self.param_count < len(func_param):
            current_func_param = func_param[self.param_count]
            if self.expresion_or_id(sent_param, current_func_param.type, "Parameter"):
                sent_param = sent_param[0]
                self.param_count += 1
                return Quadruple(
                    "param", sent_param.name, None, "param" + str(self.param_count)
                )
            else:
                self.param_count += 1
                return Quadruple(
                    "param",
                    self.qstack[self.count_prev].result_id.name,
                    None,
                    "param" + str(self.param_count),
                )

        else:
            print("ERROR: sent a numer of parameters greater than declared")
            sys.exit()

    def return_in_function(self, type, exp=None):
        if exp:
            # esto es si no es un void
            if self.expresion_or_id(exp, type, "Return"):
                exp = exp[0]
                self.push_quad(Quadruple("RETURN", exp.name, None, None))
            else:
                self.push_quad(
                    Quadruple(
                        "RETURN",
                        self.qstack[self.count_prev].result_id.name,
                        None,
                        None,
                    )
                )
        else:
            # esto es si si es void
            self.push_quad(Quadruple("RETURN", None, None, None))
            # PARA IR AL FINAL
            # Pensamientos que no quiero olvidar
            # validar el si en este spectrum no paso por un return y deberia
            # Preguntar si its okay si le digo gotonext

        self.push_quad(Quadruple("GOTO", None, None, "MISSING_ADDRESS"))
        self.jumpStackR.append(self.count_prev)

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

    def ciclo_1(self):
        # Esta va antes de las expresiones del while
        self.jumpStack.append(self.count)

    def ciclo_2(self):
        # TYPE CHECK (checa que el ultimo quad si sea un bool)
        # lo siguiente va en un else
        # Combinar con el de abajo tentativamente?
        if not symbol.Symbol.check_type_compatibility(
            "BOOL", self.qstack[self.count_prev].result_id.type
        ):
            print("ERROR: Expresion in loop is not a boolean")
            sys.exit()
        else:
            result = self.qstack[self.count_prev].result_id
            self.push_quad(Quadruple("GOTOF", result, None, "MISSING_ADDRESS"))
            self.jumpStack.append(self.count_prev)

    def ciclo_3(self):
        # Le avisa al inicio a donde ir si se acaba y al final a donde ir si sigue
        end = self.jumpStack.pop()
        ret = self.jumpStack.pop()
        self.push_quad(Quadruple("GOTO", None, None, ret))
        self.fill(end)

    def if_1(self):
        # ESTE VA DESPUES DEL COLON
        # TYPE CHECK (checa que el ultimo quad si sea un bool)
        # lo siguiente va en un else
        if not symbol.Symbol.check_type_compatibility(
            "BOOL", self.qstack[self.count_prev].result_id.type
        ):
            print("ERROR: Expresion in loop is not a boolean")
            sys.exit()
        else:
            result = self.qstack[self.count_prev].result_id
            self.push_quad(Quadruple("GOTOF", result, None, "MISSING_ADDRESS"))
            self.jumpStack.append(self.count_prev)
        # print("if_1")
        # self.print_quads()

    def if_2(self):
        # ESTE VA CUANDO SE CIERRAN EL IF TOTAL
        end = self.jumpStack.pop()
        self.fill(end)
        # print("if_2")
        # self.print_quads()

    def if_3(self):
        # ESTE VA EN EL ELSE
        self.push_quad(Quadruple("GOTO", None, None, "MISSING_ADDRESS"))
        not_true = self.jumpStack.pop()
        self.jumpStack.append(self.count_prev)
        self.fill(not_true)
        # print("if_3")
        # self.print_quads()

    def fill(self, index):
        if self.qstack[index].result_id == "MISSING_ADDRESS":
            self.qstack[index].result_id = self.count
            # print("fill")
            # self.print_quads()
        else:
            print("ERROR: Error filling jump quadruple")
            sys.exit()

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
                    else (
                        v.operator.name
                        if type(v.operator) == symbol.Symbol
                        else v.operator
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_1 == None
                    else (
                        v.operand_1.name
                        if type(v.operand_1) == symbol.Symbol
                        else v.operand_1
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_2 == None
                    else (
                        v.operand_2.name
                        if type(v.operand_2) == symbol.Symbol
                        else v.operand_2
                    )
                )
                + " "
                + str(
                    "-"
                    if v.result_id == None
                    else (
                        v.result_id.name
                        if type(v.result_id) == symbol.Symbol
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
                        if type(v.operator) == symbol.Symbol
                        else v.operator
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_1 == None
                    else (
                        v.operand_1.name
                        if type(v.operand_1) == symbol.Symbol
                        else v.operand_1
                    )
                )
                + " "
                + str(
                    "-"
                    if v.operand_2 == None
                    else (
                        v.operand_2.name
                        if type(v.operand_2) == symbol.Symbol
                        else v.operand_2
                    )
                )
                + " "
                + str(
                    "-"
                    if v.result_id == None
                    else (
                        v.result_id.name
                        if type(v.result_id) == symbol.Symbol
                        else v.result_id
                    )
                )
                + r"\n"
            )
        return rq
