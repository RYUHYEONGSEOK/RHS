# hero_controller.py : control hero move with left and right key
import random
from pico2d import *

running = None
hero = None

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

class Hero:
    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3
    NO_RUN, UP_RUN, DOWN_RUN = 0, 1, 2

    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.state = self.RIGHT_STAND
        #dash
        self.isDash = False
        #up and down
        self.UpAndDownState = self.NO_RUN
        if Hero.image == None:
            Hero.image = load_image('animation_sheet.png')

    def handle_event(self, event):
        # fill here
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state == self.LEFT_RUN:
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state == self.RIGHT_RUN:
                self.state = self.RIGHT_STAND

        #up and down
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.UpAndDownState = self.UP_RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.UpAndDownState = self.DOWN_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            if self.UpAndDownState == self.UP_RUN:
                self.UpAndDownState = self.NO_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.UpAndDownState == self.DOWN_RUN:
                self.UpAndDownState = self.NO_RUN

        #add dash
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            self.isDash = True
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            self.isDash = False


    def update(self):
        # fill here
        self.frame = (self.frame + 1) % 8

        if self.state == self.RIGHT_RUN:
            if self.isDash == False:
                self.x = min(800, self.x + 5)
            elif self.isDash == True:
                self.x = min(800, self.x + 15)
        elif self.state == self.LEFT_RUN:
            if self.isDash == False:
                self.x = max(0, self.x - 5)
            elif self.isDash == True:
                self.x = max(0, self.x - 15)

        #up and down
        if self.UpAndDownState == self.UP_RUN:
            if self.isDash == False:
                self.y = min(600, self.y + 5)
            elif self.isDash == True:
                self.y = min(600, self.y + 15)
        elif self.UpAndDownState == self.DOWN_RUN:
            if self.isDash == False:
                self.y = max(0, self.y - 5)
            elif self.isDash == True:
                self.y = max(0, self.y - 15)

    def draw(self):
        if self.isDash:
            pass
        self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)


def handle_events():
    global running
    global hero
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            # fill here
            hero.handle_event(event)


def main():

    open_canvas()

    global hero
    global running

    hero = Hero()
    grass = Grass()

    running = True
    while running:
        handle_events()

        hero.update()

        clear_canvas()
        grass.draw()
        hero.draw()
        update_canvas()

        delay(0.04)

    close_canvas()


if __name__ == '__main__':
    main()