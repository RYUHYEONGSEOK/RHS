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

#���ӽð� ���� ����
gTimeImage = None
gGameTime = None
gCheckTime = None
gIsHurryUp, gIsStart, gIsEnd = None, None, None
#��ư
gExitButton = None
#�÷��̾�
gPlayer = None
#������Ʈ���� ����Ʈ
gObjList = None
PLAYER, MONSTER, BOSS_MONSTER, SPECIAL_TILE, ITEM, BUBBLE, BUBBLE_EFFECT, BANNER = 0, 1, 2, 3, 4, 5, 6, 7
#Ÿ�� ���� ����Ʈ(15x13)
gTileList = None

def enter(_ambul = 0, _dart = 0, _pin = 0, _banana = 0):
    global gSceneImage, gCoverImage
    gSceneImage = load_image('..\\Sprite\\03.InGame\\InGame_Bg.bmp')
    gCoverImage = load_image('..\\Sprite\\03.InGame\\InGame_Image_Empty.bmp')

    #������ �ð�
    global gTimeImage, gGameTime, gCheckTime
    gTimeImage = load_image('..\\Sprite\\03.InGame\\InGame_Image_Num.png')
    gGameTime = 180
    gCheckTime = time.time()

    #������ �ð��� ���� ������
    global gIsHurryUp, gIsStart, gIsEnd
    gIsHurryUp, gIsStart, gIsEnd = False, False, False

    # �÷��̾� ��ü �߰�
    global gPlayer
    gPlayer = Object_Player.Player(40, (600 - 60), NORMAL_STAGE, _ambul, _dart, _pin, _banana)
    gPlayer.enter()

    # ������Ʈ���� ����Ʈ
    global gObjList
    gObjList = {PLAYER: [gPlayer], MONSTER: [], BOSS_MONSTER: [], SPECIAL_TILE: [], ITEM: [], BUBBLE: [], BUBBLE_EFFECT: [], BANNER: []}

    # Ÿ�ϰ��� ����Ʈ => ���߿� ������������� �ҷ�����
    global gTileList
    gTileList = []
    for i in range(0, 13):
        for j in range(0, 15):
            tempTile = Object_Tile.Tile(40 + (j * 40), (600 - 60) - (40 * i), NORMAL_STAGE, 1, 0)
            tempTile.enter()
            gTileList.append(tempTile)

    #����� Ÿ�� ���� => ���߿� ������������� �ҷ�����
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

    # ��ư ��ü �߰�
    global gExitButton
    gExitButton = Object_Button.Button(717, (600 -577), 4)
    gExitButton.enter()

    #���� �߰�
    tempMonster = Object_Monster.Monster(400, 100, NORMAL_STAGE)
    tempMonster.enter()
    gObjList[MONSTER].append(tempMonster)

def exit():
    global gSceneImage, gCoverImage
    del(gSceneImage)
    del(gCoverImage)

    # ������ �ð�
    global gTimeImage
    del (gTimeImage)

    # ������Ʈ���� ����Ʈ ����
    global gObjList
    for i in gObjList:
        for j in gObjList[i]:
            gObjList[i].remove(j)
    # ������Ʈ���� ����Ʈ 2��° ����
    for i in gObjList:
        for j in gObjList[i]:
            gObjList[i].remove(j)

    # Ÿ�ϰ��� ����Ʈ
    global gTileList
    for i in gTileList:
        gTileList.remove(i)

    # �÷��̾� ����
    global gPlayer
    gPlayer = None

    #��ư ����
    global gExitButton
    del(gExitButton)

def update():
    #������ �ð� �� Ű�����̺�Ʈ
    global gEvents, gGameTime, gCheckTime
    global gObjList
    #������ �ð��� ���� ������
    global gIsHurryUp, gIsStart, gIsEnd
    #������ ����
    if (gIsEnd == True) and (len(gObjList[BANNER]) < 1):
        Framework.change_scene(Scene_Lobby)
        return
    # �ð� 1�ʾ� ���̱�
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
    #���۹��
    if gIsStart == False:
        tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 0)
        tempBanner.enter()
        gObjList[BANNER].append(tempBanner)
        gIsStart = True
    #����
    if gIsEnd == False:
        #�й�
        if (len(gObjList[PLAYER]) < 1):
            tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 5)
            tempBanner.enter()
            gObjList[BANNER].append(tempBanner)
            gIsEnd = True
        #�¸�
        #elif (len(gObjList[MONSTER]) < 1):
        #    tempBanner = Object_Banner.Banner(400, 300, NORMAL_STAGE, 2)
        #    tempBanner.enter()
        #    gObjList[BANNER].append(tempBanner)
        #    gIsEnd = True

    # ������Ʈ���� ����Ʈ update
    for i in gObjList:
        for j in gObjList[i]:
            if (j.update(gEvents) == False):
                gObjList[i].remove(j)

    #������ ��ư �κ�� �̵�
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

    # Ÿ�ϰ��� ����Ʈ�� draw
    global gTileList
    for i in gTileList:
        i.draw()

    # ������ �ð�
    global gTimeImage, gGameTime
    gTimeImage.clip_draw(10 * (int)(gGameTime / 60), 0, 10, 12, 725, (600 - 82))
    gTimeImage.clip_draw(10 * (int)(gGameTime % 60 / 10), 0, 10, 12, 743, (600 - 82))
    gTimeImage.clip_draw(10 * (int)(gGameTime % 60 % 10), 0, 10, 12, 753, (600 - 82))

    # ��ư�� draw
    global gExitButton
    gExitButton.draw()

    #�÷��̾��� ������ ����
    global gObjList
    if len(gObjList[PLAYER]) > 0:
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].ambulanceCount, 0, 10, 12, 275, (600 - 590))
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].dartCount, 0, 10, 12, 315, (600 - 590))
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].pinCount, 0, 10, 12, 355, (600 - 590))
        gTimeImage.clip_draw(10 * gObjList[PLAYER][0].bananaCount, 0, 10, 12, 395, (600 - 590))

    # ������Ʈ���� ����Ʈ draw
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