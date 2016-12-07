# coding: cp949
from pico2d import *
import random
import time

import Scene_NormalStage
import Scene_BossStage

import Manager_Collision

import Object_Tile
import Object_Item

class SpecialTile(Object_Tile.Tile):
    def __init__(self, _x, _y, _type, _imagevalue = 0, _breakingOption = 0):
        # 타일 위치 및 이미지와 충돌 체크용 사이즈
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 34, 34
        self.imageSizeX, self.imageSizeY = None, None
        # 타일의 속성
        self.type = _type  # 노말은0, 보스면1
        self.imageValue = _imagevalue  # 어떤 이미를 보여줄지에 대한(0~1 / 0~3 / 0)
        self.breakingOption = _breakingOption  # 부서지는지 아닌지(0부서짐 1안부서짐 2부쉬)
        self.events = None
        self.isDeath = False #프레임이 모두 지나가면 True로 변경
        self.isCollision = False #충돌하면 True로 변경
        self.dropItem = random.randint(0, 100) #아이템을 드랍할 확률
        # 이미지 사용용도의 변수
        self.specialTile_image = None
        self.frame = 0
        self.frameMax = None
        self.frameTime = None
        self.isFrameMove = None

    def __del__(self):
        self.exit() #아이템 드롭
        #터지면 타일의 옵션변경
        indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
        if self.type == 0:
            if len(Scene_NormalStage.gTileList) == (15 * 13):
                Scene_NormalStage.gTileList[indexY * 15 + indexX].changeOption(0)
        elif self.type == 1:
            if len(Scene_BossStage.gTileList) == (15 * 13):
                Scene_BossStage.gTileList[indexY * 15 + indexX].changeOption(0)

    def enter(self):
        # 이미지 사용용도의 변수
        if self.type == 0:
            if self.breakingOption == 0:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Box_1.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Box_2.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
            elif self.breakingOption == 1:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Box_3.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Box_4.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 2:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Box_5.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 3:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Box_6.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 70
            elif self.breakingOption == 2:
                self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Box_7.png')
                self.frameMax = 4
                self.frameTime = time.time()
                self.isFrameMove = True
                self.imageSizeX, self.imageSizeY = 48, 65
                self.sizeX, self.sizeY = 30, 30
                self.isPlayerCollision = False
        #보스 스테이지
        elif self.type == 1:
            if self.breakingOption == 0:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_2\\Box_1.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_2\\Box_2.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
            elif self.breakingOption == 1:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_2\\Box_3.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('.\\Sprite\\03.InGame\\Map_2\\Box_4.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 70

    def exit(self):
        del (self.specialTile_image)
        #아이템의 드랍
        if self.breakingOption == 0:
            if self.dropItem < 25:
                tempItemNum = (int)(self.dropItem / 10)
                if self.type == 0:
                    tempItem = Object_Item.Item(self.X, self.Y, self.type, tempItemNum)
                    tempItem.enter()
                    Scene_NormalStage.gObjList[4].append(tempItem)
                elif self.type == 1:
                    tempItem = Object_Item.Item(self.X, self.Y, self.type, tempItemNum)
                    tempItem.enter()
                    Scene_BossStage.gObjList[4].append(tempItem)

    def update(self, _frametime, _events):
        if self.isDeath == True:
            return False

        #충돌체크
        self.collisionBubbleEffect()
        self.collisionBubble()
        self.collisionItem()

        #충돌되면 프레임 무브하고 삭제하는것
        self.bush_frame_move()
        if (self.isCollision == True) and (self.isFrameMove == True):
            self.frame_move()

    def draw(self):
        # 프레임이 시작하는 그림에서의 X좌표, Y좌표(Y좌표는 아래서부터 1) => 왼쪽 아래부터 오른쪽 위까지 하나를 그림
        if self.breakingOption == 0:#부서지는 타일
            if self.imageValue == 0 or self.imageValue == 1:
                tempFrame = (self.frame % 3)
                tempScene = (int)(self.frame / 3)
                self.specialTile_image.clip_draw(tempFrame * self.imageSizeX, 135 - (tempScene + 1) * self.imageSizeY,
                                                 self.imageSizeX, self.imageSizeY,
                                                 self.X, self.Y + ((self.imageSizeY - self.sizeY) / 2))
        elif self.breakingOption == 2:#부쉬
            self.specialTile_image.clip_draw(self.frame * self.imageSizeX, 0, self.imageSizeX, self.imageSizeY,
                                             self.X, self.Y + ((self.imageSizeY - self.sizeY) / 2) - 5)
        else:#나머지 타일
            self.specialTile_image.clip_draw(0, 0, self.imageSizeX, self.imageSizeY,
                                             self.X, self.Y + ((self.imageSizeY - self.sizeY) / 2))

    def frame_move(self):
        if self.breakingOption == 0:
            if self.frameTime + 0.1 < time.time():
                self.frameTime = time.time()
                self.frame += 1
                if self.frame > self.frameMax:
                    self.isDeath = True
        elif self.breakingOption == 2:
            self.isDeath = True

    def bush_frame_move(self):
        if (self.breakingOption != 2):
            return

        if self.isPlayerCollision == True:
            if self.frameTime + 0.25 < time.time():
                self.frameTime = time.time()
                self.frame += 1
                if self.frame > self.frameMax:
                    self.frame = 0
        else:
            self.frame = 0

    def collisionBubbleEffect(self):
        if self.type == 0:
            if self.breakingOption != 1:
                for i in Scene_NormalStage.gObjList[6]:
                    if Manager_Collision.collisionMiniIntersectRect(i, self):
                        self.isCollision = True
                        break
        elif self.type == 1:
            if self.breakingOption != 1:
                for i in Scene_BossStage.gObjList[6]:
                    if Manager_Collision.collisionMiniIntersectRect(i, self):
                        self.isCollision = True
                        break

    def collisionBubble(self):
        if self.type == 0:
            if self.breakingOption == 2:
                for i in Scene_NormalStage.gObjList[5]:
                    if Manager_Collision.collisionMiniIntersectRect(self, i):
                        i.isBushCheck = True
        elif self.type == 1: pass

    def collisionItem(self):
        if self.type == 0:
            if self.breakingOption == 2:
                #부쉬와의 충돌
                for i in Scene_NormalStage.gObjList[4]:
                    i.isBushCheck = False
                    if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                        i.isBushCheck = True
            else:
                for i in Scene_NormalStage.gObjList[4]:
                    #다트의 충돌
                    if (i.itemNumber == 8):
                        if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                            i.isDelete = True
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[4]:
                if (i.itemNumber == 8):
                    if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                        i.isDelete = True