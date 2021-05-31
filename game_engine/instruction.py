from router_solver import *


class Instruction(object):
    def __init__(self, character_name, movement, times=None):
        self.character_name = character_name
        self.movement = movement
        if type(times) == int:
            self.times = int(times)  # TODO: Change this name attribute
        elif type(times) == str:
            self.times = str(times)

    def __eq__(self, other):
        if type(self) is Instruction and type(other) is Instruction:
            self_data = [
                self.character_name,
                self.movement,
                self.times,
            ]

            other_data = [
                other.character_name,
                other.movement,
                other.times,
            ]

            return self_data == other_data

    def __hash__(self):
        return id(self)

    def print_instructions(instructions):
        for instruction in instructions:
            print("CHARACTER_NAME:", instruction.character_name)
            if type(instruction.times) == int:
                print("MOVEMENT:", instruction.movement)
                print("TIMES:", instruction.times)
            elif type(instruction.times) == str:
                print("ATRIBUTE:", instruction.movement)
                print("NAME:", instruction.times)
            print()
