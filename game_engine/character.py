from router_solver import *
import game_engine.constants
from game_engine.constants import *
from game_engine.spritesheet import *


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.__speed = speed

        self.board_x = None
        self.board_y = None

        self.hat = 0

        self.walking_frames = {
            0: {
                "R": [],
                "L": [],
            },
            1: {
                "R": [],
                "L": [],
            },
        }

        self.moving = False
        self.sprite_direction = "R"
        self.jump_image = 0
        self.image = None
        self.rect = None

    def construct_animation(self):
        x = 1
        y = 1
        w = Constants.FROG_SPRITE_WIDTH // Constants.FROG_SPRITE_NUMBER
        h = Constants.FROG_SPRITE_HEIGHT // Constants.FROG_HATS_NUMBER
        sprite_sheet = SpriteSheet(Constants.FROG_IMAGE)

        # TODO: turn images on left frames
        for _ in range(14):
            image = sprite_sheet.get_image(x, y, w, h)
            self.walking_frames[0]["L"].append(image)
            self.walking_frames[0]["R"].append(image)

            image = sprite_sheet.get_image(x, y + 50, w, h)
            self.walking_frames[1]["R"].append(image)
            self.walking_frames[1]["L"].append(image)

            x += w

        self.image = self.walking_frames[self.hat][self.sprite_direction][0]
        self.rect = self.image.get_rect()

    def update(self):
        if self.moving:
            self.image = self.walking_frames[self.hat][self.sprite_direction][
                self.jump_image
            ]
            if self.jump_image < 13:
                self.jump_image += 1
            else:
                self.jump_image = 0
                self.moving = False

    def available_position(self, board, x, y):
        fixed_x = x // Constants.FROG_WIDTH
        fixed_y = y // Constants.FROG_HEIGHT
        position = board[fixed_y][fixed_x]

        print(fixed_x, ",", fixed_y)
        print(position)

        if position == None:
            return True

        elif type(position) == Character:
            return False

        elif position.type == "Fly":
            position.eaten = True
            return True

        return False

    def fix_return_board_position(self):
        x = self.x // Constants.FROG_WIDTH
        y = self.y // Constants.FROG_HEIGHT
        return [x, y]


    def move_down(self, times, board):
        times = int(times)
        movement = self.height * times
        new_y = self.y + movement
        is_available = self.available_position(board, self.x, new_y)
        print(is_available)
        if self.y + self.height + movement <= Constants.DISPLAY_HEIGHT:
            self.y += movement
            self.rect.y = self.y
            self.moving = True

        return self.fix_return_board_position()

    def move_up(self, times, board):
        times = int(times)
        movement = self.height * times
        new_y = self.y - movement
        is_available = self.available_position(board, self.x, new_y)
        if self.y - movement >= 0 and is_available:
            self.y -= movement
            self.rect.y = self.y
            self.moving = True

        return self.fix_return_board_position()

    def move_right(self, times, board):
        times = int(times)
        movement = self.width * times
        new_x = self.x + movement
        is_available = self.available_position(board, new_x, self.y)
        print(is_available)
        if self.x + self.width + movement <= Constants.DISPLAY_WIDTH and is_available:
            self.x += movement
            self.rect.x = self.x
            self.moving = True

        return self.fix_return_board_position()

    def move_left(self, times, board):
        times = int(times)
        movement = self.width * times
        new_x = self.x - movement
        is_available = self.available_position(board, new_x, self.y)
        if self.x - self.width - movement >= 0 and is_available:
            self.x -= movement
            self.rect.x = self.x
            self.moving = True

        return self.fix_return_board_position()

    def change_hat(self, hat_id):
        self.hat = int(hat_id)
        return hat in [0, 1]
