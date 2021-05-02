import collections

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def __eq__(self, quad):
        return self.name == quad.name and self.type == quad.type
    
    def __hash__(self):
        return id(self)

    def print_symbol(self):
        print("VAR: " + self.name)
        print("TYPE: " +self.type)

class VarTable(object):
    def __init__(self):
        self.variables = {}

    def push_variable(self, symbol, value):
        self.variables[symbol] = value

    def print_VarTable(self):
        print("NAME TYPE VALUE ")
        for symbol in self.variables:
            print(symbol.name + "   " + symbol.type + "     " +  str(self.variables[symbol]))
            print()

class FuncTable(object):
    def __init__(self):
        self.functions = {}

    def push_function(self, name, type):
        self.functions[name] = type

    def print_FuncTable(self):
        print("NAME TYPE")
        for name in self.functions:
            print(name + "   " + self.functions[name])
            print()
