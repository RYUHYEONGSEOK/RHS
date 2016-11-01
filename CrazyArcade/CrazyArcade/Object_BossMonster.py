# coding: cp949
from pico2d import *
import time

import Manager_Collision

import Scene_NormalStage
import Scene_BossStage

import Object

class BossMonster(Object.GameObject):
    def __init__(self, _x, _y, _type, _dir = 0, _state = 0):
        #���� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 34, 34
        #������ �Ӽ�(�븻��0, ������1)
        #state�� 0�̸� ������ 1�̸� �״°���
        #������ 0�� 1�� 2�� 3�� (4���� 5����)
        self.type = _type
        self.dir, self.state = _dir, _state
        self.speed = 2
        self.isDelete, self.isCollision = False, False
        # �̹��� ���뵵�� ����
        self.isBushCheck = False
        self.monster_image = None
        self.imageSizeX, self.imageSizeY = 41, 39
        self.frame = None
        self.frameTime = None

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

    def update(self, _events):
        #����ó��
        if (self.isCollision == True) and (self.state == 0):
            self.state = 1
            self.frame = 0

        #������
        self.move()
        #�浹ó��
        self.collisionWall()
        self.collisionSpecialTile()
        self.collisionPlayer()
        self.collisionBubble()
        self.collisionBubbleEffect()

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
        if self.isDelete == True:
            return False

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if self.isBushCheck: pass
        elif self.state == 0:
            self.monster_image.clip_draw(self.imageSizeX * self.frame, 234 - ((self.dir + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y)
        elif self.state == 1:
            tempX = (int)(self.frame % 2)
            tempY = (int)(self.frame / 2) + 4
            self.monster_image.clip_draw(self.imageSizeX * tempX, 234 - ((tempY + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y)

    def move(self):
        #������ 0�� 1�� 2�� 3�� (4���� 5����)
        if self.state == 0:
            if self.dir == 0:
                self.Y -= self.speed
            elif self.dir == 1:
                self.X -= self.speed
            elif self.dir == 2:
                self.X += self.speed
            elif self.dir == 3:
                self.Y += self.speed

    def collisionWall(self):
        if self.X < 40:
            self.X = 40
            self.dir = 2
            return
        elif self.X > 600:
            self.X = 600
            self.dir = 1
            return
        if self.Y < 60:
            self.Y = 60
            self.dir = 3
            return
        elif self.Y > 540:
            self.Y = 540
            self.dir = 0
            return

    def collisionSpecialTile(self):
        self.isBushCheck = False
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[3]:
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(self, i)
                if (isCollision == True) and (i.breakingOption != 2):
                    Manager_Collision.collisionAABB(self, i, left, top, right, bottom)
                    if self.dir == 0:
                        self.dir = 3
                    elif self.dir == 1:
                        self.dir = 2
                    elif self.dir == 2:
                        self.dir = 1
                    elif self.dir == 3:
                        self.dir = 0
                    break
                elif (isCollision == True) and (i.breakingOption == 2):
                    self.isBushCheck = True
                    if i.isPlayerCollision == False:
                        i.isPlayerCollision = True
                    break
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[3]:
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(self, i)
                if (isCollision == True) and (i.breakingOption != 2):
                    Manager_Collision.collisionAABB(self, i, left, top, right, bottom)
                    if self.dir == 0:
                        self.dir = 3
                    elif self.dir == 1:
                        self.dir = 2
                    elif self.dir == 2:
                        self.dir = 1
                    elif self.dir == 3:
                        self.dir = 0
                    break

    def collisionPlayer(self):
        if self.type == 0:
            if (len(Scene_NormalStage.gObjList[0]) > 0):
                if (Manager_Collision.collisionMiniIntersectRect(self, Scene_NormalStage.gObjList[0][0]) == True):
                    Scene_NormalStage.gObjList[0][0].birth = 1
                    Scene_NormalStage.gObjList[0][0].player_state = 'STATE_BUBBLE'
                    self.isCollision = True
                    self.state = 1
        elif self.type == 1:
            if (len(Scene_BossStage.gObjList[0]) > 0):
                if (Manager_Collision.collisionMiniIntersectRect(self, Scene_BossStage.gObjList[0][0]) == True):
                    Scene_BossStage.gObjList[0][0].birth = 1
                    Scene_BossStage.gObjList[0][0].player_state = 'STATE_BUBBLE'
                    self.isCollision = True
                    self.state = 1

    def collisionBubble(self):
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[5]:
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(self, i)
                if (isCollision == True):
                    Manager_Collision.collisionAABB(self, i, left, top, right, bottom)
                    if self.dir == 0:
                        self.dir = 3
                    elif self.dir == 1:
                        self.dir = 2
                    elif self.dir == 2:
                        self.dir = 1
                    elif self.dir == 3:
                        self.dir = 0
                    break
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[5]:
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(self, i)
                if (isCollision == True):
                    Manager_Collision.collisionAABB(self, i, left, top, right, bottom)
                    if self.dir == 0:
                        self.dir = 3
                    elif self.dir == 1:
                        self.dir = 2
                    elif self.dir == 2:
                        self.dir = 1
                    elif self.dir == 3:
                        self.dir = 0
                    break

    def collisionBubbleEffect(self):
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[6]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self)):
                    self.isCollision = True
                    self.state = 1
                    break
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[6]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self)):
                    self.isCollision = True
                    self.state = 1
                    break