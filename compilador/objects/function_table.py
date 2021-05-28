from router_solver import *
import compilador.objects.variable_tables
import compilador.objects.symbol
from compilador.objects.variable_tables import *
from compilador.objects.symbol import *


class FunctionTable(object):
    def __init__(self):
        self.functions = {}

    def reset_functionTable(self):
        self.functions = {}

    def set_function(self, name, type, parameters, variable_table):
        self.functions[name] = {
            "t": (type_dictionary[type] if type in type_dictionary else None),
            "p": parameters,
            "s": 0,
            "vt": variable_table,
        }

    def set_function_variable_table_at(self, name):
        self.functions[name]["vt"] = VariableTable()
        for symbol in self.functions[name]["p"]:
            symbol.set_scope(name)
            self.functions[name]["vt"].set_variable(symbol)

    def set_function_size_at(self, name):
        self.functions[name]["s"] = self.functions[name]["vt"].get_size()

    def insert_to_constant_table(self, constant):
        for c in constant:
            if not self.functions["Constant Segment"]["vt"].lookup_variable(c.name):
                self.functions["Constant Segment"]["vt"].set_variable(c)

    def get_function(self, name):
        return self.functions[name]

    def get_function_type(self, name):
        return self.functions[name]["t"]

    def get_function_parameters(self, name):
        return self.functions[name]["p"]

    def get_function_size(self, name):
        return self.functions[name]["s"]

    def get_function_variable_table(self, name):
        return self.functions[name]["vt"]

    def erase_function_variable_table(self, name):
        del self.functions[name]["vt"]
        self.functions[name]["vt"] = None

    def lookup_function(self, name):
        if name in self.functions:
            return True
        else:
            return False

    def print_FuncTable(self):
        print(get_functable_formatted(self.functions))
