import collections

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
    def print_symbol(self):
        print("VAR: " + self.name)
        print("TYPE: " +self.type)

class SymbolTable(object):
    def __init__(self):
        self.symbols = {}

    def push_symbol(self, symbol, value):
        self.symbols[symbol] = value

    def print_table(self):
        print("NAME TYPE VALUE ")
        for symbol in self.symbols:
            print(symbol.name + "     " + symbol.type + "    " +  str(self.symbols[symbol]))
            #symbol.print_symbol()
            #print("VALUE: " + str(self.symbols[symbol]))
            print()





a = Symbol('a', 'int')
b = Symbol('b', 'string')

st = SymbolTable()
st.push_symbol(a, 1)
st.push_symbol(b, 'hola')

#a.print_symbol()

st.print_table()

