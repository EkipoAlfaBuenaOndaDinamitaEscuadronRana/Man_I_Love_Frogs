import pygame
import game_engine.character
import game_engine.instruction
from game_engine.character import *
from game_engine.instruction import *


class Engine:
    __display_width = 500
    __display_height = 500
    __speed = 3

    def instruction_movement(instruction, characters):
        character = characters[instruction.character_name]
        movement = instruction.movement

        if movement == "down":
            character.move_down(Engine.__display_height)

        if movement == "up":
            character.move_up()

        if movement == "right":
            character.move_right(Engine.__display_width)

        if movement == "left":
            character.move_left()

    """
    characters = {
        "Rosita Fresita": Character(0, 0, 30, 30, 50),
        "Dino Adrian": Character(0, 50, 30, 30, 50),
    }

    instructions = [
        Instruction("Rosita Fresita", "right"),
        Instruction("Dino Adrian", "down")
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
