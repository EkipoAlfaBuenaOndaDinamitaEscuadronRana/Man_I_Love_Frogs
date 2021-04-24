class Cuadruple(object):
    def __init__(self, operator, operand_1, operand_2, result_id):
        self.operator = operator
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.result_id = result_id

    def format_cuadruple(self):
        return "{} {} {} {}".format(self.operator, self.operand_1, self.operand_2, self.result_id)
