from router_solver import *


class Character(object):
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__speed = speed

    def move_down(self, display_height, times):
        movement = self.__speed * int(times)
        if self.y + self.height + movement <= display_height:
            self.y += movement

    def move_up(self, times):
        movement = self.__speed * int(times)
        if self.y - movement >= 0:
            self.y -= movement

    def move_right(self, display_width, times):
        movement = self.__speed * int(times)
        if self.x + self.width + movement <= display_width:
            self.x += movement

    def move_left(self, times):
        movement = self.__speed * int(times)
        if self.x - self.__speed >= 0:
            self.x -= movement
