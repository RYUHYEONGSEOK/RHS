from pico2d import *

import Framework
import Scene_Lobby

import Object_Player
import Object_Button

gName = "Scene_NormalStage"
gSceneImage = None
gEvents = None

#플레이어
gPlayer = None
#버튼
gExitButton = None

def enter():
    global gSceneImage
    gSceneImage = load_image('..\\Sprite\\03.InGame\\InGame_Bg.bmp')

    # 플레이어 객체 추가
    global gPlayer
    gPlayer = Object_Player.Player(40, 60)
    gPlayer.enter()

    # 버튼 객체 추가
    global gExitButton
    gExitButton = Object_Button.Button(717, (600 -577), 4)
    gExitButton.enter()

def exit():
    global gSceneImage
    del(gSceneImage)

    # 플레이어 삭제
    global gPlayer
    del (gPlayer)

    #버튼 삭제
    global gExitButton
    del(gExitButton)

def update():
    global gEvents
    global gPlayer
    global gExitButton

    # 객체들의 update
    gPlayer.update(gEvents)

    #나가기 버튼 로비로 이동
    if gExitButton.update(gEvents) == 4:
        Framework.change_scene(Scene_Lobby)
        return

def draw():
    global gSceneImage
    global gExitButton

    clear_canvas()

    #객체들의 draw
    gSceneImage.draw(400, 300)
    gExitButton.draw()

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