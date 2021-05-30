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

    def instruction_movement(instruction, characters):
        character = characters[instruction.character_name]
        movement = instruction.movement
        times = instruction.times

        if movement == "JD":
            character.move_down(times)

        elif movement == "JU":
            character.move_up(times)

        elif movement == "JR":
            character.move_right(times)

        elif movement == "JL":
            character.move_left(times)

        elif movement == "HAT":
            character.change_hat(times)

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

        while True:
            Engine.check_if_quit()
            clock.tick(Engine.__speed)
            active_sprite_list.update()
            display.fill(Constants.BLUE)
            active_sprite_list.draw(display)

            # for character in characters.values():
            #     pygame.draw.rect(
            #         display,
            #         Constants.WHITE,
            #         (character.x, character.y, character.width, character.height),
            #     )

            if len(instructions):
                Engine.instruction_movement(instructions.pop(0), characters)

            pygame.display.update()

characters = {
    "Rosita Fresita": Character(0, 0, Constants.FROG_WIDTH, Constants.FROG_HEIGHT, 50),
    "Dino Adrian": Character(0, 100, Constants.FROG_WIDTH, Constants.FROG_HEIGHT, 50),
}

instructions = [
    Instruction("Rosita Fresita", "JR", 29),
    Instruction("Rosita Fresita", "JD", 17),
    # Instruction("Rosita Fresita", "JR", 1),
    # Instruction("Rosita Fresita", "JR", 2),
    # Instruction("Rosita Fresita", "JR", 3),
    Instruction("Dino Adrian", "JD", 1),
    # Instruction("Dino Adrian", "JD", 2),
    # Instruction("Dino Adrian", "JD", 1),
]

Engine.start(characters, instructions)
