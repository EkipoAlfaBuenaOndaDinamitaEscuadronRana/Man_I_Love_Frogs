import pygame
from character import *
from instruction import *

pygame.init()

clock = pygame.time.Clock()
speed = 3

display_width = 500
display_height = 500

obj_characters = [
    #         x  y   width height speed
    Character(0, 0,  30,   30,    50),
    Character(0, 50, 30,   30,    50)
]

name_characters = {
    'Rosita Fresita': obj_characters[0],
    'Dino Adrian': obj_characters[1]
}

instructions = [
    #           name              movement
    Instruction('Rosita Fresita', 'right'),
    Instruction('Rosita Fresita', 'right'),
    Instruction('Rosita Fresita', 'right'),
    Instruction('Rosita Fresita', 'right'),
    Instruction('Rosita Fresita', 'right'),
    Instruction('Rosita Fresita', 'down'),
    Instruction('Dino Adrian',    'down'),
    Instruction('Dino Adrian',    'down'),
    Instruction('Dino Adrian',    'down'),
    Instruction('Dino Adrian',    'down'),
    Instruction('Dino Adrian',    'down'),
    Instruction('Dino Adrian',    'right')
]

# TODO: This method is only used for testing. Remove if necesary
def userMoves(character, pressed_key):
    if pressed_key[pygame.K_DOWN] or pressed_key[pygame.K_s]:
        character.move_down(display_height)

    if pressed_key[pygame.K_UP] or pressed_key[pygame.K_w]:
        character.move_up()

    if pressed_key[pygame.K_RIGHT] or pressed_key[pygame.K_d]:
        character.move_right(display_width)

    if pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_a]:
        character.move_left()

def instructionMoves(instruction):
    character = name_characters[instruction.character_name]
    movement = instruction.movement

    if movement == 'down':
        character.move_down(display_height)

    if movement == 'up':
        character.move_up()

    if movement == 'right':
        character.move_right(display_width)

    if movement == 'left':
        character.move_left()

def checkIfUserQuit(pressed_key):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if pressed_key[pygame.K_p]:
        pygame.quit()

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Super compi que no tiene nombre todavia')

while True:
    clock.tick(speed)
    pressed_key = pygame.key.get_pressed()

    checkIfUserQuit(pressed_key)

    if len(instructions):
        instructionMoves(instructions.pop(0))

    display.fill((0, 0, 0))

    for character in obj_characters:
        pygame.draw.rect(display, (255, 255, 255), (character.x, character.y, character.width, character.height))

    pygame.display.update()
