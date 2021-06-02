from router_solver import *
import compilador.objects.symbol
from compilador.objects.symbol import *

# CLASE MEMORY SEGMENT
# Objeto que objetos en un segmento de memoria unico

class MemorySegment(object):
        ####################### INITS #######################

    def __init__(self, name, size, initial_position):
        self.name = name    # Nombre de la instancia de memoria
        self.size = size    # tamaño de la instancia de memoria
        self.__memory = dict()  # Dicionario de memoria con simbolos
        self.__memory_values = dict()   # Dicionario de memoria con valores reales
        self.__subsegment_size = size // 7  # Tamaño de cada sub segmento por tipo
        self.initial_position = initial_position    # Dirección inicial global        

        self.ints = 0 # dirección inicial de INTs
        self.flts = self.__subsegment_size # Dirección inicial de FLTs
        self.strs = self.__subsegment_size * 2  # Dirección inical de STRs
        self.chars = self.__subsegment_size * 3 # Dirección inical de CHARs 
        self.bools = self.__subsegment_size * 4 # Dirección inicial de BOOLs
        self.nulls = self.__subsegment_size * 5 # Dirección inicial de NULLs
        self.frogs = self.__subsegment_size * 6 # Dirección inicial de FROG

        self.spare_memory_ints = self.__subsegment_size # Tamaño de memoria segmento INT
        self.spare_memory_flts = self.__subsegment_size # Tamaño de memoria segmento FLT
        self.spare_memory_strs = self.__subsegment_size # Tamaño de memoria segmento STR
        self.spare_memory_chars = self.__subsegment_size # Tamaño de memoria segmento CHAR
        self.spare_memory_bools = self.__subsegment_size # Tamaño de memoria segmento BOOL
        self.spare_memory_nulls = self.__subsegment_size # Tamaño de memoria segmento NULL
        self.spare_memory_frogs = self.__subsegment_size # Tamaño de memoria segmento FROG

        ####################### SETS #######################


    # Validaciones antes de asignar dirección de memoria al simbolo
    def insert_symbol(self, symbol):
        s_type = symbol.type
        # Genera dirección inicial de subsegmento
        initial_position = self.__get_memory_inital_direction(s_type)
        # Genera dirección en segmento de memoria
        symbol_position = self.__get_symbol_position(s_type)
        # Genera tamaño que tomara en memoria
        s_size = symbol.memory_size()
        # Valida que la memoria que necesita no exceda la disponible 
        if symbol_position + s_size - 1 < initial_position + self.__subsegment_size:
            # Asigna y el simbolo a memoria 
            self.__assign_memory(symbol, symbol_position)
            # Resta memoria que necesita de la memoria disponible
            self.__substract_memory(symbol)

            return True

        print("ERROR: Memory exceded for in " + self.name + " for type" + s_type )
        sys.exit()
    
    # Asigna memoria a una variable
    def __assign_memory(self, symbol, symbol_position):
        if type(symbol) == Symbol:
            # Asigna dirección de segmento local
            symbol.segment_direction = symbol_position
            # Asigna dirección global
            symbol.global_direction = self.initial_position + symbol_position
            # Guarda simbolo en memoria
            self.__memory[symbol_position] = symbol
            # Guarda valor en memoria
            self.__memory_values[symbol_position] = symbol.value
            # Si es constante o tipo FROG su valor es su nombre
            if self.name == "Constant Segment" or symbol.type == "FROG":
                symbol.value = symbol.name
                self.__memory_values[symbol_position] = symbol.name
        else:
            pass


    # Resta tamaño de simbolo a memoria disponible del subsegmento del tipo 
    def __substract_memory(self, symbol):
        s_type = symbol.type
        s_size = symbol.memory_size()

        if s_type == "INT":
            self.spare_memory_ints -= s_size

        elif s_type == "FLT":
            self.spare_memory_flts -= s_size

        elif s_type == "STR":
            self.spare_memory_strs -= s_size

        elif s_type == "CHAR":
            self.spare_memory_chars -= s_size

        elif s_type == "BOOL":
            self.spare_memory_bools -= s_size

        elif s_type == "NULL":
            self.spare_memory_nulls -= s_size

        elif s_type == "FROG":
            self.spare_memory_frogs -= s_size


       ####################### GETS #######################

    # Regresa la dirección inicial del sub segmento por tipo
    def __get_memory_inital_direction(self, s_type):
        type_inital_position = {
            "INT": self.ints,
            "FLT": self.flts,
            "STR": self.strs,
            "CHAR": self.chars,
            "BOOL": self.bools,
            "NULL": self.nulls,
            "FROG": self.frogs,
        }

        return type_inital_position[s_type]

    # Regresa el tamaño restante de memoria en el subsegmento por tipo
    def __get_spare_memory(self, s_type):
        left_memory = {
            "INT": self.spare_memory_ints,
            "FLT": self.spare_memory_flts,
            "STR": self.spare_memory_strs,
            "CHAR": self.spare_memory_chars,
            "BOOL": self.spare_memory_bools,
            "NULL": self.spare_memory_nulls,
            "FROG": self.spare_memory_frogs,
        }

        return left_memory[s_type]
    
    # Regresa la dirección local a la cual se asignara un simbolo dependiendo de su tipo
    def __get_symbol_position(self, s_type):
        return (
            self.__subsegment_size
            - self.__get_spare_memory(s_type)
            + self.__get_memory_inital_direction(s_type)
        )
       
    
    ####################### SEARCH #######################

    # Regresa simbolo en una dirección
    def search_symbol(self, direction):
        direction = direction - self.initial_position
        return self.__memory.get(direction, None)

    # Regresa valor en una dirección
    def search_value(self, direction):
        direction = direction - self.initial_position
        return self.__memory_values.get(direction, None)

    
    ####################### MODIFY #######################

    # Modifica el valor en una dirección
    def modify_value(self, direction, value):
        direction = direction - self.initial_position
        self.__memory_values[direction] = value
    
    # Se asigna dirección a simbolo de arreglo[indice] y guarda su valor en memoria
    def modify_address(self, symbol, address):
        if address not in self.__memory.keys():
            self.__assign_memory(symbol, address)

    ####################### SAVE MEMORY #######################

    # Regresa un diccionario temporal con el valor en cada dirección 
    def save_local_memory(self):
        local_data = {}
        for space in self.__memory:
            local_data[space] = self.__memory[space].value

        return local_data

    # Borra la dirección del simbolo y borra el valor
    def erase_local_memory(self):
        for space in self.__memory:
            self.__memory[space].segment_direction = None
            self.__memory[space].global_direction = None
            self.__memory_values[space] = None
    
    # Regresa la memoria a lo que se tenía cuando se congelo
    def backtrack_memory(self, frozen_memory):
        for k, v in frozen_memory.items():
            self.__memory[k].value = v
            self.__memory[k].segment_direction = k
            self.__memory[k].global_direction = k + self.initial_position

    ####################### PRINTS #######################

    # Imprime segmento de memoria
    def print_memory_segment(self):
        print("##### MEMORY ", self.name, " ##########")
        for space in self.__memory:
            self.__memory[space].print_symbol()
            print("SAVED_VALUE:", self.__memory_values[space])
            print("................")

