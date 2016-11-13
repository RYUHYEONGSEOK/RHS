# coding: cp949
from pico2d import *

import Framework
import Scene_NormalStage
import Scene_BossStage

import Manager_Sound

import Object_Button

gEvents = None
gStageNumber = 1
#이미지
gSceneImage = None
gCoverImage = None
gMapNormalImage = None
gMapBossImage = None
gNumberImage = None
#버튼
gStartButton = None
gMapNormalButton = None
gMapBossButton = None
gQButton = None
gWButton = None
gEButton = None
gRButton = None
#아이템수
gAmbulNum = 0
gDartNum = 0
gPinNum = 0
gBananaNum = 0

def enter(_ambul = 0, _dart = 0, _pin = 0, _banana = 0):
    global gSceneImage, gCoverImage, gMapNormalImage, gMapBossImage, gNumberImage
    gSceneImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Bg.bmp')
    gCoverImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Image_Empty.bmp')
    gMapNormalImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Image_Map_0.bmp')
    gMapBossImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Image_Map_1.bmp')
    gNumberImage = load_image('..\\Sprite\\03.InGame\\InGame_Image_Num.png')

    #버튼 객체 추가
    global gStartButton, gMapNormalButton, gMapBossButton, gQButton, gWButton, gEButton, gRButton
    gStartButton = Object_Button.Button(598, (600 - 515), 1)
    gStartButton.enter()
    gMapNormalButton = Object_Button.Button(698, (600 - 349), 2)
    gMapNormalButton.enter()
    gMapBossButton = Object_Button.Button(698, (600 - 368), 3)
    gMapBossButton.enter()
    gQButton = Object_Button.Button(60.5, (600 - 255), 5)
    gQButton.enter()
    gWButton = Object_Button.Button(97.5, (600 - 255), 6)
    gWButton.enter()
    gEButton = Object_Button.Button(134.5, (600 - 255), 7)
    gEButton.enter()
    gRButton = Object_Button.Button(171.5, (600 - 255), 8)
    gRButton.enter()

    # 아이템수 동기화
    global gAmbulNum, gDartNum, gPinNum, gBananaNum
    gAmbulNum, gDartNum, gPinNum, gBananaNum = _ambul, _dart, _pin, _banana

    # 사운드
    Manager_Sound.PlayBGMSound('BGM_PREPARE')

def exit():
    #이미지 삭제
    global gSceneImage, gCoverImage, gMapNormalImage, gMapBossImage, gNumberImage
    del (gSceneImage)
    del (gCoverImage)
    del (gMapNormalImage)
    del (gMapBossImage)
    del (gNumberImage)

    #버튼 삭제
    global gStartButton, gMapNormalButton, gMapBossButton, gQButton, gWButton, gEButton, gRButton
    del(gStartButton)
    del(gMapNormalButton)
    del(gMapBossButton)
    del(gQButton)
    del(gWButton)
    del(gEButton)
    del(gRButton)

    #사운드
    Manager_Sound.StopBGMSound('BGM_PREPARE')

def update():
    #이벤트값은 버튼들로 뿌려줘야 한다!
    global gEvents, gStageNumber

    #버튼
    global gStartButton, gMapNormalButton, gMapBossButton, gQButton, gWButton, gEButton, gRButton
    global gAmbulNum, gDartNum, gPinNum, gBananaNum
    if (gStartButton.update(gEvents)) == 1:
        if gStageNumber == 1:
            Framework.change_scene(Scene_NormalStage, gAmbulNum, gDartNum, gPinNum, gBananaNum)
            return
        elif gStageNumber == 2:
            Framework.change_scene(Scene_BossStage, gAmbulNum, gDartNum, gPinNum, gBananaNum)
            return

    if (gMapNormalButton.update(gEvents)) == 2:
        gStageNumber = 1
    if (gMapBossButton.update(gEvents)) == 3:
        gStageNumber = 2

    if (gQButton.update(gEvents)) == 5:
        gAmbulNum += 1
    if (gWButton.update(gEvents)) == 6:
        gDartNum += 1
    if (gEButton.update(gEvents)) == 7:
        gPinNum += 1
    if (gRButton.update(gEvents)) == 8:
        gBananaNum += 1

    #아이템의 수를 조절하는 함수
    setItemCount()

def draw():
    global gSceneImage, gCoverImage
    clear_canvas()
    #배경
    gSceneImage.draw(400, 300)
    #가림막
    for i in range(0, 3):
        gCoverImage.draw(306 + (i * 189), (600 - 210))
    #맵선택 화면
    if gStageNumber == 1:
        gMapNormalImage.draw(551, (600 - 406))
    elif gStageNumber == 2:
        gMapBossImage.draw(551, (600 - 406))

    #시작버튼
    global gStartButton, gMapNormalButton, gMapBossButton, gQButton, gWButton, gEButton, gRButton
    gStartButton.draw()
    gMapNormalButton.draw()
    gMapBossButton.draw()

    global gAmbulNum, gDartNum, gPinNum, gBananaNum
    gQButton.draw(), gWButton.draw(), gEButton.draw(), gRButton.draw()
    gNumberImage.clip_draw(gAmbulNum * 10, 0, 10, 12, 72.5, (600 - 260))
    gNumberImage.clip_draw(gDartNum * 10, 0, 10, 12, 109.5, (600 - 260))
    gNumberImage.clip_draw(gPinNum * 10, 0, 10, 12, 146.5, (600 - 260))
    gNumberImage.clip_draw(gBananaNum * 10, 0, 10, 12, 183.5, (600 - 260))

    update_canvas()

def handle_events():
    global gEvents
    gEvents = None
    gEvents = get_events()
    for event in gEvents:
        if event.type == SDL_QUIT:
            Framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Framework.quit()

def pause(): pass
def resume(): pass

def setItemCount():
    global gAmbulNum, gDartNum, gPinNum, gBananaNum

    if gAmbulNum > 9:
        gAmbulNum = 0
    if gDartNum > 9:
        gDartNum = 0
    if gPinNum > 9:
        gPinNum = 0
    if gBananaNum > 9:
        gBananaNum = 0