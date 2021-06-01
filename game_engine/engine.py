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


class Engine:
    __display_width = Constants.DISPLAY_WIDTH
    __display_height = Constants.DISPLAY_HEIGHT
    __speed = Constants.SPEED

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

        elif movement == "HAT":
            x, y = character.change_hat(times, board)

        else:
            return

        # update_board(board, character, x, y)

    def update_board(board, character, x, y):
        for row in board:
            for space in row:
                if space == character:
                    space = None

        board[x][y] = character

    def print_board(board):
        for row in board:
            for space in row:
                if space == None:
                    print(space, end=" ")
                else:
                    print("Frog", end=" ")
            print()
        print()

    def build_characters(characters):
        active_sprite_list = pygame.sprite.Group()
        for c in characters:
            character = characters[c]
            character.construct_animation()
            character.rect.x = character.x
            character.rect.y = character.y
            active_sprite_list.add(character)

        return active_sprite_list

    def init_game(characters):
        cols = Constants.DISPLAY_WIDTH // Constants.FROG_WIDTH - 1
        rows = Constants.DISPLAY_HEIGHT // Constants.FROG_HEIGHT - 1

        board = [[None for x in range(cols)] for i in range(rows)]

        for c in characters:
            character = characters[c]

            char_x = character.x // Constants.FROG_WIDTH
            char_y = character.y // Constants.FROG_HEIGHT

            character.board_x = char_x
            character.board_y = char_y

            board[char_y][char_x] = character

        return board

    def check_if_quit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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
        pygame.display.set_caption("Man I Love Frogs")

        active_sprite_list = Engine.build_characters(characters)
        board = Engine.init_game(characters)
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

            pygame.display.update()
