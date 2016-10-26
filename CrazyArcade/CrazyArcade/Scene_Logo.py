# coding: cp949
from pico2d import *

import Framework
import Scene_Lobby

gSceneImage = None
gLogo_time = 0.0

def enter(_ambul = 0, _dart = 0, _pin = 0, _banana = 0):
    global gSceneImage
    gSceneImage = load_image('..\\Sprite\\01.Logo\\kpu_credit.png')

    #시간 초기화
    global gLogo_time
    gLogo_time = 0.0

def exit():
    global gSceneImage
    del(gSceneImage)

def update():
    global gLogo_time
    if gLogo_time > 1.0:
        gLogo_time = 0
        Framework.change_scene(Scene_Lobby)
        return

    delay(0.01)
    gLogo_time += 0.01

def draw():
    global gSceneImage
    clear_canvas()
    gSceneImage.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Framework.quit()

def pause(): pass
def resume(): pass