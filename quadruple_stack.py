from quadruple import *
import sys

class QuadrupleStack(object):
    def __init__(self):
        self.qstack = {}
        self.count_prev = 0
        self.count = 1
        self.jumpStack = []

    def push_quad(self, quadruple):
        self.qstack[self.count] = quadruple
        # print("push_quad")
        # self.print_quads()
        self.count_prev += 1
        self.count += 1
    
    def  push_list(self, list):
        for elem in list:
            self.push_quad(elem)

    def solve_expression(self, expresion):
        return Quadruple.arithmetic_expression(expresion, self.count)

    def if_1(self):
        # ESTE VA DESPUES DEL COLON
        # > A C T1
        #TYPE CHECK (checa que el ultimo quad si sea un bool)
        # lo siguiente va en un else
        if self.count > 20:
            sys.exit()

        result = self.qstack[self.count_prev].result_id
        self.push_quad(Quadruple("GOTOF", result, '-', 'MISSING_ADDRESS'))
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
        self.push_quad(Quadruple("GOTO", '-', '-', 'MISSING_ADDRESS'))
        not_true = self.jumpStack.pop()
        self.jumpStack.append(self.count_prev)
        self.fill(not_true)
        # print("if_3")
        # self.print_quads()

    def fill(self, index):
        if self.qstack[index].result_id == 'MISSING_ADDRESS':
            self.qstack[index].result_id = self.count
            # print("fill")
            # self.print_quads()
        else:
            print("ERROR: Error filling jump quadruple")
            sys.exit()

    def print_quads(self):
        for k, v in self.qstack.items():
             
            print(str(int(k)).zfill(2) + " | " + str(v.operator) + " " + str(v.operand_1) + " " + str(v.operand_2) + " " + str(v.result_id))