# coding: cp949
from pico2d import *
import time
#import math

#import Manager_ASTAR
import Manager_Collision

import Scene_NormalStage
import Scene_BossStage

import Object

class Monster(Object.GameObject):
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

        #AStar�� ����Ʈ
        #self.AStarList = []
        #self.targetIndex = 0

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
        #self.AStarList.clear()

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

        #���̽�Ÿ �����
        #if self.type == 0:
        #    if (self.astarTargetCheck()) and (len(Scene_NormalStage.gObjList[0]) > 0):
        #        self.AStarList.clear()
        #        Manager_ASTAR.AStarStart(self.X, self.Y, Scene_NormalStage.gObjList[0][0].X, Scene_NormalStage.gObjList[0][0].Y, self.type)
        #        for i in Manager_ASTAR.gBestList:
        #            self.AStarList.append(i)
        #elif self.type == 1:
        #    pass
        #���̽�Ÿ ������
        #if self.type == 0:
        #    self.astarMove()
        #elif self.type == 1:
        #    pass

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
                elif (isCollision == True) and (i.breakingOption == 2):
                    self.isBushCheck = True
                    if i.isPlayerCollision == False:
                        i.isPlayerCollision = True
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

    def collisionPlayer(self):
        if self.type == 0:
            if (len(Scene_NormalStage.gObjList[0]) > 0):
                if (Manager_Collision.collisionMiniIntersectRect(self, Scene_NormalStage.gObjList[0][0]) == True):
                    Scene_NormalStage.gObjList[0][0].birth = 1
                    Scene_NormalStage.gObjList[0][0].player_state = 'STATE_BUBBLE'
                    self.isCollision = True
                    Scene_NormalStage.gObjList[0][0].isSlidingPlayer = False
                    self.state = 1
        elif self.type == 1:
            if (len(Scene_BossStage.gObjList[0]) > 0):
                if (Manager_Collision.collisionMiniIntersectRect(self, Scene_BossStage.gObjList[0][0]) == True):
                    Scene_BossStage.gObjList[0][0].birth = 1
                    Scene_BossStage.gObjList[0][0].player_state = 'STATE_BUBBLE'
                    self.isCollision = True
                    Scene_BossStage.gObjList[0][0].isSlidingPlayer = False
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

    ###########################################################################astar
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
            self.frame = 0
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

            if distance < 8:
                self.AStarList.remove(self.AStarList[0])
        elif self.type == 1:
            pass