from pico2d import *

import Framework
import Scene_NormalStage
#import Scene_BossStage

import Object_Button

gName = "Scene_Lobby"
gSceneImage = None
gCoverImage = None
gMapNormalImage = None
gMapBossImage = None
gEvents = None
gStageNumber = 1
#버튼
gStartButton = None
gMapNormalButton = None
gMapBossButton = None

def enter():
    global gSceneImage, gCoverImage, gMapNormalImage, gMapBossImage
    gSceneImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Bg.bmp')
    gCoverImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Image_Empty.bmp')
    gMapNormalImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Image_Map_0.bmp')
    gMapBossImage = load_image('..\\Sprite\\02.Lobby\\Lobby_Image_Map_1.bmp')

    #버튼 객체 추가
    global gStartButton, gMapNormalButton, gMapBossButton
    gStartButton = Object_Button.Button(598, (600 - 515), 1)
    gStartButton.enter()
    gMapNormalButton = Object_Button.Button(698, (600 - 349), 2)
    gMapNormalButton.enter()
    gMapBossButton = Object_Button.Button(698, (600 - 368), 3)
    gMapBossButton.enter()

    # 기본스테이지 1로 맞춰놓기
    global gStageNumber
    gStageNumber = 1

def exit():
    global gSceneImage, gCoverImage, gMapNormalImage, gMapBossImage
    del (gSceneImage)
    del (gCoverImage)
    del (gMapNormalImage)
    del (gMapBossImage)

    #버튼 삭제
    global gStartButton, gMapNormalButton, gMapBossButton
    del(gStartButton)
    del(gMapNormalButton)
    del(gMapBossButton)

def update():
    #이벤트값은 버튼들로 뿌려줘야 한다!
    global gEvents, gStageNumber

    #버튼
    global gStartButton, gMapNormalButton, gMapBossButton
    if (gStartButton.update(gEvents)) == 1:
        if gStageNumber == 1:
            Framework.change_scene(Scene_NormalStage)
            return
        elif gStageNumber == 2:
            pass

    if (gMapNormalButton.update(gEvents)) == 2:
        gStageNumber = 1
    if (gMapBossButton.update(gEvents)) == 3:
        gStageNumber = 2

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
    global gStartButton, gMapNormalButton, gMapBossButton
    gStartButton.draw()
    gMapNormalButton.draw()
    gMapBossButton.draw()

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