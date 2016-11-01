# coding: cp949
from pico2d import *
import time

import Framework
import Scene_Lobby

import Object_Player
import Object_Button
import Object_Tile
import Object_Special_Tile
import Object_Banner
import Object_Monster

NORMAL_STAGE = 0
gSceneImage = None
gCoverImage = None
gEvents = None

#게임시간 관련 변수
gTimeImage = None
gGameTime = None
gCheckTime = None
gIsHurryUp, gIsStart, gIsEnd = None, None, None
#버튼
gExitButton = None
#플레이어
gPlayer = None
#오브젝트관리 리스트
gObjList = None
PLAYER, MONSTER, BOSS_MONSTER, SPECIAL_TILE, ITEM, BUBBLE, BUBBLE_EFFECT, BANNER = 0, 1, 2, 3, 4, 5, 6, 7
#타일 관리 리스트(15x13)
gTileList = None

def enter(_ambul = 0, _dart = 0, _pin = 0, _banana = 0):
    global gSceneImage, gCoverImage
    gSceneImage = load_image('..\\Sprite\\03.InGame\\InGame_Bg.bmp')
    gCoverImage = load_image('..\\Sprite\\03.InGame\\InGame_Image_Empty.bmp')

    #게임의 시간
    global gTimeImage, gGameTime, gCheckTime
    gTimeImage = load_image('..\\Sprite\\03.InGame\\InGame_Image_Num.png')
    gGameTime = 180
    gCheckTime = time.time()

    #게임의 시간에 대한 논리연산
    global gIsHurryUp, gIsStart, gIsEnd
    gIsHurryUp, gIsStart, gIsEnd = False, False, False

    # 플레이어 객체 추가
    global gPlayer
    gPlayer = Object_Player.Player(40, (600 - 60), NORMAL_STAGE, _ambul, _dart, _pin, _banana)
    gPlayer.enter()

    # 오브젝트관리 리스트
    global gObjList
    gObjList = {PLAYER: [gPlayer], MONSTER: [], BOSS_MONSTER: [], SPECIAL_TILE: [], ITEM: [], BUBBLE: [], BUBBLE_EFFECT: [], BANNER: []}

    # 타일관리 리스트 => 나중에 파일입출력으로 불러오기
    global gTileList
    gTileList = []
    for i in range(0, 13):
        for j in range(0, 15):
            tempTile = Object_Tile.Tile(40 + (j * 40), (600 - 60) - (40 * i), NORMAL_STAGE, 1, 0)
            tempTile.enter()
            gTileList.append(tempTile)

    #스페셜 타일 생성 => 나중에 파일입출력으로 불러오기
    tempSpecialTile = Object_Special_Tile.SpecialTile(400, 300, NORMAL_STAGE, 0, 0)
    tempSpecialTile.enter()
    gObjList[SPECIAL_TILE].append(tempSpecialTile)
    #indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
    indexX, indexY = (int)((400 - 20) / 40), (int)((560 - 300) / 40)
    gTileList[indexY * 13 + indexX].changeOption(1)
    tempSpecialTile = Object_Special_Tile.SpecialTile(440, 300, NORMAL_STAGE, 0, 1)
    tempSpecialTile.enter()
    gObjList[SPECIAL_TILE].append(tempSpecialTile)
    indexX, indexY = (int)((440 - 20) / 40), (int)((560 - 300) / 40)
    gTileList[indexY * 13 + indexX].changeOption(1)
    tempSpecialTile = Object_Special_Tile.SpecialTile(480, 300, NORMAL_STAGE, 0, 2)
    tempSpecialTile.enter()
    gObjList[SPECIAL_TILE].append(tempSpecialTile)
    indexX, indexY = (int)((480 - 20) / 40), (int)((560 - 300) / 40)
    gTileList[indexY * 13 + indexX].changeOption(1)

    # 버튼 객체 추가
    global gExitButton
    gExitButton = Object_Button.Button(717, (600 -577), 4)
    gExitButton.enter()

    #몬스터 추가
    tempMonster = Object_Monster.Monster(400, 100, NORMAL_STAGE)
    tempMonster.enter()
    gObjList[MONSTER].append(tempMonster)

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
            gObjList[i].remove(j)
    # 오브젝트관리 리스트 2번째 삭제
    for i in gObjList:
        for j in gObjList[i]:
            gObjList[i].remove(j)

    # 타일관리 리스트
    global gTileList
    for i in gTileList:
        gTileList.remove(i)

    # 플레이어 삭제
    global gPlayer
    gPlayer = None

    #버튼 삭제
    global gExitButton
    del(gExitButton)

def update():
    #게임의 시간 및 키보드이벤트
    global gEvents, gGameTime, gCheckTime
    global gObjList
    #게임의 시간에 대한 논리연산
    global gIsHurryUp, gIsStart, gIsEnd
    #게임의 종료
    if (gIsEnd == True) and (len(gObjList[BANNER]) < 1):
        Framework.change_scene(Scene_Lobby)
        return
    # 시간 1초씩 줄이기
    if (gIsEnd == False):
        if gCheckTime + 1 < time.time():
            gCheckTime = time.time()
            gGameTime -= 1
            if gGameTime < 0:
                gGameTime = 0
                tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 5)
                tempBanner.enter()
                gObjList[BANNER].append(tempBanner)
                gIsEnd = True
            elif (gGameTime == 45) and (gIsHurryUp == False):
                tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 1)
                tempBanner.enter()
                gObjList[BANNER].append(tempBanner)
                gIsHurryUp = True
    #시작배너
    if gIsStart == False:
        tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 0)
        tempBanner.enter()
        gObjList[BANNER].append(tempBanner)
        gIsStart = True
    #승패
    if gIsEnd == False:
        #패배
        if (len(gObjList[PLAYER]) < 1):
            tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 5)
            tempBanner.enter()
            gObjList[BANNER].append(tempBanner)
            gIsEnd = True
        #승리
        #elif (len(gObjList[MONSTER]) < 1):
        #    tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 2)
        #    tempBanner.enter()
        #    gObjList[BANNER].append(tempBanner)
        #    gIsEnd = True

    # 오브젝트관리 리스트 update
    for i in gObjList:
        for j in gObjList[i]:
            if (j.update(gEvents) == False):
                gObjList[i].remove(j)

    #나가기 버튼 로비로 이동
    global gExitButton
    if (gExitButton.update(gEvents) == 4) and (gIsEnd == False):
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
        i.draw()

    # 게임의 시간
    global gTimeImage, gGameTime
    gTimeImage.clip_draw(10 * (int)(gGameTime / 60), 0, 10, 12, 725, (600 - 82))
    gTimeImage.clip_draw(10 * (int)(gGameTime % 60 / 10), 0, 10, 12, 743, (600 - 82))
    gTimeImage.clip_draw(10 * (int)(gGameTime % 60 % 10), 0, 10, 12, 753, (600 - 82))

    # 버튼의 draw
    global gExitButton
    gExitButton.draw()

    #플레이어의 아이템 숫자
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