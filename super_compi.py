import sys
import compilador.helpers.file_parser
import compilador.vm.virtual_machine
from compilador.helpers.file_parser import *
from compilador.vm.virtual_machine import *

if len(sys.argv) > 1:
    i = 1
    while i < len(sys.argv):
        print(sys.argv[i])
        data = parser_file(sys.argv[i])
        print(data["str"])
        # vm = VirtualMachine(3000, 1000, 6000, data['ft'])
        # vm.quadruple_direction_allocator(data['q'])
        # vm.run(data['q'])
        i += 1
else:
    running_file = "compilador/tests/test_12.txt"
    print("DEFAULT: {}".format(running_file))
    data = parser_file(running_file)
    print(data["str"])

    quads = data["q"]

    vm = VirtualMachine(3000, 1000, 6000, data["ft"])

    # Quadruple.print_quads(quads, "pre")
    vm.quadruple_direction_allocator(quads)
    # Quadruple.print_quads(quads, "post")
    instructions = vm.run(quads)
    Instruction.print_instructions(instructions)
