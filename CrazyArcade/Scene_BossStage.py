from pico2d import *
import time

import Framework
import Scene_Lobby

import Object_Player
import Object_Button
import Object_Tile

BOSS_STAGE = 1
gSceneImage = None
gCoverImage = None
gEvents = None

#게임시간 관련 변수
gTimeImage = None
gGameTime = None
gCheckTime = None
#버튼
gExitButton = None
#플레이어
gPlayer = None
#오브젝트관리 리스트
gObjList = None
PLAYER, MONSTER, BOSS_MONSTER, TILE, ITEM, BUBBLE, BUBBLE_EFFECT = 0, 1, 2, 3, 4, 5, 6
#타일 관리 리스트(15x13)
gTileList = None

def enter(_ambul = 0, _dart = 0, _pin = 0, _banana = 0):
    global gSceneImage, gCoverImage
    gSceneImage = load_image('Sprite\\03.InGame\\InGame_Bg.bmp')
    gCoverImage = load_image('Sprite\\03.InGame\\InGame_Image_Empty.bmp')

    # 게임의 시간
    global gTimeImage, gGameTime, gCheckTime
    gTimeImage = load_image('Sprite\\03.InGame\\InGame_Image_Num.png')
    gGameTime = 180
    gCheckTime = time.time()

    # 플레이어 객체 추가
    global gPlayer
    gPlayer = Object_Player.Player(40, (600 - 60), BOSS_STAGE, _ambul, _dart, _pin, _banana)
    gPlayer.enter()

    # 오브젝트관리 리스트
    global gObjList
    gObjList = {PLAYER: [gPlayer], MONSTER: [], BOSS_MONSTER: [], TILE: [], ITEM: [], BUBBLE: [], BUBBLE_EFFECT: []}

    # 타일관리 리스트 => 나중에 파일입출력으로 불러오기
    global gTileList
    gTileList = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
    # 타일관리 리스트 => 나중에 파일입출력으로 불러오기
    for i in range(0, 13):
        for j in range(0, 15):
            tempTile = Object_Tile.Tile(40 + (j * 40), (600 - 60) - (40 * i), BOSS_STAGE, 1, 0)
            tempTile.enter()
            gTileList[i].append(tempTile)

    # 버튼 객체 추가
    global gExitButton
    gExitButton = Object_Button.Button(717, (600 -577), 4)
    gExitButton.enter()

def exit():
    global gSceneImage, gCoverImage
    del(gSceneImage)
    del(gCoverImage)

    # 게임의 시간
    global gTimeImage
    del (gTimeImage)

    # 오브젝트관리 리스트 삭제
    global gObjList
    for i in gObjList:
        for j in gObjList[i]:
            del j

    # 타일관리 리스트
    global gTileList
    for i in gTileList:
        for j in gTileList[i]:
            del j

    # 플레이어 삭제
    global gPlayer
    gPlayer = None

    #버튼 삭제
    global gExitButton
    del(gExitButton)

def update():
    # 게임의 시간 및 키보드이벤트
    global gEvents, gGameTime, gCheckTime

    # 시간 1초씩 줄이기
    if gCheckTime + 1 < time.time():
        gCheckTime = time.time()
        gGameTime -= 1
        # 시간이 초과되면 0으로 초기화 하고 종료
        if gGameTime < 0:
            gGameTime = 0
            # 종료되는 과정 추가(지금은 임시방편)
            Framework.change_scene(Scene_Lobby)
            return

    # 오브젝트관리 리스트 update
    global gObjList
    for i in gObjList:
        for j in gObjList[i]:
            if (j.update(gEvents) == False):
                gObjList[i].remove(j)
            else:
                pass

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

    # 타일관리 리스트의 draw
    global gTileList
    for i in gTileList:
        for j in gTileList[i]:
            j.draw()

    # 게임의 시간
    global gTimeImage, gGameTime
    gTimeImage.clip_draw(10 * (int)(gGameTime / 60), 0, 10, 12, 725, (600 - 82))
    gTimeImage.clip_draw(10 * (int)(gGameTime % 60 / 10), 0, 10, 12, 743, (600 - 82))
    gTimeImage.clip_draw(10 * (int)(gGameTime % 60 % 10), 0, 10, 12, 753, (600 - 82))

    # 버튼의 draw
    global gExitButton
    gExitButton.draw()

    # 플레이어의 아이템 숫자
    global gObjList
    if len(gObjList[PLAYER]) > 0:
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].ambulanceCount, 0, 10, 12, 275, (600 - 590))
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].dartCount, 0, 10, 12, 315, (600 - 590))
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].pinCount, 0, 10, 12, 355, (600 - 590))
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].bananaCount, 0, 10, 12, 395, (600 - 590))

    # 오브젝트관리 리스트 draw
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