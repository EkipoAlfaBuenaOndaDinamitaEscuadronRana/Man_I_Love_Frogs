from router_solver import *
import pygame
import game_engine.constants
from game_engine.constants import *


class SpriteSheet(object):
    def __init__(self, file_name):
        # Load the sprite sheet.
        BLACK = (0, 0, 0)
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.sprite_sheet.set_colorkey(BLACK)

    def get_image(self, x, y, width, height):
        """Grab a single image out of a larger spritesheet
        Pass in the x, y location of the sprite
        and the width and height of the sprite."""

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        image.set_colorkey(Constants.BLUE)

        # Return the image
        return image
