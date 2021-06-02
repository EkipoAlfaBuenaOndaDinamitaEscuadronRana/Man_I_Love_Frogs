from router_solver import *

# CLASE STATE 
# Objeto que guarda el nombre del contexto actual e información del estado actual

class State(object):
    def __init__(self, table=None, opt=None):
        self.table = table      # Nombre del contexto actual
        self.opt = opt          # Opcional de estado actual

# CLASE STATE TABLE
# Objeto que guarda un stack de estados del parser

class StateTable(object):

    ####################### INITS #######################
    
    def __init__(self):
        self.states = []        # Stack de estados

    # Reinica los valores para cuando compilan cosas consecutivamente
    def reset_states(self):
        self.states = []

    ####################### SETS #######################

    # Agrega un estado a la tabla de estados
    def set_state(self, state):
        self.states.append(state)
    
    # Le agrega un valor al opcional de la tabla actual
    def set_curr_state_opt(self, opt):
        self.states[-1].opt = opt

    ####################### GETS #######################

    # Regresa el nombre del contexto actual
    def get_curr_state_table(self):
        return self.states[-1].table

    # Regresa el valor del ocpional actual
    def get_curr_state_opt(self):
        return self.states[-1].opt

    # Regresa el nombre de la tabla global
    def get_global_table(self):
        return self.states[0].table

    ####################### POPS #######################

    # Borra el ultimo opcional de la lista
    def pop_curr_state_opt(self):
        self.states[-1].opt = None

    # Borra el ultimo estado de la lista
    def pop_curr_state(self):
        self.states.pop()

    ####################### PRINTS #######################

    # Imprime tabla de estados
    def print_StateTable(self):
        print(get_statetable_formatted(self.states))
