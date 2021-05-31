from router_solver import *
import compilador.objects.symbol
from compilador.objects.symbol import *
import collections


class VariableTable(object):
    def __init__(self):
        self.variables = {}
        self.offsets = {
            "INT": 0,
            "FLT": 0,
            "CHAR": 0,
            "BOOL": 0,
            "STR": 0,
            "FROG": 0,
            "NULL": 0,
        }

    def reset_functionTable(self):
        self.variables = {}
        self.offsets = {
            "INT": 0,
            "FLT": 0,
            "CHAR": 0,
            "BOOL": 0,
            "STR": 0,
            "FROG": 0,
            "NULL": 0,
        }

    def set_variable(self, symbol):
        self.variables[symbol.name] = symbol
        self.add_address(symbol)

    def get_variable_type(self, name):
        return self.variables[name].type

    def get_var_symbol(self, name):
        return self.variables[name]

    def add_address(self, symbol):
        self.offsets[symbol.type] = self.variables[symbol.name].set_address(
            self.offsets[symbol.type]
        )

    def add_return_location(self, name, loc):
        self.variables[name].set_return_location(loc)

    def get_size(self):
        size = 0
        for k, v in self.variables.items():
            if v.is_dimensioned():
                size += v.get_dimension_sizes()
            else:
                size += 1
        return size

    def lookup_variable(self, name):
        if name in self.variables:
            return True
        else:
            return False

    def print_VariableTable(self):
        print(get_vartable_formatted(self.variables))
