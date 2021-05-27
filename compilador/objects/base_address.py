from router_solver import *
import compilador.helpers.printer
from compilador.helpers.printer import *
import numpy as np

class BaseAddress(object):

    def __init__(self, name=None, parent =None, type=None, scope=None, offset=None):
        self.name = name #A-BA
        self.parent = parent #A
        self.type = type #INT
        self.scope = scope #GLOBAL
        self.offset = offset #17
        
