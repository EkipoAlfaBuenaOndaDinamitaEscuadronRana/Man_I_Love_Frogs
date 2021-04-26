import pygame
from character import *

pygame.init()

clock = pygame.time.Clock()
speed = 30

display_width = 500
display_height = 300

characters = [
    #         x  y   width height speed
    Character(0, 0,  30,   30,    10),
    Character(0, 50, 30,   30,    10)
]

def userMoves(character, pressed_key):
    if pressed_key[pygame.K_DOWN] or pressed_key[pygame.K_s]:
        character.move_down(display_height)

    if pressed_key[pygame.K_UP] or pressed_key[pygame.K_w]:
        character.move_up()

    if pressed_key[pygame.K_RIGHT] or pressed_key[pygame.K_d]:
        character.move_right(display_width)

    if pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_a]:
        character.move_left()

def checkIfUserQuit(pressed_key):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if pressed_key[pygame.K_p]:
        pygame.quit()

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Super compi que no tiene nombre todavia")

while True:
    clock.tick(speed)
    pressed_key = pygame.key.get_pressed()
    
    checkIfUserQuit(pressed_key)

    for character in characters:
        userMoves(character, pressed_key)

    display.fill((0, 0, 0))

    for character in characters:
        pygame.draw.rect(display, (255, 255, 255), (character.x, character.y, character.width, character.height))

    pygame.display.update()
