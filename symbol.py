import symbol


class Symbol(object):
    type_dictionary = {
        "int": "INT",
        "float": "FLT",
        "char": "CHAR",
        "bool": "BOOL",
        "null": "NULL",
        "string": "STR",
        "void": "VOID",
        "INT": "INT",
        "FLT": "FLT",
        "CHAR": "CHAR",
        "BOOL": "BOOL",
        "NULL": "NULL",
        "STR": "STR",
        "VOID" : "VOID",
        "operation": "operation",
        "parentheses": "parentheses",
        "not": "not",
        "assignment": "assignment",
        "comparison": "comparison",
        "matching": "matching",
        "assignment_operation": "assignment_operation",
    }

    type_translation = {
        "INT": ["INT", "NULL"],
        "FLT": ["INT", "FLT", "NULL"],
        "CHAR": ["CHAR", "NULL"],
        "BOOL": ["INT", "FLT", "BOOL", "NULL"],
        "NULL": ["NULL"],
        "STR": ["STR", "CHAR", "NULL"]
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

    def check_type_compatibility(type_recipient, type_sender):
        return type_sender in Symbol.type_translation[type_recipient]
            
    def print_symbol(self):
        print("VAR: " + self.name)
        print("TYPE: " + self.type)
