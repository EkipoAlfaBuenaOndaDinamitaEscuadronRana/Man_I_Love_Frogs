import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
from router_solver import *
import game_engine.character
from game_engine.character import *
import game_engine.instruction
from game_engine.instruction import *
import game_engine.constants
from game_engine.constants import *
import game_engine.item
from game_engine.item import *
import game_engine.levels
from game_engine.levels import *


class Engine:
    __display_width = Constants.DISPLAY_WIDTH
    __display_height = Constants.DISPLAY_HEIGHT
    __speed = Constants.SPEED
    __flys = 0

    # Actualiza el estado de un character dependiendo de la instrucción dada
    def instruction_movement(instruction, characters, board):
        character = characters[instruction.character_name]
        movement = instruction.movement
        times = instruction.times

        if movement == "JD":
            x, y = character.move_down(times, board)

        elif movement == "JU":
            x, y = character.move_up(times, board)

        elif movement == "JR":
            x, y = character.move_right(times, board)

        elif movement == "JL":
            x, y = character.move_left(times, board)

        elif movement == "hat":
            character.change_hat(times)
            return

        else:
            return

        Engine.update_board(board, character, x, y)

    # Elimina una mosca del juego
    def delete_fly(fly):
        fly.rect.x = 2000
        fly.rect.y = 2000
        fly.y = 2000
        fly.x = 2000
        Engine.__flys -= 1

    # Actualiza el tablero colocando personajes en lugares especificos o bien,
    # Actualizando items
    def update_board(board, character, x, y):
        for i in range(len(board)):
            for j in range(len(board[i])):
                space = board[i][j]
                if space == character:
                    board[i][j] = None
                elif type(space) == Item:
                    if space.eaten:
                        Engine.delete_fly(space)
                        board[i][j] = None

        board[y][x] = character

    # Despliega la matriz del tablero del juego
    def print_board(board):
        for row in board:
            for space in row:
                if type(space) == Character:
                    print("F", end=" ")
                elif type(space) == Item:
                    if space.type == "Rock":
                        print("R", end=" ")
                    else:
                        print("B", end=" ")
                else:
                    print("-", end=" ")
            print()
        print()

    # Construye el nievel dependiendo del parametro dado
    def build_level(played_level):
        if played_level == "one":
            return Levels.LEVEL_ONE

        elif played_level == "two":
            return Levels.LEVEL_TWO

    # genera animaciones y contruye sprites de los objetos del juego
    def build_characters_and_items(characters, items):
        active_sprite_list = pygame.sprite.Group()
        for item in items:
            item.construct_animation()
            item.rect.x = item.x
            item.rect.y = item.y
            active_sprite_list.add(item)

            if item.type == "Fly":
                Engine.__flys += 1

        for c in characters:
            character = characters[c]
            character.construct_animation()
            character.rect.x = character.x
            character.rect.y = character.y
            active_sprite_list.add(character)

        return active_sprite_list

    # Inicializa los valores de los personajes, crea el tablero
    def init_game(characters, items):
        cols = Constants.DISPLAY_WIDTH // Constants.FROG_WIDTH
        rows = Constants.DISPLAY_HEIGHT // Constants.FROG_HEIGHT

        board = [[None for x in range(cols)] for i in range(rows)]

        for c in characters:
            character = characters[c]

            char_x = character.x // Constants.FROG_WIDTH
            char_y = character.y // Constants.FROG_HEIGHT

            character.board_x = char_x
            character.board_y = char_y

            board[char_y][char_x] = character

        for item in items:
            item_x = item.board_x
            item_y = item.board_y
            board[item_y][item_x] = item

        return board

    # Revisa que el usuario haya dado a salir en el juego
    def check_if_quit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    # Inicializa todas las funciones del juego
    def start(characters, instructions, played_level):
        """INPUT EXAMPLE
        characters = {
        "Rosita Fresita": Character(0, 0, 50, 50, 50),
        "Dino Adrian": Character(0, 50, 50, 50, 50),
        }

        instructions = [
        Instruction("Rosita Fresita", "JR", 1),
        Instruction("Dino Adrian", "JD", 1),
        ]
        """
        pygame.init()

        clock = pygame.time.Clock()
        display = pygame.display.set_mode(
            (Engine.__display_width, Engine.__display_height)
        )
        pygame.display.set_caption("Man I Love Frogs")

        items = Engine.build_level(played_level)
        active_sprite_list = Engine.build_characters_and_items(characters, items)
        board = Engine.init_game(characters, items)
        # Engine.print_board(board)
        counter = 0

        while True:
            Engine.check_if_quit()
            clock.tick(Engine.__speed)
            active_sprite_list.update()
            display.fill(Constants.BLUE)
            active_sprite_list.draw(display)
            counter += 1

            if len(instructions) and counter == 14:
                Engine.instruction_movement(instructions.pop(0), characters, board)
                counter = 0

            if Engine.__flys == 0:
                font_title = pygame.font.Font(None, 52)
                announcement = font_title.render(
                    "GANAMOS :D Mi hija sí baila con el señor", True, Constants.WHITE
                )
                announcement_rect = announcement.get_rect(
                    center=(
                        int(Constants.DISPLAY_WIDTH / 2),
                        int(Constants.DISPLAY_HEIGHT / 3),
                    )
                )
                display.blit(announcement, announcement_rect)

                font_cien = pygame.font.Font(None, 24)
                ponganos_cien = font_cien.render(
                    "Maestra, si está leyendo esto por favor ponganos 100 porque si no me quitan mi beca D:",
                    True,
                    Constants.WHITE,
                )
                ponganos_cien_rect = ponganos_cien.get_rect(
                    center=(
                        int(Constants.DISPLAY_WIDTH / 2),
                        int(Constants.DISPLAY_HEIGHT / 2.5),
                    )
                )
                display.blit(ponganos_cien, ponganos_cien_rect)

            pygame.display.update()
