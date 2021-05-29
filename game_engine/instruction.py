from router_solver import *


class Instruction(object):
    def __init__(self, character_name, movement, times=None):
        self.character_name = character_name
        self.movement = movement
        self.times = times

    def print_instructions(instructions):
        for instruction in instructions:
            print("CHARACTER_NAME:", instruction.character_name)
            print("MOVEMENT:", instruction.movement)
            print("TIMES:", instruction.times)
            print()
