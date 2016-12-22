import random

from pico2d import *

class Brick:
    def __init__(self):
        self.image = load_image('brick180x40.png')
        self.x, self.y = 400, 180
        self.moving_speed = 50
        #moving dir
        self.isLeftMoving = False

    def update(self, frame_time):
        if self.isLeftMoving == True:
            self.x -= self.moving_speed * frame_time
            if self.x < 90:
                self.x = 90
                self.isLeftMoving = False
        elif self.isLeftMoving == False:
            self.x += self.moving_speed * frame_time
            if self.x > 800 - 90:
                self.x = 800 - 90
                self.isLeftMoving = True

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 90, self.y - 20, self.x + 90, self.y + 20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())