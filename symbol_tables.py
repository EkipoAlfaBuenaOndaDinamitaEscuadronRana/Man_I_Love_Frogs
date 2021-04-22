import collections
from symbol import *

class VariableTable(object):
    def __init__(self):
        self.variables = {}

    def set_variable(self, symbol, value):
        self.variables[symbol.name] = [symbol.type, value]
    
    def get_variable(self, name):
        return self.variables[name]
    
    def lookup_variable(self, name):
        if name in self.variables:
            return True
        else:
            return False
    
    def print_VariableTable(self):
        print("NAME TYPE VALUE ")
        for s in self.variables:
            print(s + "   " + self.variables[s][0] + "     " +  str(self.variables[s][1]))
            print()
        

class FunctionTable(object):
    def __init__(self):
        self.functions = {}

    def set_function(self, name, type):
        self.functions[name] = type

    def get_function(self, name):
        return self.functions[name]

    def lookup_function(self, name):
        if name in self.functions:
            return True
        else:
            return False

    def print_FuncTable(self):
        print("NAME TYPE")
        for name in self.functions:
            print(name + "   " + self.functions[name])
            print()



# a = Symbol("a", "int")
# b = Symbol("b", "int")
# a2 = Symbol("a", "int")
# vt = VariableTable()

# vt.set_variable(a, 1)
# vt.set_variable(b, 2)

# if vt.lookup_variable(a2.name):
#     print("found an existing a")
# else: 
#     vt.set_variable(a2, 1)


# vt.print_VariableTable()