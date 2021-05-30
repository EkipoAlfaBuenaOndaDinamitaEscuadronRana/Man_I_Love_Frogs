import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from router_solver import *
import pygame
import game_engine.character
from game_engine.character import *
import game_engine.instruction
from game_engine.instruction import *


class Engine:
    __display_width = 500
    __display_height = 500
    __speed = 3

    def instruction_movement(instruction, characters):
        character = characters[instruction.character_name]
        movement = instruction.movement
        times = instruction.times

        if movement == "JD":
            character.move_down(Engine.__display_height, times)

        if movement == "JU":
            character.move_up(times)

        if movement == "JR":
            character.move_right(Engine.__display_width, times)

        if movement == "JL":
            character.move_left(times)

    """
    characters = {
        "Rosita Fresita": Character(0, 0, 30, 30, 50),
        "Dino Adrian": Character(0, 50, 30, 30, 50),
    }

    instructions = [
        Instruction("Rosita Fresita", "JR", 1),
        Instruction("Dino Adrian", "JD", 1),
    ]
    """

    def start(characters, instructions):
        pygame.init()

        clock = pygame.time.Clock()

        display = pygame.display.set_mode(
            (Engine.__display_width, Engine.__display_height)
        )
        pygame.display.set_caption("Super compi que no tiene nombre todavia")

        while True:
            clock.tick(Engine.__speed)

            if len(instructions):
                Engine.instruction_movement(instructions.pop(0), characters)

            display.fill((0, 0, 0))

            for character in characters.values():
                pygame.draw.rect(
                    display,
                    (255, 255, 255),
                    (character.x, character.y, character.width, character.height),
                )

            pygame.display.update()
