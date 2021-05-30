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
        self.walking_frames_l_0 = []
        self.walking_frames_r_0 = []

        self.walking_frames_l_1 = []
        self.walking_frames_r_1 = []

        self.direction = "R"
        self.image = None
        self.rect = None

    def construct_animation(self):
        x = 0
        y = 0
        w = Constants.FROG_SPRITE_WIDTH // 14
        h = Constants.FROG_SPRITE_HEIGHT // 2
        sprite_sheet = SpriteSheet("game_engine/sprites/ranita_resized.png")

        # TODO: turn images on left frames
        for _ in range(14):
            image = sprite_sheet.get_image(x, y, w, h)
            self.walking_frames_r_0.append(image)
            self.walking_frames_l_0.append(image)

            image = sprite_sheet.get_image(x, y + 50, w, h)
            self.walking_frames_r_1.append(image)
            self.walking_frames_l_1.append(image)

            x += w

        self.image = self.walking_frames_r_0[0]
        self.rect = self.image.get_rect()

    def move_down(self, times):
        movement = self.__speed * int(times)
        if self.y + self.height + movement <= Constants.DISPLAY_HEIGHT:
            self.y += movement
            self.rect.y = self.y

    def move_up(self, times):
        movement = self.__speed * int(times)
        if self.y - movement >= 0:
            self.y -= movement
            self.rect.y = self.y

    def move_right(self, times):
        movement = self.__speed * int(times)
        if self.x + self.width + movement <= Constants.DISPLAY_WIDTH:
            self.x += movement
            self.rect.x = self.x

    def move_left(self, times):
        movement = self.__speed * int(times)
        if self.x - self.__speed >= 0:
            self.x -= movement
            self.rect.x = self.x

    # TODO: Return when hat quadruple is finished
    def change_hat(self, hat_id):
        self.hat = int(hat_id)
