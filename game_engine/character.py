class Character(object):
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__speed = speed

    def move_down(self, display_height):
        if self.y + self.height + self.__speed <= display_height:
            self.y += self.__speed

    def move_up(self):
        if self.y - self.__speed >= 0:
            self.y -= self.__speed

    def move_right(self, display_width):
        if self.x + self.width + self.__speed <= display_width:
            self.x += self.__speed

    def move_left(self):
        if self.x - self.__speed >= 0:
            self.x -= self.__speed
