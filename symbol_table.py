import collections

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
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



a = Symbol('a', 'int')
b = Symbol('b', 'string')

vt = VarTable()
vt.push_variable(a, 1)
vt.push_variable(b, 'hola')

ft = FuncTable()
ft.push_function('square', 'int')
ft.push_function('validate', 'void')

#a.print_symbol()

vt.print_VarTable()
ft.print_FuncTable()

