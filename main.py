import pygame as pg
from pygame.sprite import Group

from src.settings import *
from src.particle import Particle

class Window:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(SIZE, pg.RESIZABLE| pg.SCALED | pg.SRCALPHA)
        self.particles = Group()
        for _ in range(100):
            Particle(self.particles)


    def run(self):
        pg.display.set_caption("My Game")
        clock = pg.time.Clock()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            dt = clock.tick(FPS) / 1000

            self.screen.fill((0, 0, 0))

            self.particles.draw(self.screen)

            pg.display.flip()
        pg.quit()


if __name__ == "__main__":
    Window().run()