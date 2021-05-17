from re import A
from quadruple import *
import sys


class QuadrupleStack(object):
    def __init__(self):
        self.qstack = {}
        self.count_prev = 0
        self.count = 1
        self.jumpStack = []
        self.funcjump = {}

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
        self.count_prev += 1
        self.count += 1


    def ciclo_1(self):
        # Esta va antes de las expresiones del while
        self.jumpStack.append(self.count)

    def ciclo_2(self):
        # TYPE CHECK (checa que el ultimo quad si sea un bool)
        # lo siguiente va en un else
        # Combinar con el de abajo tentativamente?
        if self.qstack[self.count_prev].result_id.type != "BOOL":
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
        if self.qstack[self.count_prev].result_id.type != "BOOL":
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

    def print_quads(self):
        for k, v in self.qstack.items():
            print(
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
            )

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
