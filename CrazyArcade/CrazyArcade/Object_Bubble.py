# coding: cp949
from pico2d import *
import time
import math

import Scene_NormalStage
import Scene_BossStage

import Manager_Collision

import Object
import Object_BubbleEffect

class Bubble(Object.GameObject):
    def __init__(self, _x, _y, _type, _power):
        #ǳ�� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 38, 38
        #ǳ���� �Ӽ�(�븻��0, ������1)
        self.type, self.power = _type, _power
        self.birth, self.birthTime = 0, time.time()
        self.isCollision = False #�÷��̾�� �����Ÿ��� ������ �浹�� �����ϵ��� ����� ����
        # �̹��� ���뵵�� ����
        self.bubble_image = None
        self.frame = None
        self.frameMax = None
        self.frameTime = 0
        self.isBushCheck = False

    def __del__(self):
        self.exit()

    def enter(self):
        # �̹��� ���뵵�� ����
        self.bubble_image = load_image('..\\Sprite\\03.InGame\\Bubble\\Bubble.png')
        self.frame = 0
        self.frameMax = 3
        self.frameTime = time.time()

    def exit(self):
        del (self.bubble_image)
        self.createBubbleEffect()

    def update(self, _events):
        #�浹�Ǵ����� ���� Ȯ��
        if self.isCollision == False:
            if self.type == 0:
                tempX, tempY = Scene_NormalStage.gObjList[0][0].X - self.X, Scene_NormalStage.gObjList[0][0].Y - self.Y
                tempdistance = math.sqrt((tempX * tempX) + (tempY * tempY))
                if tempdistance > 40:
                    self.isCollision = True
            elif self.type == 1:
                tempX, tempY = Scene_BossStage.gObjList[0][0].X - self.X, Scene_BossStage.gObjList[0][0].Y - self.Y
                tempdistance = math.sqrt((tempX * tempX) + (tempY * tempY))
                if tempdistance > 40:
                    self.isCollision = True

        # ��ǳ�� ����
        if self.birth == 3:
            return False

        #��Ÿ�� �Լ� �߰�
        if ((self.birthTime + 1) < time.time()):
            self.birthTime = time.time()
            self.birth += 1

        #�浹
        self.collisionPlayer()

        #�ִϸ��̼� �κ�
        self.frame_move()

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if self.isBushCheck: pass
        else:
            self.bubble_image.clip_draw((self.frame * 40), 0, 40, 40, self.X, self.Y)

    def frame_move(self):
        if (self.frameTime + 0.25 < time.time()):
            self.frameTime = time.time()
            self.frame += 1

            if self.frame > self.frameMax:
                self.frame = 0

    def collisionPlayer(self):
        if self.type == 0:
            if (len(Scene_NormalStage.gObjList[0]) > 0):
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(Scene_NormalStage.gObjList[0][0], self)
                if (isCollision == True) and (self.isCollision == True):
                    Manager_Collision.collisionAABB(Scene_NormalStage.gObjList[0][0], self, left, top, right, bottom)
                    Scene_NormalStage.gObjList[0][0].isSlidingPlayer = False
        elif self.type == 1:
            if (len(Scene_BossStage.gObjList[0]) > 0):
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(Scene_BossStage.gObjList[0][0], self)
                if (isCollision == True) and (self.isCollision == True):
                     Manager_Collision.collisionAABB(Scene_BossStage.gObjList[0][0], self, left, top, right, bottom)
                     Scene_BossStage.gObjList[0][0].isSlidingPlayer = False

    def createBubbleEffect(self):
        isTopEnd, isBottomEnd, isLeftEnd, isRightEnd = False, False, False, False
        isTopNonDestroy, isBottomNonDestroy, isLeftNonDestroy, isRightNonDestroy = False, False, False, False
        indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
        posX, posY = 40 + (indexX * 40), (600 - 60) - (40 * indexY)
        #����ȿ�� ����(0���,1��,2�Ʒ�,3������,4����,5������,6�Ʒ�����,7�����ʿ���,8���ʿ���)
        if self.type == 0:
            #���
            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(posX, posY, self.type, 0)
            tempBubbleEffect.enter()
            Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
            for i in range(0, self.power):
                #��
                tempX, tempY = posX, posY + (i + 1) * 40
                if (indexY - (i + 1)) < 0:
                    isTopEnd = True
                if isTopEnd == False:
                    for j in Scene_NormalStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isTopNonDestroy = True
                            isTopEnd = True
                            break
                    if (i + 1 == self.power) or (isTopEnd == True):
                        if (isTopNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 1)
                            tempBubbleEffect.enter()
                            Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
                        isTopEnd = True
                    if isTopEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 5)
                        tempBubbleEffect.enter()
                        Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
                #��
                tempX, tempY = posX, posY - (i + 1) * 40
                if (indexY + (i + 1)) > 12:
                    isBottomEnd = True
                if isBottomEnd == False:
                    for j in Scene_NormalStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isBottomNonDestroy = True
                            isBottomEnd = True
                            break
                    if (i + 1 == self.power) or (isBottomEnd == True):
                        if (isBottomNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 2)
                            tempBubbleEffect.enter()
                            Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
                        isBottomEnd = True
                    if isBottomEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 6)
                        tempBubbleEffect.enter()
                        Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
                #��
                tempX, tempY = posX + (i + 1) * 40, posY
                if (indexX + (i + 1)) > 14:
                    isRightEnd = True
                if isRightEnd == False:
                    for j in Scene_NormalStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isRightNonDestroy = True
                            isRightEnd = True
                            break
                    if (i + 1 == self.power) or (isRightEnd == True):
                        if (isRightNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 3)
                            tempBubbleEffect.enter()
                            Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
                        isRightEnd = True
                    if isRightEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 7)
                        tempBubbleEffect.enter()
                        Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
                #��
                tempX, tempY = posX - (i + 1) * 40, posY
                if (indexX - (i + 1)) < 0:
                    isLeftEnd = True
                if isLeftEnd == False:
                    for j in Scene_NormalStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isLeftNonDestroy = True
                            isLeftEnd = True
                            break
                    if (i + 1 == self.power) or (isLeftEnd == True):
                        if (isLeftNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 4)
                            tempBubbleEffect.enter()
                            Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
                        isLeftEnd = True
                    if isLeftEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 8)
                        tempBubbleEffect.enter()
                        Scene_NormalStage.gObjList[6].append(tempBubbleEffect)
        elif self.type == 1:
            #���
            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(posX, posY, self.type, 0)
            tempBubbleEffect.enter()
            Scene_BossStage.gObjList[6].append(tempBubbleEffect)
            for i in range(0, self.power):
                #��
                tempX, tempY = posX, posY + (i + 1) * 40
                if (indexY - (i + 1)) < 0:
                    isTopEnd = True
                if isTopEnd == False:
                    for j in Scene_BossStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isTopNonDestroy = True
                            isTopEnd = True
                            break
                    if (i + 1 == self.power) or (isTopEnd == True):
                        if (isTopNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 1)
                            tempBubbleEffect.enter()
                            Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                        isTopEnd = True
                    if isTopEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 5)
                        tempBubbleEffect.enter()
                        Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                #��
                tempX, tempY = posX, posY - (i + 1) * 40
                if (indexY + (i + 1)) > 12:
                    isBottomEnd = True
                if isBottomEnd == False:
                    for j in Scene_BossStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isBottomNonDestroy = True
                            isBottomEnd = True
                            break
                    if (i + 1 == self.power) or (isBottomEnd == True):
                        if (isBottomNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 2)
                            tempBubbleEffect.enter()
                            Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                        isBottomEnd = True
                    if isBottomEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 6)
                        tempBubbleEffect.enter()
                        Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                #��
                tempX, tempY = posX + (i + 1) * 40, posY
                if (indexX + (i + 1)) > 14:
                    isRightEnd = True
                if isRightEnd == False:
                    for j in Scene_BossStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isRightNonDestroy = True
                            isRightEnd = True
                            break
                    if (i + 1 == self.power) or (isRightEnd == True):
                        if (isRightNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 3)
                            tempBubbleEffect.enter()
                            Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                        isRightEnd = True
                    if isRightEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 7)
                        tempBubbleEffect.enter()
                        Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                #��
                tempX, tempY = posX - (i + 1) * 40, posY
                if (indexX - (i + 1)) < 0:
                    isLeftEnd = True
                if isLeftEnd == False:
                    for j in Scene_BossStage.gObjList[3]:
                        if (Manager_Collision.collisionPtInRect(j, tempX, tempY)) and (j.breakingOption != 2):
                            if (j.breakingOption == 1):
                                isLeftNonDestroy = True
                            isLeftEnd = True
                            break
                    if (i + 1 == self.power) or (isLeftEnd == True):
                        if (isLeftNonDestroy == False):
                            tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 4)
                            tempBubbleEffect.enter()
                            Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                        isLeftEnd = True
                    if isLeftEnd == False:
                        tempBubbleEffect = Object_BubbleEffect.BubbleEffect(tempX, tempY, self.type, 8)
                        tempBubbleEffect.enter()
                        Scene_BossStage.gObjList[6].append(tempBubbleEffect)