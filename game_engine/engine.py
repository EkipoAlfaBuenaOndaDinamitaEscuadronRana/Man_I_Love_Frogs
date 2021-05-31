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


class Engine:
    __display_width = Constants.DISPLAY_WIDTH
    __display_height = Constants.DISPLAY_HEIGHT
    __speed = Constants.SPEED
    __flys = 0

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

        Engine.update_board(board, character, x, y)

    def update_board(board, character, x, y):
        for i in range(len(board)):
            for j in range(len(board[i])):
                space = board[i][j]
                if space == character:
                    board[i][j] = None
                elif type(space) == Item:
                    if space.eaten:
                        board[i][j] = None
                        Engine.__flys -= 1

        board[y][x] = character
        Engine.print_board(board)

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

    def build_items():
        return [
            Item(150, 0, 50, 50, "Rock"),
            Item(150, 500, 50, 50, "Fly"),
        ]

    def build_characters_and_items(characters, items):
        active_sprite_list = pygame.sprite.Group()
        for item in items:
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

    def init_game(characters, items):
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

        for item in items:
            item_x = item.board_x
            item_y = item.board_y
            board[item_y][item_x] = item

        return board

    def check_if_quit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    """
    characters = {
        "Rosita Fresita": Character(0, 0, 50, 50, 50),
        "Dino Adrian": Character(0, 50, 50, 50, 50),
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

        items = Engine.build_items()
        active_sprite_list = Engine.build_characters_and_items(characters, items)
        board = Engine.init_game(characters, items)
        Engine.print_board(board)
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
                print("GANAMOS")

            pygame.display.update()


characters = {
    "Rosita Fresita": Character("Rosita Fresita", 0, 0, 50, 50, 50),
    "Dino Adrian": Character("Dino Adrian", 0, 50, 50, 50, 50),
}

instructions = [
    Instruction("Rosita Fresita", "JR", 1),
    Instruction("Rosita Fresita", "JR", 3),
    Instruction("Rosita Fresita", "JD", 10),
    Instruction("Rosita Fresita", "JL", 1),
    # Instruction("Rosita Fresita", "JU", 1),
    # Instruction("Rosita Fresita", "JU", 1),
    # Instruction("Rosita Fresita", "JU", 1),
    # Instruction("Rosita Fresita", "JL", 1),
    # Instruction("Rosita Fresita", "JL", 1),
    # Instruction("Rosita Fresita", "JL", 1),
    # Instruction("Rosita Fresita", "JL", 1),
    # Instruction("Rosita Fresita", "JR", 2),
    # Instruction("Rosita Fresita", "JR", 2),
    # Instruction("Rosita Fresita", "JR", 1),
    # Instruction("Rosita Fresita", "JR", 1),
    # Instruction("Rosita Fresita", "JR", 3),
    # Instruction("Rosita Fresita", "JD", 1),
    # Instruction("Rosita Fresita", "JD", 1),
    # Instruction("Rosita Fresita", "JD", 2),
    # Instruction("Rosita Fresita", "JD", 1),
    # Instruction("Rosita Fresita", "JD", 21),
    # Instruction("Rosita Fresita", "JD", 1),
    # Instruction("Rosita Fresita", "JD", 1),
    # Instruction("Dino Adrian", "JD", 1),
]


Engine.start(characters, instructions)
