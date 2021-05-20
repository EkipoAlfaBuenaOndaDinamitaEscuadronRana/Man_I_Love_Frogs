from router_solver import *

class State(object):
    def __init__(self, table=None, opt=None):
        self.table = table
        self.opt = opt

    def set_state(self, table, opt=None):
        self.table = table
        self.opt = opt


class StateTable(object):
    def __init__(self):
        self.states = []

    def reset_states(self):
        self.states = []

    def push_state(self, state):
        self.states.append(state)

    def get_curr_state(self):
        return self.states[-1]

    def get_curr_state_table(self):
        return self.states[-1].table

    def get_curr_state_opt(self):
        return self.states[-1].opt

    def set_curr_state_opt(self, opt):
        self.states[-1].opt = opt

    def remove_curr_state_opt(self):
        self.states[-1].opt = None

    def pop_curr_state(self):
        self.states.pop()

    def get_and_pop(self):
        s = self.get_curr_state()
        self.pop_curr_state()
        return s

    def get_global_table(self):
        return self.states[0].table

    def isEmpty(self):
        return self.states.count() == 0

    def isValidState(self, state, functiontable):
        otherValidStates = ["funcD", "noVar", "as_on"]
        if not state.isEmpty():
            if state.table not in functiontable.keys():
                if state.table not in otherValidStates:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    def print_StateTable(self):
        print(get_statetable_formatted(self.states))
