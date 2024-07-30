import pygame as pg
from pygame.sprite import AbstractGroup, Sprite, Group

import numpy as np
import random

from .settings import *


class ArrayGroup(Group):
    def __init__(self, *sprites) -> None:
        super().__init__(sprites)

    def to_array(self):
        return np.array([sprite.rect for sprite in self.sprites()], dtype=np.float64)
    
    def startup(self):
        self.particles = self.to_array()
        self.particlev = np.zeros_like(self.particles)
        self.length = len(self.sprites())

    def update(self, dt, *args, **kwargs):
        Fp = np.zeros((self.length, 2))
        for par in self.particles:
            dp = self.particles - par
            drSquared = np.sum(dp ** 2, axis=1)
            h = np.sqrt(drSquared) + drSquared
            drPowerN32 = 1. / (np.maximum(h, 1E-10))
            Fp += -(dp.T * drPowerN32).T    # - sum G mm / r^2 * r_hat
            self.particlev += dt * Fp 
        self.particles += self.particlev * dt
        self.particles = np.clip(self.particles, 0, np.array([WIDTH, HEIGHT]) - Particle.radius)
        

    def draw(self, surface):
        for i, par in enumerate(self.sprites()):
            surface.blit(par.image, self.particles[i])


class Particle(Sprite):
    radius = 2
    def __init__(self, group) -> None:
        super().__init__(group)

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        # self.image.fill('white')
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        self.rect = np.array([random.randint(self.radius, WIDTH - self.radius) - self.radius, random.randint(self.radius, HEIGHT - self.radius) - self.radius]) # center




    