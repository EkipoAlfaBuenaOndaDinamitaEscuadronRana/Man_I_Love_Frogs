from router_solver import *
import compilador.helpers.printer
from compilador.helpers.printer import *
import numpy as np

# CLASE BASE ADDRESS
# Objeto que guarda la dirección base de un arreglo


class BaseAddress(object):
    def __init__(
        self, name=None, symbol=None, parent=None, type=None, scope=None, offset=None
    ):
        self.name = name  # Nombre de variable - BA
        self.symbol = symbol  # Guarda el simbolo de su padre
        self.parent = parent  # Guarda el nombre de su padre
        self.type = type  # Guarda el tipo de su padre
        self.scope = scope  # Guarda el contexto de su padre
        self.offset = offset  # Guarda el tamaño de su padre
        self.value = None  # Guarda su valor real
        self.segment_direction = None  # Guarda su dirección en el segmento
        self.global_direction = None  # Guarda su dirección global

    # Imprime datos de objeto

    def print_base_address(self):
        if self.name:
            print("VAR:", self.name)

        if len(self.type):
            print("TYPE:", self.type)

        if self.parent:
            print("PARENT:", self.parent)

        if self.segment_direction != None and self.global_direction != None:
            print("SEGMENT_DIRECTION:", self.segment_direction)
            print("GLOBAL_DIRECTION:", self.global_direction)

        if self.scope:
            print("SCOPE:", self.scope)

        if self.value:
            print("VALUE: ", self.value)

        if self.offset:
            print("VALUE: ", self.offset)

    def memory_size(self):
        # self.print_base_address()
        # print("------------------------------")
        # TODO: Change to real size
        return 2
