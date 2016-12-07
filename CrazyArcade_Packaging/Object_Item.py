# coding: cp949
from pico2d import *

import Scene_NormalStage
import Scene_BossStage

import Manager_Collision
import Manager_Sound

import Object

class Item(Object.GameObject):
    def __init__(self, _x, _y, _type, _itemNum, _dir = 0):
        #아이템 위치 및 이미지와 충돌 체크용 사이즈
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 30, 30
        #아이템의 속성(노말은0, 보스면1)
        #아이템의 번호(0~8) : 물풍선,파워,신발,파워최대,속도최대,제외,제외,바나나,다트
        self.type, self.itemNumber = _type, _itemNum
        #다트의 경우에는 방향(상하우좌 0 1 2 3)
        self.dir = _dir
        self.isDelete = False
        self.isCollision = False
        # 이미지 사용용도의 변수
        self.item_image = None
        self.isBushCheck = False

    def __del__(self):
        self.exit()

    def enter(self):
        # 이미지 사용용도의 변수
        if self.itemNumber == 8:
            self.item_image = load_image('.\\Sprite\\03.InGame\\Item\\Dart.png')
        else:
            self.item_image = load_image('.\\Sprite\\03.InGame\\Item\\Item.png')

    def exit(self):
        del (self.item_image)

    def update(self, _frametime, _events):
        #바나나에서 충돌체크되는지 체크
        if self.itemNumber == 7:
            if self.isCollision == False:
                if self.type == 0:
                    tempX, tempY = Scene_NormalStage.gObjList[0][0].X - self.X, Scene_NormalStage.gObjList[0][0].Y - self.Y
                    tempdistance = math.sqrt((tempX * tempX) + (tempY * tempY))
                    if tempdistance > 42:
                        self.isCollision = True
                elif self.type == 1:
                    tempX, tempY = Scene_BossStage.gObjList[0][0].X - self.X, Scene_BossStage.gObjList[0][0].Y - self.Y
                    tempdistance = math.sqrt((tempX * tempX) + (tempY * tempY))
                    if tempdistance > 42:
                        self.isCollision = True
        #다트만 움직임을 가짐
        if self.itemNumber == 8:
            if self.dir == 0:
                self.Y += 8 * _frametime * 50
            elif self.dir == 1:
                self.Y -= 8 * _frametime * 50
            elif self.dir == 2:
                self.X += 8 * _frametime * 50
            elif self.dir == 3:
                self.X -= 8 * _frametime * 50
            #벽 넘어가면 삭제
            if self.X > 620 or self.X < 20:
                self.isDelete = True
            if self.Y > 550 or self.Y < 40:
                self.isDelete = True
        #충돌
        if (self.itemNumber != 8):
            self.collisionPlayer()
            self.collisionBubbleEffect()
        else:
            self.collisionBubble()
        #삭제처리
        if self.isDelete == True:
            if self.type == 7:
                Manager_Sound.PlayEffectSound('ITEM_BANANA_OFF')
            else:
                Manager_Sound.PlayEffectSound('ITEM_OFF')
            return False

    def draw(self):
        # 프레임이 시작하는 그림에서의 X좌표, Y좌표(Y좌표는 아래서부터 1) => 왼쪽 아래부터 오른쪽 위까지 하나를 그림
        if self.isBushCheck: pass
        elif self.itemNumber == 8:
            self.item_image.clip_draw((self.dir * 40), 0, 40, 40, self.X, self.Y)
        else:
            self.item_image.clip_draw((self.itemNumber * 40), 0, 40, 40, self.X, self.Y)

    def collisionPlayer(self):
        if self.type == 0:
            if (len(Scene_NormalStage.gObjList[0]) > 0):
                if(Manager_Collision.collisionMiniIntersectRect(self, Scene_NormalStage.gObjList[0][0]) == True):
                    if self.itemNumber == 0:
                        Scene_NormalStage.gObjList[0][0].bubbleCount += 1
                    elif self.itemNumber == 1:
                        Scene_NormalStage.gObjList[0][0].power += 1
                    elif self.itemNumber == 2:
                        Scene_NormalStage.gObjList[0][0].speed += 1
                    elif self.itemNumber == 3:
                        Scene_NormalStage.gObjList[0][0].power = 5
                    elif self.itemNumber == 4:
                        Scene_NormalStage.gObjList[0][0].speed = 6
                    elif self.itemNumber == 7:
                        if self.isCollision == True:
                            Scene_NormalStage.gObjList[0][0].isSlidingPlayer = True
                        else: return
                    self.isDelete = True
        elif self.type == 1:
            if (len(Scene_BossStage.gObjList[0]) > 0):
                if(Manager_Collision.collisionMiniIntersectRect(self, Scene_BossStage.gObjList[0][0]) == True):
                    if self.itemNumber == 0:
                        Scene_BossStage.gObjList[0][0].bubbleCount += 1
                    elif self.itemNumber == 1:
                        Scene_BossStage.gObjList[0][0].power += 1
                    elif self.itemNumber == 2:
                        Scene_BossStage.gObjList[0][0].speed += 1
                    elif self.itemNumber == 3:
                        Scene_BossStage.gObjList[0][0].power = 4
                    elif self.itemNumber == 4:
                        Scene_BossStage.gObjList[0][0].speed = 6
                    elif self.itemNumber == 7:
                        if self.isCollision == True:
                            Scene_BossStage.gObjList[0][0].isSlidingPlayer = True
                        else: return
                    self.isDelete = True

    def collisionBubble(self):
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[5]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True
                    i.birth = 3
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[5]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True
                    i.birth = 3

    def collisionBubbleEffect(self):
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[6]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[6]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True