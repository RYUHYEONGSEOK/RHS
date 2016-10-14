from pico2d import *

import Framework
import Scene_Lobby

import Object_Player
import Object_Button

gSceneImage = None
gCoverImage = None
gEvents = None

#버튼
gExitButton = None
#플레이어
gPlayer = None
#오브젝트관리 리스트
gObjList = None
PLAYER, MONSTER, BOSS_MONSTER, TILE, ITEM, BUBBLE, BUBBLE_EFFECT = 0, 1, 2, 3, 4, 5, 6

def enter(_ambul = 0, _dart = 0, _pin = 0, _banana = 0):
    global gSceneImage, gCoverImage
    gSceneImage = load_image('..\\Sprite\\03.InGame\\InGame_Bg.bmp')
    gCoverImage = load_image('..\\Sprite\\03.InGame\\InGame_Image_Empty.bmp')

    # 플레이어 객체 추가
    global gPlayer
    gPlayer = Object_Player.Player(40, 60, _ambul, _dart, _pin, _banana)
    gPlayer.enter()

    # 오브젝트관리 리스트
    global gObjList
    gObjList = {PLAYER: [gPlayer], MONSTER: [], BOSS_MONSTER: [], TILE: [], ITEM: [], BUBBLE: [], BUBBLE_EFFECT: []}

    # 버튼 객체 추가
    global gExitButton
    gExitButton = Object_Button.Button(717, (600 -577), 4)
    gExitButton.enter()

def exit():
    global gSceneImage, gCoverImage
    del(gSceneImage)
    del(gCoverImage)

    # 오브젝트관리 리스트 삭제
    global gObjList
    for i in gObjList:
        for j in gObjList[i]:
            del j

    # 플레이어 삭제
    global gPlayer
    gPlayer = None

    #버튼 삭제
    global gExitButton
    del(gExitButton)

def update():
    global gEvents

    # 오브젝트관리 리스트 update
    global gObjList
    for i in gObjList:
        for j in gObjList[i]:
            j.update(gEvents)

    #나가기 버튼 로비로 이동
    global gExitButton
    if gExitButton.update(gEvents) == 4:
        Framework.change_scene(Scene_Lobby)
        return

def draw():
    global gSceneImage, gCoverImage

    clear_canvas()
    gSceneImage.draw(400, 300)
    for i in range(0, 3):
        gCoverImage.draw(717, (600 - 161.5) - (43 * i))

    # 버튼의 draw
    global gExitButton
    gExitButton.draw()

    # 오브젝트관리 리스트 draw
    global gObjList
    for i in gObjList:
        for j in gObjList[i]:
            j.draw()

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