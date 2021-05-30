from router_solver import *
import game_engine.constants
from game_engine.constants import *
from spritesheet import *


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.x = x
        self.y = y

        self.board_x = None
        self.board_y = None

        self.width = width
        self.height = height
        self.__speed = speed

        self.hat = 0
        self.curr_frame = 0
        self.__move_count = 0

        self.walking_frames = {
          0: {
            "R": [],
            "L": [],
          },

          1: {
            "R": [],
            "L": [],
          }
        }

        self.curr_state = "moving"
        self.sprite_direction = "R"
        self.curr_direction = None
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
        if self.curr_state == "moving":
            self.image = self.walking_frames[self.hat][self.sprite_direction][self.jump_image]
            if self.jump_image < 13:
                self.jump_image += 1
            else:
                self.jump_image = 0
                self.curr_state = "not_moving"

    def move_down(self, times):
        times = int(times)
        movement = self.height * times
        if self.y + self.height + movement <= Constants.DISPLAY_HEIGHT:
            self.y += movement
            self.rect.y = self.y
            return True
        return False

    def move_up(self, times):
        times = int(times)
        movement = self.height * times
        if self.y - movement >= 0:
            self.y -= movement
            self.rect.y = self.y
            return True
        return False

    def move_right(self, times):
        times = int(times)
        movement = self.width * times
        if self.x + self.width + movement <= Constants.DISPLAY_WIDTH:
            self.x += movement
            self.rect.x = self.x
            return True
        return False

    def move_left(self, times):
        times = int(times)
        movement = self.width * times
        if self.x - self.width - movement >= 0:
            self.x -= movement
            self.rect.x = self.x
            return True
        return False

    # TODO: Return when hat quadruple is finished
    def change_hat(self, hat_id):
        self.hat = int(hat_id)
