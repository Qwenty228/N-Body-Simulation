import pygame as pg

from src.settings import *
from src.particle import Particle, ArrayGroup

class Window:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(SIZE, pg.RESIZABLE| pg.SCALED | pg.SRCALPHA)
        self.particles = ArrayGroup()
        for _ in range(500):
            Particle(self.particles)
        self.particles.startup()
       

    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            pg.display.set_caption(f"N Body | FPS: {int(clock.get_fps())}")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            dt = clock.tick(FPS) / 1000

            self.screen.fill((0, 0, 0))

            self.particles.update(dt)

            self.particles.draw(self.screen)

            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    Window().run()