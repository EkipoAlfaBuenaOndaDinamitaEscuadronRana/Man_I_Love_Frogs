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

    def __print_quads(self, pre_quads):
        if pre_quads:
            print("Program Quads before assignations:")
            print("-------------------------------------")
            print(self.pretty_quads)
        else:
            print("Program Quads after assignations:")
            for q in self.quads:
                print("--{}----------------------------------".format(q))
                self.quads[q].print_quad()
            print("-------------------------------------")

    def __print_instructions(self, instructions):
        print("\nResulting Instructions:")
        print("-------------------------------------")
        Instruction.print_instructions(instructions)

    def __print_running(self):
        print("Running: {}".format(self.running_file))
        print("-------------------------------------")

    def run(self, **kwargs):
        if kwargs.get("print_pre_quads"):
            self.__print_quads(True)

        vm = VirtualMachine(3000, 1000, 6000, self.function_table)
        # vm.quadruple_direction_allocator(self.quads)

        if kwargs.get("print_post_quads"):
            self.__print_quads(False)

        if kwargs.get("print_running"):
            self.__print_running()

        instructions = vm.run(self.quads)

        if kwargs.get("print_instructions"):
            self.__print_instructions(instructions)

        if kwargs.get("run_game") and len(instructions):
            characters = {
                "pepe": Character(0, 0, 30, 30, 50),
            }

            Engine.start(characters, instructions)

        return instructions
