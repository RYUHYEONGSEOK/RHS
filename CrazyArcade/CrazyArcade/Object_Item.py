# coding: cp949
from pico2d import *

import Scene_NormalStage
import Scene_BossStage

import Manager_Collision

import Object

class Item(Object.GameObject):
    def __init__(self, _x, _y, _type, _itemNum, _dir = 0):
        #������ ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 38, 38
        #�������� �Ӽ�(�븻��0, ������1)
        #�������� ��ȣ(0~8) : ��ǳ��,�Ŀ�,�Ź�,�Ŀ��ִ�,�ӵ��ִ�,����,����,�ٳ���,��Ʈ
        self.type, self.itemNumber = _type, _itemNum
        #��Ʈ�� ��쿡�� ����(���Ͽ��� 0 1 2 3)
        self.dir = _dir
        self.isDelete = False
        # �̹��� ���뵵�� ����
        self.item_image = None
        self.isBushCheck = False

    def __del__(self):
        self.exit()

    def enter(self):
        # �̹��� ���뵵�� ����
        if self.itemNumber == 8:
            self.item_image = load_image('..\\Sprite\\03.InGame\\Item\\Dart.png')
        else:
            self.item_image = load_image('..\\Sprite\\03.InGame\\Item\\Item.png')

    def exit(self):
        del (self.item_image)

    def update(self, _events):
        #��Ʈ�� �������� ����
        if self.itemNumber == 8:
            if self.dir == 0:
                self.Y += 8
            elif self.dir == 1:
                self.Y -= 8
            elif self.dir == 2:
                self.X += 8
            elif self.dir == 3:
                self.X -= 8
            #�� �Ѿ�� ����
            if self.X > 620 or self.X < 20:
                self.isDelete = True
            if self.Y > 550 or self.Y < 40:
                self.isDelete = True
        #�浹
        if (self.itemNumber != 8):
            self.collisionPlayer()
            self.collisionBubbleEffect()
        else:
            self.collisionBubble()
        #����ó��
        if self.isDelete == True:
            return False

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if self.isBushCheck: pass
        elif self.itemNumber == 8:
            self.item_image.clip_draw((self.dir * 40), 0, 40, 40, self.X, self.Y)
        else:
            self.item_image.clip_draw((self.itemNumber * 40), 0, 40, 40, self.X, self.Y)

    def collisionPlayer(self):
        if self.type == 0:
            if (len(Scene_NormalStage.gObjList[0]) > 0):
                if(Manager_Collision.collisionMiniIntersectRect(self, Scene_NormalStage.gObjList[0][0]) == True):
                    self.isDelete = True
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
                    #�ٳ��� ���߿� �߰�
                    elif self.itemNumber == 7:
                        pass
        elif self.type == 1:
            if (len(Scene_BossStage.gObjList[0]) > 0):
                if(Manager_Collision.collisionMiniIntersectRect(self, Scene_BossStage.gObjList[0][0]) == True):
                    self.isDelete = True
                    if self.itemNumber == 0:
                        Scene_BossStage.gObjList[0][0].bubbleCount += 1
                    elif self.itemNumber == 1:
                        Scene_BossStage.gObjList[0][0].power += 1
                    elif self.itemNumber == 2:
                        Scene_BossStage.gObjList[0][0].speed += 1
                    elif self.itemNumber == 3:
                        Scene_BossStage.gObjList[0][0].power = 5
                    elif self.itemNumber == 4:
                        Scene_BossStage.gObjList[0][0].speed = 6
                    #�ٳ��� ���߿� �߰�
                    elif self.itemNumber == 7:
                        pass

    def collisionBubble(self):
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[5]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True
                    i.birth = 3
                    break
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[5]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True
                    i.birth = 3
                    break

    def collisionBubbleEffect(self):
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[6]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True
                    break
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[6]:
                if (Manager_Collision.collisionMiniIntersectRect(i, self) == True):
                    self.isDelete = True
                    break