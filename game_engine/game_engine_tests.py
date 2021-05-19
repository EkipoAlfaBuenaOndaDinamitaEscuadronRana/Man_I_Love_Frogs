"""
Para correr el archivo, usar este comando
python3 -m unittest game_engine_tests.py
"""
import game_engine.engine
from game_engine.engine import *
import unittest


class TestEngine(unittest.TestCase):
    def test_instruction_movement(self):
        characters = {"pikachu": Character(0, 50, 30, 30, 50)}
        instructions = [
            Instruction("pikachu", "down"),
            Instruction("pikachu", "up"),
            Instruction("pikachu", "right"),
            Instruction("pikachu", "left"),
        ]

        # Starting on point x = 0 and y = 50
        self.assertEqual(characters["pikachu"].y, 50)

        # Moving down
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].y, 100)

        # Moving up
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].y, 50)

        # Moving right
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].x, 50)

        # Moving left
        Engine.instruction_movement(instructions.pop(0), characters)
        self.assertEqual(characters["pikachu"].x, 0)


class TestCharacter(unittest.TestCase):
    def test_move_down(self):
        character = Character(0, 50, 30, 30, 50)
        display_height = 500

        self.assertEqual(character.y, 50)
        character.move_down(display_height)
        self.assertEqual(character.y, 100)

    def test_move_up(self):
        character = Character(0, 50, 30, 30, 50)

        self.assertEqual(character.y, 50)
        character.move_up()
        self.assertEqual(character.y, 0)

    def test_move_right(self):
        character = Character(0, 50, 30, 30, 50)
        display_width = 500

        self.assertEqual(character.x, 0)
        character.move_right(display_width)
        self.assertEqual(character.x, 50)

    def test_move_left(self):
        character = Character(50, 50, 30, 30, 50)

        self.assertEqual(character.x, 50)
        character.move_left()
        self.assertEqual(character.x, 0)
