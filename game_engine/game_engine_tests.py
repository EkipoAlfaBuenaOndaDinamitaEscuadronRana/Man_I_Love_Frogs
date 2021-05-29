from router_solver import *
import game_engine.engine
from game_engine.engine import *
from execute import *
import execute
import unittest


class TestEngine(unittest.TestCase):
    def test_instruction_movement(self):
        characters = {"pikachu": Character(100, 100, 30, 30, 50)}
        instructions = [
            Instruction("pikachu", "JD", 3),
            Instruction("pikachu", "JU", 5),
            Instruction("pikachu", "JR", 1),
            Instruction("pikachu", "JL", 3),
        ]

        # Starting on point x = 100 and y = 100
        self.assertEqual(characters["pikachu"].x, 100)
        self.assertEqual(characters["pikachu"].y, 100)

        # Moving down
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].y, 250)

        # Moving up
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].y, 0)

        # Moving right
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].x, 150)

        # Moving left
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].x, 0)


class TestCharacter(unittest.TestCase):
    def test_move_down(self):
        character = Character(0, 50, 30, 30, 50)
        display_height = 500

        self.assertEqual(character.y, 50)
        character.move_down(display_height, 1)
        self.assertEqual(character.y, 100)

    def test_move_up(self):
        character = Character(0, 50, 30, 30, 50)

        self.assertEqual(character.y, 50)
        character.move_up(1)
        self.assertEqual(character.y, 0)

    def test_move_right(self):
        character = Character(0, 50, 30, 30, 50)
        display_width = 500

        self.assertEqual(character.x, 0)
        character.move_right(display_width, 1)
        self.assertEqual(character.x, 50)

    def test_move_left(self):
        character = Character(50, 50, 30, 30, 50)

        self.assertEqual(character.x, 50)
        character.move_left(1)
        self.assertEqual(character.x, 0)
