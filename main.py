import pygame as pg

from src.settings import *
from src.particle import Particle, ArrayGroup, GPUGroup
from src.shader import Shader, Mouse


class Window:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(
            SIZE, pg.RESIZABLE | pg.OPENGL | pg.DOUBLEBUF, vsync=1)
        self.particles = GPUGroup()
        # self.particles = ArrayGroup()
        for _ in range(N):
            Particle(self.particles)
        self.particles.startup()

    def run(self):
        shader = Shader()

        clock = pg.time.Clock()
        running = True
        while running:
            Mouse.update()
            pg.display.set_caption(f"{N=} Body | FPS: {int(clock.get_fps())}")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                shader.event(event)

            dt = clock.tick(FPS) / 1000

            self.screen.fill((0, 0, 0))

            self.particles.update(dt)

            self.particles.draw(self.screen)

            shader.render(self.screen)

            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    Window().run()
