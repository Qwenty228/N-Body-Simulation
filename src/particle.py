import pygame as pg
from pygame.sprite import Sprite

import numpy as np
import random

from .settings import *


class Particle(Sprite):
    def __init__(self, group) -> None:
        super().__init__(group)

        self.radius = 4
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0, 0))
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
