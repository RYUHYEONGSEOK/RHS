# coding: cp949
from pico2d import *
import time
import math

import Manager_ASTAR

import Scene_NormalStage
import Scene_BossStage

import Object

class Monster(Object.GameObject):
    def __init__(self, _x, _y, _type, _dir = 0, _state = 0):
        #���� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 39, 39
        #������ �Ӽ�(�븻��0, ������1)
        #state�� 0�̸� ������ 1�̸� �״°���
        #������ 0�� 1�� 2�� 3�� (4���� 5����)
        self.type = _type
        self.dir, self.state = _dir, _state
        self.speed = 2
        self.isDelete, self.isCollision = False, False
        # �̹��� ���뵵�� ����
        self.monster_image = None
        self.imageSizeX, self.imageSizeY = 41, 39
        self.frame = None
        self.frameTime = None

        #AStar�� ����Ʈ
        self.AStarList = []
        self.targetIndex = 0

    def __del__(self):
        self.exit()

    def enter(self):
        # �̹��� ���뵵�� ����
        self.monster_image = load_image('..\\Sprite\\03.InGame\\Monster\\Monster_Normal.png')
        self.imageSizeX, self.imageSizeY = 41, 39
        self.frame = 0
        self.frameTime = time.time()

    def exit(self):
        del (self.monster_image)
        self.AStarList.clear()

    def update(self, _events):
        #������ ������
        if (self.frameTime + 0.25 < time.time()):
            self.frameTime = time.time()
            self.frame += 1
            if self.state == 0:
                if self.frame > 1:
                    self.frame = 0
            elif self.state == 1:#�״� ������ ���� ���������
                if self.frame > 3:
                    self.frame = 0
                    self.isDelete = True
        #����ó��
        if (self.isCollision == True) and (self.state == 0):
            self.state = 1
            self.frame = 0
        #����ó��
        if self.isDelete == True:
            return False
        #���̽�Ÿ �����
        if self.type == 0:
            if (self.astarTargetCheck()) and (len(Scene_NormalStage.gObjList[0]) > 0):
                self.AStarList.clear()
                Manager_ASTAR.AStarStart(self.X, self.Y, Scene_NormalStage.gObjList[0][0].X, Scene_NormalStage.gObjList[0][0].Y, self.type)
                for i in Manager_ASTAR.gBestList:
                    self.AStarList.append(i)
        elif self.type == 1:
            pass
        #���̽�Ÿ ������
        self.astarMove()

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if self.state == 0:
            self.monster_image.clip_draw(self.imageSizeX * self.frame, 234 - ((self.dir + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y)
        elif self.state == 1:
            tempX = (int)(self.frame % 2)
            tempY = (int)(self.frame / 2) + 4
            self.monster_image.clip_draw(self.imageSizeX * tempX, 234 - ((tempY + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y)

    #astar
    def astarTargetCheck(self):
        if self.type == 0:
            if len(Scene_NormalStage.gObjList[0]) > 0:
                indexX, indexY = (int)((Scene_NormalStage.gObjList[0][0].X - 20) / 40), (int)((560 - Scene_NormalStage.gObjList[0][0].Y) / 40)
                if self.targetIndex != indexX + indexY * 13:
                    self.targetIndex = indexX + indexY * 13
                    return True
                return False
            return False
        elif self.type == 1:
            if len(Scene_BossStage.gObjList[0]) > 0:
                indexX, indexY = (int)((Scene_BossStage.gObjList[0][0].X - 20) / 40), (int)((560 - Scene_BossStage.gObjList[0][0].Y) / 40)
                if self.targetIndex != indexX + indexY * 13:
                    self.targetIndex = indexX + indexY * 13
                    return True
                return False
            return False

    def astarMove(self):
        if len(self.AStarList) == 0:
            return

        moveIndex = self.AStarList[0]

        if self.type == 0:
            dirX = Scene_NormalStage.gTileList[moveIndex].X - self.X
            dirY = Scene_NormalStage.gTileList[moveIndex].Y - self.Y

            distance = math.sqrt(dirX * dirX + dirY * dirY)

            dirX = (int)(dirX * self.speed / distance)
            dirY = (int)(dirY * self.speed / distance)

            self.X += dirX
            self.Y += dirY

            if distance < 5:
                self.AStarList.remove(self.AStarList[0])
        elif self.type == 1:
            pass
        