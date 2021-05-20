import compilador.objects.symbol
from compilador.objects.symbol import *
import collections


class VariableTable(object):
    def __init__(self):
        self.variables = {}

    def reset_functionTable(self):
        self.variables = {}

    def set_variable(self, symbol, value):
        self.variables[symbol.name] = [symbol.type, value]

    def get_variable_type(self, name):
        return self.variables[name][0]

    def get_var_symbol(self, name):
        return Symbol(name, self.variables[name][0])

    def get_size(self):
        return len(self.variables)

    def lookup_variable(self, name):
        if name in self.variables:
            return True
        else:
            return False

    def print_VariableTable(self):
        print(get_vartable_formatted(self.variables))
