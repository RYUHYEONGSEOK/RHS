import random

from pico2d import *

from boy import FreeBoy as Boy # import Boy class from boy.py

class FreeBall:
    image = None;

    def __init__(self, _x, _y):
        self.x, self.y = _x, _y
        if FreeBall.image == None:
            FreeBall.image = load_image('ball21x21.png')

    def update(self, frame_time, object):
        self.x = clamp(0, self.x, self.bg.w)
        self.y = clamp(0, self.y, self.bg.h)

        if (self.collide(object) == True):
            return 1

    def draw(self):
        sx = self.x - self.bg.window_left
        sy = self.y - self.bg.window_bottom
        self.image.clip_draw(0, 0, 21, 21, sx, sy)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def set_background(self, bg):
        self.bg = bg


    def collide(self, b):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True