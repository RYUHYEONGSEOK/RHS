﻿import random

from pico2d import *

class Boy:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 25.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3

    def __init__(self):
        self.x, self.y = 0, 100
        self.frame = random.randint(0, 7)
        self.life_time = 0.0
        self.total_frames = 0.0
        self.dir = 0
        self.fall_speed = 100
        self.isBrickCollision = False
        self.state = self.RIGHT_STAND
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

        #jump
        self.jump_count = 0
        self.isJump = False


    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.life_time += frame_time
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8
        self.x += (self.dir * distance)

        self.x = clamp(0, self.x, 800)

        if self.isJump:
            self.jump_count -= 1
            if self.jump_count == 0:
                self.isJump = False

            if (self.isJump == True) and (self.jump_count < 41):
                self.y += 80 * (self.jump_count - 20) * frame_time
            elif (self.isJump == True) and (self.jump_count < 21):
                self.y += 80 * self.jump_count * frame_time

        self.y -= frame_time * self.fall_speed

    def stop(self):
        self.fall_speed = 0

    def draw(self):
        self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 25, self.y - 40, self.x + 25, self.y + 40

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.RIGHT_RUN):
                self.state = self.LEFT_RUN
                self.dir = -1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.RIGHT_STAND, self.LEFT_STAND, self.LEFT_RUN):
                self.state = self.RIGHT_RUN
                self.dir = 1
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN,):
                self.state = self.LEFT_STAND
                self.dir = 0
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN,):
                self.state = self.RIGHT_STAND
                self.dir = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if self.isJump == False:
                self.isJump = True
                self.jump_count = 41