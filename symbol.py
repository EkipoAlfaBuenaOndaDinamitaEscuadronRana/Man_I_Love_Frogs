import symbol


class Symbol(object):
    type_dictionary = {
        "int": "INT",
        "float": "FLT",
        "char": "CHAR",
        "bool": "BOOL",
        "null": "NULL",
        "string": "STR",
        "INT": "INT",
        "FLT": "FLT",
        "CHAR": "CHAR",
        "BOOL": "BOOL",
        "NULL": "NULL",
        "STR": "STR",
        "operation": "operation",
        "parentheses": "parentheses",
        "not": "not",
        "assignment": "assignment",
        "comparison": "comparison",
        "matching": "matching",
        "assignment_operation": "assignment_operation",
    }

    def __init__(self, name=None, type=None):
        self.name = name
        self.type = (
            Symbol.type_dictionary[type] if type in Symbol.type_dictionary else None
        )

    def __eq__(self, quad):
        if type(self) is Symbol and type(quad) is Symbol:
            return self.name == quad.name and self.type == quad.type
        elif self is None and quad is None:
            return True
        else:
            return False

    def __hash__(self):
        return id(self)

    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        self.type = (
            Symbol.type_dictionary[type] if type in Symbol.type_dictionary else None
        )

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def print_symbol(self):
        print("VAR: " + self.name)
        print("TYPE: " + self.type)
