from pico2d import *
import random

import game_framework


from boy import FreeBoy as Boy # import Boy class from boy.py
from background import FixedBackground as Background
import ball

name = "scroll_state"

boy = None
background = None

g_ballList = None
g_ballListCount = 0
g_Ball = None

mouseX = 0
mouseY = 0

def create_world():
    global boy, background
    boy = Boy()
    background = Background()

    background.set_center_object(boy)
    boy.set_background(background)

    
    #create ball
    global g_Ball, g_ballList
    g_Ball = ball.FreeBall(random.randint(100, 3000), random.randint(100, 1300))
    g_Ball.set_background(background)
    g_ballList = [g_Ball]
    for i in range(0, 99):
        g_Ball = ball.FreeBall(random.randint(100, 3000), random.randint(100, 1300))
        g_Ball.set_background(background)
        g_ballList.append(g_Ball)


def destroy_world():
    global boy, background
    del(boy)
    del(background)


def enter():
    open_canvas(800, 600)
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()
    close_canvas()


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    global mouseX, mouseY, g_Ball, g_ballList, boy
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouseX, mouseY = event.x, event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = boy.getXY()
            g_Ball = ball.FreeBall(mouseX + x, (600 - event.y) + y)
            g_Ball.set_background(background)
            g_ballList.append(g_Ball)
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                boy.handle_event(event)
                background.handle_event(event)


def update(frame_time):
    boy.update(frame_time)
    background.update(frame_time)

    global g_ballList, g_ballListCount

    for i in g_ballList:
        g_ballListCount += 1
        if (i.update(frame_time, boy) == 1):
            i = g_ballList.remove(i)


def draw(frame_time):
    clear_canvas()
    background.draw()
    boy.draw()

    global g_ballList, g_ballListCount
    for i in g_ballList:
        i.draw()

    debug_print('ballcount=%d' % (g_ballListCount))
    g_ballListCount = 0
    update_canvas()



