from quadruple import *

class QuadrupleStack(object):
    def __init__(self):
        self.qstack = {}
        self.count = 0

    def push_quad(self, quadruple):
        self.count += 1
        self.qstack[self.count] = quadruple
    
    def  push_list(self, list):
        for elem in list:
            self.push_quad(elem)

    def solve_expression(self, expresion):
        quad = Quadruple(None, None, None, None)
        return quad.arithmetic_expression(expresion)

    def print_quads(self):
        for k, v in self.qstack.items():
            print("ID: " + str(k) + " QUADS: " + v.operator + " " + v.operand_1 + " " + v.operand_2 + " " + v.result_id)