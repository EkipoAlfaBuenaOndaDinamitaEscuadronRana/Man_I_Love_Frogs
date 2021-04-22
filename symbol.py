class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def print_symbol(self):
        print("VAR: " + self.name)
        print("TYPE: " +self.type)
