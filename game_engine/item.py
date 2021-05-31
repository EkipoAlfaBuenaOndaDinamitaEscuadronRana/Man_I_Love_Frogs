from router_solver import *
import game_engine.constants
from game_engine.constants import *
from game_engine.spritesheet import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type):
        super().__init__()

        self.x = x
        self.y = y
        self.type = type
        self.width = width
        self.height = height
        self.eaten = False

        self.board_x = self.x // Constants.ITEM_WIDTH
        self.board_y = self.y // Constants.ITEM_HEIGHT

        if type == "Rock":
            sprite_sheet = SpriteSheet(Constants.ROCK_IMAGE)
        elif type == "Fly":
            sprite_sheet = SpriteSheet(Constants.FLY_IMAGE)

        self.image = sprite_sheet.get_image(1, 1, Constants.ITEM_WIDTH, Constants.ITEM_HEIGHT)
        self.rect = self.image.get_rect()

        def update(self):
            pass
