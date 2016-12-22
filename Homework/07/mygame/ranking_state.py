import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "RankingState"

font = None
image = None
scoreList = []

def enter():
    global font, image
    font = load_font('NANUMBARUNGOTHICBOLD.TTF')
    image = load_image('blackboard.png')

    global scoreList
    scoreList.clear()

    boydata = open('ranking_data.txt', 'r')
    scoreList = json.load(boydata)
    boydata.close()


def exit():
    global font, image

    del (font)
    del (image)


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)


def update(frame_time):pass


def draw(frame_time):
    global scoreList

    clear_canvas()
    image.draw(400, 300)

    for i in range(0, 10):
        font.draw(200, 600 - 40 * (i + 1), '%d. PLAYER%d : %3.2f(x : %d, y : %d)' % (i + 1, scoreList[5 * i + 1], scoreList[5 * i + 2], scoreList[5 * i + 3], scoreList[5 * i + 4]))
        if (int)(len(scoreList) / 5) == i + 1:
            break

    update_canvas()