from pico2d import *

import Framework
import Scene_Lobby

gName = "Scene_Logo"
gSceneImage = None
gLogo_time = 0.0

def enter():
    global gSceneImage
    gSceneImage = load_image('..\\Sprite\\01.Logo\\kpu_credit.png')

def exit():
    global gSceneImage
    del(gSceneImage)

def update():
    global gLogo_time
    #if gLogo_time > 1.0:
    if gLogo_time > 0.1:
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