from router_solver import *


class Character(object):
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__speed = speed

    # TODO: Calculate this correctly
    def move_down(self, display_height, times):
        if self.y + self.height + self.__speed <= display_height:
            self.y += self.__speed

    def move_up(self, times):
        if self.y - self.__speed >= 0:
            self.y -= self.__speed

    def move_right(self, display_width, times):
        if self.x + self.width + self.__speed <= display_width:
            self.x += self.__speed

    def move_left(self, times):
        if self.x - self.__speed >= 0:
            self.x -= self.__speed
