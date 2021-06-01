from router_solver import *
import compilador.objects.variable_tables
import compilador.objects.symbol
from compilador.objects.variable_tables import *
from compilador.objects.symbol import *

# CLASE FUNCTION TABLE
# Objeto que guarda el directorio de funciones del programa


class FunctionTable(object):

    ####################### INITS #######################

    def __init__(self):
        self.functions = {}  # Diccionario de funciones
        self.temp_table = {}  # Guarda los temporales usados
        self.function_symbols = {}  # Genera un simbolo unico para cada función

    # Reinica los valores para cuando compilan cosas consecutivamente
    def reset_functionTable(self):
        self.functions = {}
        self.temp_table = {}
        self.function_symbols = {}

    ####################### SETS #######################

    # Guarda una función en la tabla
    # Key   : Nombre de la función
    # Value : Diccionario de valores
    # t     -> Guarda el tipo de la función
    # p     -> Guarda lista de parametros de la función
    # s     -> Guarda el tamaño de la función
    # vt    -> Guarda la tabla de variables de la función
    # Guarda el simbolo unico de la función en la tabla
    def set_function(self, name, type, parameters, variable_table, scope=None):
        self.functions[name] = {
            "t": (type_dictionary[type] if type in type_dictionary else None),
            "p": parameters,
            "s": 0,
            "vt": variable_table,
        }
        self.function_symbols[name] = Symbol(name, type, scope)

    # Genera la tabla de variables en una función en especifico
    # Guarda los parametros de la función en la tabla de variables
    def set_function_variable_table_at(self, name):
        self.functions[name]["vt"] = VariableTable()
        for symbol in self.functions[name]["p"]:
            symbol.set_scope(name)
            self.functions[name]["vt"].set_variable(symbol)

    # Guarda el tamaño de la función
    def set_function_size_at(self, name, size):
        self.functions[name]["s"] = size

    # Mete una variable constante a la tabla de constantes
    # Valida que constante no exista en la tabla
    def insert_to_constant_table(self, constant):
        for c in constant:
            if not self.functions["Constant Segment"]["vt"].lookup_variable(c.name):
                self.functions["Constant Segment"]["vt"].set_variable(c)

    # Guarda simbolo unico para cada temporal
    def set_temporal(self, symbol):
        data = str([symbol.name, symbol.scope])
        self.temp_table[data] = symbol

    ####################### GETS #######################

    # Genera el tamaño de la función
    # Tamaño de tabla de variables + temporales usados
    def generate_function_size_at(self, name, temps):
        if temps > 0:
            temps -= 1
        return self.functions[name]["vt"].get_size() + temps

    # Regresa el simbolo unico de la función
    def get_function_symbol(self, name):
        return self.function_symbols[name]

    # Regresa el tipo de la función
    def get_function_type(self, name):
        return self.functions[name]["t"]

    # Regrea los parametros de la función
    def get_function_parameters(self, name):
        return self.functions[name]["p"]

    # Regresa el tamaño de la función
    def get_function_size(self, name):
        return self.functions[name]["s"]

    # Regresa tabla de variables de función
    def get_function_variable_table(self, name):
        return self.functions[name]["vt"]

    # Regresa simbolo unico de temporal
    def get_temporal(self, symbol):
        return self.temp_table[str([symbol.name, symbol.scope])]

    ####################### SEARCH #######################

    # Indica si existe una función en la tabla de funciones
    def lookup_function(self, name):
        return name in self.functions

    # Indica si existe el temporal en la lista de temporales
    def lookup_temporal(self, symbol):
        data = str([symbol.name, symbol.scope])
        return data in self.temp_table

    ####################### PRINTS #######################

    # Imprime tabla de funciones
    def print_FuncTable(self):
        print(get_functable_formatted(self.functions))
