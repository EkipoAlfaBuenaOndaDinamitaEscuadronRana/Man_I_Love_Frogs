class Symbol(object):
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.type = type
    
    def get_name(self):
        return self.name

    def print_symbol(self):
        print("VAR: " + self.name)
        print("TYPE: " +self.type)
