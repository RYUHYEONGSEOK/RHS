import random

from pico2d import *

class Grass:
    def __init__(self):
        self.x = 400
        self.y = 30
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 401, self.y - 31, self.x + 401, self.y + 31

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


class Brick:
    def __init__(self):
        self.x = 400
        self.y = 200
        self.speed = 40
        self.dir = 0
        self.image = load_image('brick180x40.png')

    def update(self, frame_time):
        #left
        if self.dir == 0:
            self.x -= frame_time * self.speed
            if self.x < 90:
                self.x = 90
                self.dir = 1
        #right
        elif self.dir == 1:
            self.x += frame_time * self.speed
            if self.x > 710:
                self.x = 710
                self.dir = 0

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())