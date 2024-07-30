import pygame as pg
from pygame.sprite import Sprite, Group

import numpy as np
import random

from .settings import *


class ArrayGroup(Group):
    def __init__(self, *sprites) -> None:
        super().__init__(sprites)

    def to_array(self):
        return np.array([sprite.rect for sprite in self.sprites()])

class Particle(Sprite):
    particles = None
    def __init__(self, group) -> None:
        super().__init__(group)

        self.radius = 10
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        self.image.fill((0, 0, 0, 0))
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        self.rect = np.array([random.randint(self.radius, WIDTH - self.radius) - self.radius, random.randint(self.radius, HEIGHT - self.radius) - self.radius]) # center


        


    def update(self, dt):
        """Update the particle's position.
            Using vectorization of operation on basic simulation algorithm
        """
        pass