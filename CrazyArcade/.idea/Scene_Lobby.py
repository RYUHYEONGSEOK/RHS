from pico2d import *

import Framework
#import Scene_Stage
#import Scene_Stage

import Object_Player


gName = "Scene_Lobby"
gSceneImage = None
gEvents = None
gPlayer = None

def enter():
    global gSceneImage
    gSceneImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Bg.bmp')

    #플레이어 객체 추가
    global gPlayer
    gPlayer = Object_Player.Player(40, 60)
    gPlayer.enter()

def exit():
    global gSceneImage
    del (gSceneImage)

    #플레이어 삭제
    global gPlayer
    del(gPlayer)

def update():
    # 나중에 제거하지만 이벤트값은 버튼들로 뿌려줘야 한다!
    global gPlayer
    global gEvents
    gPlayer.update(gEvents)

    #pass

def draw():
    global gSceneImage
    clear_canvas()
    gSceneImage.draw(400, 300)
    #나중에 제거
    global gPlayer
    gPlayer.draw()

    update_canvas()

def handle_events():
    global gEvents
    gEvents = get_events()
    for event in gEvents:
        if event.type == SDL_QUIT:
            Framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Framework.quit()

def pause(): pass
def resume(): pass