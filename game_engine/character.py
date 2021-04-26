class Character(object):
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__speed = speed

    def moversePaAbajito(self, display_height):
        if self.y + self.height + self.__speed <= display_height:
            self.y += self.__speed

    def moversePaRribita(self):
        if self.y - self.__speed >= 0:
            self.y -= self.__speed

    def moversePaLaDerecha(self, display_width):
        if self.x + self.width + self.__speed <= display_width:
            self.x += self.__speed

    def moversePaLaIzquierda(self):
        if self.x - self.__speed >= 0:
            self.x -= self.__speed
