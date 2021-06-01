from router_solver import *
import compilador.objects.symbol
from compilador.objects.symbol import *
import collections


# CLASE VARIABLE TABLE
# Objeto que guarda el tabla de variables


class VariableTable(object):

    ####################### INITS #######################

    def __init__(self):
        self.variables = {}  # Dictioario de variables
        self.offsets = {  # Offset de variable por tipo
            "INT": 0,
            "FLT": 0,
            "CHAR": 0,
            "BOOL": 0,
            "STR": 0,
            "FROG": 0,
            "NULL": 0,
        }

    # Reinica los valores para cuando compilan cosas consecutivamente
    def reset_functionTable(self):
        self.variables = {}
        self.offsets = {
            "INT": 0,
            "FLT": 0,
            "CHAR": 0,
            "BOOL": 0,
            "STR": 0,
            "FROG": 0,
            "NULL": 0,
        }

    ####################### SETS #######################

    # Guarda una variable en la tabla
    # Key : Nombre de la variable
    # Value : simbolo de la variable
    def set_variable(self, symbol):
        self.variables[symbol.name] = symbol
        self.set_address(symbol)

    # Guarda el offset de la variable
    def set_address(self, symbol):
        self.offsets[symbol.type] = self.variables[symbol.name].set_address(
            self.offsets[symbol.type]
        )

    # Guarda el temporal donde se asigno el valor de retorno de una función
    def set_return_location(self, name, loc):
        self.variables[name].set_return_location(loc)

    ####################### GETS #######################

    # Regresa el tipo de una variable
    def get_variable_type(self, name):
        return self.variables[name].type

    # Regresa el simbolo de una variable con su nombre
    def get_var_symbol(self, name):
        return self.variables[name]

    # Regresa el tamaño de la tabla de variables consierando dimensiones
    def get_size(self):
        size = 0
        for k, v in self.variables.items():
            if v.is_dimensioned():
                size += v.get_dimension_sizes()
            else:
                size += 1
        return size

    ####################### SEARCH #######################

    # Indica si existe una variable en la tabla de variables
    def lookup_variable(self, name):
        return name in self.variables

    ####################### PRINTS #######################

    # Imprime tabla de variables
    def print_VariableTable(self):
        print(get_vartable_formatted(self.variables))
