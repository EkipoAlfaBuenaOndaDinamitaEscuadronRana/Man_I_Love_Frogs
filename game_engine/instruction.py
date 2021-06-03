from router_solver import *


class Instruction(object):
    def __init__(self, character_name, movement, times=None):
        self.character_name = character_name
        self.movement = movement
        if type(times) == int:
            self.times = int(times)

    # Verifica que dos instructiones sean iguales
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

            if instruction.movement == "hat":
                valid_hats = {1: '"cowboy"', 2: '"cool"', 3: '"shoes"', 4: '"makeup"'}
                name = ""
                if instruction.times not in valid_hats:
                    name = "None"
                else:
                    name = valid_hats[instruction.times]

                print("ATRIBUTE:", instruction.movement)
                print("NAME:", name)
            else:
                print("MOVEMENT:", instruction.movement)
                print("TIMES:", instruction.times)

            print()
