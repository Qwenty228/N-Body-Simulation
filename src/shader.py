import moderngl
from array import array
import pygame as pg
from .settings import *

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    gl_Position = vec4(vert, 0.0, 1.0); 
    uvs = texcoord;                             
    }

'''
frag_shader = '''
#version 330 core
uniform sampler2D tex;
uniform vec2 iResolution;
uniform vec2 originalResolution;


in vec2 uvs;          
out vec4 f_color;

void main(){
    float ratio = min(iResolution.x/originalResolution.x, iResolution.y/originalResolution.y);      // get best fit ratio from original to new fullscreen
    vec2 offset = (iResolution - originalResolution * ratio) / 2.0;                                 // get the offset of the image to center it
    vec2 uv = uvs*iResolution;                                                                      // get the pixel position on the screen
    if (uv.x < offset.x || uv.x > iResolution.x - offset.x || uv.y < offset.y || uv.y > iResolution.y - offset.y) {
        f_color = vec4(0.0, 0.0, 0.0, 1.0);                                                         // if the pixel is outside the image, return black                               
        return;
    }
    uv = (uv - offset)/(originalResolution*ratio);                                                  // shift pixel by offset and divide by the scaled original resolution to turn back to 0-1 range
    f_color = vec4(texture(tex, uv).rgb, 1.0);
}
'''


class Shader:
    def __init__(self):
        self.ctx = moderngl.create_context()
        self.screen_size = SIZE
        quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0,  1.0, 0.0, 0.0,   # top left
            1.0, 1.0, 1.0, 0.0,     # top right
            -1.0,  -1.0, 0.0, 1.0,  # bottom left
            1.0, -1.0, 1.0, 1.0,   # bottom right
        ]))

        self.program = self.ctx.program(vertex_shader=vert_shader,
                                        fragment_shader=frag_shader)
        self.vao = self.ctx.vertex_array(
            self.program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')]
        )

    def render(self, surface: pg.Surface):
        tex = self.ctx.texture(surface.get_size(), 4)  # number of color channels
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)  # no interpolation
        tex.swizzle = 'BGRA'  # gl differs from pygame, so we have to swizzle the colors
        tex.write(surface.get_view('1'))  # write the surface to the texture 
        tex.use(0)
        self.program['tex'] = 0
        self.program['iResolution'] = self.screen_size 
        self.program['originalResolution'] = SIZE
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)

    def event(self, event):
        if event.type == pg.VIDEORESIZE:
            self.screen_size = event.size
            Mouse.ratio = min(event.w/WIDTH, event.h/HEIGHT)
            Mouse.offset = (event.w - WIDTH * Mouse.ratio) / 2.0, (event.h - HEIGHT * Mouse.ratio) / 2.0
        



class Mouse:
    offset = (0, 0)
    pos = (0, 0)
    ratio = 1
    @classmethod
    def update(cls):
        x, y = pg.mouse.get_pos()
        cls.pos = (x - cls.offset[0]) /cls.ratio , (y - cls.offset[1] )/ cls.ratio