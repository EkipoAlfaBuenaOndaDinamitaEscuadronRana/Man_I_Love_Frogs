import sys
import compilador.helpers.file_parser
from compilador.helpers.file_parser import *
import compilador.vm.virtual_machine
from compilador.vm.virtual_machine import *
import game_engine.engine
from game_engine.engine import *


class Executer(object):
    def __init__(self, running_file):
        self.running_file = running_file
        self.data = parser_file(running_file)
        self.quads = self.data["q"]
        self.pretty_quads = self.data["str"]
        self.function_table = self.data["ft"]

    def run(self, **kwargs):
        if kwargs.get("print_quads"):
            print("Program Quads:")
            print("-------------------------------------")
            print(self.pretty_quads)

        vm = VirtualMachine(3000, 1000, 6000, self.function_table)
        vm.quadruple_direction_allocator(self.quads)

        print("Running: {}".format(self.running_file))
        print("-------------------------------------")
        instructions = vm.run(self.quads)

        if kwargs.get("print_instructions"):
            print("\nResulting Instructions:")
            print("-------------------------------------")
            Instruction.print_instructions(instructions)

        if len(instructions):
            characters = {
                "pepe": Character(100, 100, 30, 30, 50),
            }

            Engine.start(characters, instructions)


Executer("compilador/tests/test_12.milf").run(print_quads=True, print_instructions=True)
