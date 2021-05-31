from router_solver import *
import compilador.helpers.printer
from compilador.helpers.printer import *
import numpy as np


class BaseAddress(object):
    def __init__(
        self, name=None, symbol=None, parent=None, type=None, scope=None, offset=None
    ):
        self.name = name  # A-BA
        self.symbol = symbol
        self.parent = parent  # A
        self.type = type  # INT
        self.scope = scope  # GLOBAL
        self.offset = offset  # 17
        self.value = None
        self.segment_direction = None
        self.global_direction = None

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
