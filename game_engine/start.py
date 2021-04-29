import pygame
from character import *
from instruction import *


class Engine:
    __display_width = 500
    __display_height = 500
    __speed = 3

    # TODO: This method is only used for testing. Remove if necesary
    def userMoves(character, pressed_key):
        if pressed_key[pygame.K_DOWN] or pressed_key[pygame.K_s]:
            character.move_down(Engine.__display_height)

        if pressed_key[pygame.K_UP] or pressed_key[pygame.K_w]:
            character.move_up()

        if pressed_key[pygame.K_RIGHT] or pressed_key[pygame.K_d]:
            character.move_right(Engine.__display_width)

        if pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_a]:
            character.move_left()

    def instructionMoves(instruction):
        character = name_characters[instruction.character_name]
        movement = instruction.movement

        if movement == "down":
            character.move_down(Engine.__display_height)

        if movement == "up":
            character.move_up()

        if movement == "right":
            character.move_right(Engine.__display_width)

        if movement == "left":
            character.move_left()

    def checkIfUserQuit(pressed_key):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if pressed_key[pygame.K_p]:
            pygame.quit()

    def start(characters, name_characters, instructions):
        pygame.init()

        clock = pygame.time.Clock()

        display = pygame.display.set_mode(
            (Engine.__display_width, Engine.__display_height)
        )
        pygame.display.set_caption("Super compi que no tiene nombre todavia")

        while True:
            clock.tick(Engine.__speed)
            pressed_key = pygame.key.get_pressed()

            Engine.checkIfUserQuit(pressed_key)

            if len(instructions):
                Engine.instructionMoves(instructions.pop(0))

            display.fill((0, 0, 0))

            for character in characters:
                pygame.draw.rect(
                    display,
                    (255, 255, 255),
                    (character.x, character.y, character.width, character.height),
                )

            pygame.display.update()


# TODO: Todas estas instrucciones y personajes son ejemplos
#       Debe ser borrado al momento de entrar a producción
obj_characters = [
    #         x  y   width height speed
    Character(0, 0, 30, 30, 50),
    Character(0, 50, 30, 30, 50),
]

name_characters = {
    "Rosita Fresita": obj_characters[0],
    "Dino Adrian": obj_characters[1],
}

instructions = [
    #           name              movement
    Instruction("Rosita Fresita", "right"),
    Instruction("Rosita Fresita", "right"),
    Instruction("Rosita Fresita", "right"),
    Instruction("Rosita Fresita", "right"),
    Instruction("Rosita Fresita", "right"),
    Instruction("Rosita Fresita", "down"),
    Instruction("Dino Adrian", "down"),
    Instruction("Dino Adrian", "down"),
    Instruction("Dino Adrian", "down"),
    Instruction("Dino Adrian", "down"),
    Instruction("Dino Adrian", "down"),
    Instruction("Dino Adrian", "right"),
]

Engine.start(obj_characters, name_characters, instructions)
