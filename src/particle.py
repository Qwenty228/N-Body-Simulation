import pygame as pg
from pygame.sprite import Sprite, Group
import numba
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

    def update(self, dt, *args, **kwargs):
        Fp = np.zeros((N, 2))
        for par in self.particles:
            dp = self.particles - par
            drSquared = np.sum(dp ** 2, axis=1)
            h = np.sqrt(drSquared) + drSquared
            drPowerN32 = 1. / (np.maximum(h, 1E-10))
            Fp += -(dp.T * drPowerN32).T    # - sum G mm / r^2 * r_hat
            self.particlev += dt * Fp
        self.particles += self.particlev * dt
        self.particles = np.clip(self.particles, 0, np.array(
            [WIDTH, HEIGHT]) - Particle.radius)

    def draw(self, surface):
        for i, par in enumerate(self.sprites()):
            surface.blit(par.image, self.particles[i])


@numba.jit(nopython=True, parallel=True, cache=True, fastmath=True)
def nbody(particle, particlev, dt):
    for i in numba.prange(N):
        Fx = 0.0
        Fy = 0.0
        for j in range(N):
            if j != i:
                dx = particle[j, 0] - particle[i, 0]
                dy = particle[j, 1] - particle[i, 1]

                drSquared = dx * dx + dy * dy + 1
                drPowerN32 = 1.0 / (drSquared + np.sqrt(drSquared))
                Fx += dx * drPowerN32
                Fy += dy * drPowerN32

            particlev[i, 0] += dt * Fx
            particlev[i, 1] += dt * Fy

    for i in numba.prange(N):
        particle[i, 0] += particlev[i, 0] * dt
        particle[i, 1] += particlev[i, 1] * dt


class GPUGroup(ArrayGroup):
    def update(self, dt):
        nbody(self.particles, self.particlev, dt)
        self.particles = np.clip(self.particles, 0, np.array(
            [WIDTH, HEIGHT]) - Particle.radius)


class Particle(Sprite):
    radius = 2

    def __init__(self, group) -> None:
        super().__init__(group)

        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))

        self.image = pg.Surface(
            (self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        # self.image.fill('white')
        pg.draw.circle(self.image, self.color,
                       (self.radius, self.radius), self.radius)

        self.rect = np.array([random.randint(self.radius, WIDTH - self.radius) - self.radius,
                             random.randint(self.radius, HEIGHT - self.radius) - self.radius])  # center
