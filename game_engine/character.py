from router_solver import *
import game_engine.constants
from game_engine.constants import *


class Character(object):
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__speed = speed
        self.curr_frame = 0

    def move_down(self, times):
        movement = self.__speed * int(times)
        if self.y + self.height + movement <= Constants.DISPLAY_HEIGHT:
            self.y += movement

    def move_up(self, times):
        movement = self.__speed * int(times)
        if self.y - movement >= 0:
            self.y -= movement

    def move_right(self, times):
        movement = self.__speed * int(times)
        if self.x + self.width + movement <= Constants.DISPLAY_WIDTH:
            self.x += movement

    def move_left(self, times):
        movement = self.__speed * int(times)
        if self.x - self.__speed >= 0:
            self.x -= movement

    # TODO: Return when hat quadruple is finished
    def change_hat(self, sprite_name):
        pass
