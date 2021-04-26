import pygame

pygame.init()

clock = pygame.time.Clock()
speed = 30

display_width = 500
display_height = 300

character_x = 10
character_y = 10
character_width = 30
character_height = 30

def moversePaAbajito():
    global character_y, character_height, display_height
    if character_y + character_height + 10 <= display_height:
        character_y += 10

def moversePaRribita():
    global character_y
    if character_y - 10 >= 0:
            character_y -= 10

def moversePaLaDerecha():
    global character_x, character_width, display_width
    if character_x + character_width + 10 <= display_width:
        character_x += 10

def moversePaLaIzquierda():
    global character_x
    if character_x - 10 >= 0:
        character_x -= 10

def userMoves(pressed_key):
    if pressed_key[pygame.K_DOWN] or pressed_key[pygame.K_s]:
        moversePaAbajito()

    if pressed_key[pygame.K_UP] or pressed_key[pygame.K_w]:
        moversePaRribita()

    if pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_a]:
        moversePaLaIzquierda()

    if pressed_key[pygame.K_RIGHT] or pressed_key[pygame.K_d]:
        moversePaLaDerecha()

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

    userMoves(pressed_key)
    checkIfUserQuit(pressed_key)   

    display.fill((0, 0, 0))
    pygame.draw.rect(display, (255, 255, 255), (character_x, character_y, character_width, character_height))

    pygame.display.update()
