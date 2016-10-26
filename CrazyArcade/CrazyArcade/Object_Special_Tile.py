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
        # Ÿ�� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 40, 40
        self.imageSizeX, self.imageSizeY = None, None
        # Ÿ���� �Ӽ�
        self.type = _type  # �븻��0, ������1
        self.imageValue = _imagevalue  # � �̸̹� ���������� ����(0~1 / 0~3 / 0)
        self.breakingOption = _breakingOption  # �μ������� �ƴ���(0�μ��� 1�Ⱥμ��� 2�ν�)
        self.events = None
        self.isDeath = False #�������� ��� �������� True�� ����
        self.isCollision = False #�浹�ϸ� True�� ����
        self.dropItem = random.randint(0, 100) #�������� ����� Ȯ��
        # �̹��� ���뵵�� ����
        self.specialTile_image = None
        self.frame = 0
        self.frameMax = None
        self.frameTime = None
        self.isFrameMove = None

    def __del__(self):
        self.exit()

        if self.breakingOption == 0: pass
        #������ Ÿ���� �ɼǺ���(len(Scene_NormalStage.gTileList) > indexY) �̰ɷ��ϸ� �� �߰��� indexX�� �ٲ�°ǰ�
        indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
        if self.type == 0:
            if len(Scene_NormalStage.gTileList[indexY]) > indexX:
                Scene_NormalStage.gTileList[indexY][indexX].changeOption(0)
            else: print('error')
        elif self.type == 1:
            if len(Scene_BossStage.gTileList[indexY]) > indexX:
                Scene_BossStage.gTileList[indexY][indexX].changeOption(0)
            else: print('error')

    def enter(self):
        # �̹��� ���뵵�� ����
        if self.type == 0:
            if self.breakingOption == 0:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_1\\Box_1.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_1\\Box_2.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
            elif self.breakingOption == 1:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_1\\Box_3.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_1\\Box_4.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 2:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_1\\Box_5.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 3:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_1\\Box_6.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 70
            elif self.breakingOption == 2:
                self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_1\\Box_7.png')
                self.frameMax = 4
                self.frameTime = time.time()
                self.isFrameMove = True
                self.imageSizeX, self.imageSizeY = 48, 65
                self.sizeX, self.sizeY = 30, 30
                self.isPlayerCollision = False
        #���� ��������
        elif self.type == 1:
            if self.breakingOption == 0:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_2\\Box_1.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_2\\Box_2.png')
                    self.frameMax = 8
                    self.frameTime = time.time()
                    self.isFrameMove = True
                    self.imageSizeX, self.imageSizeY = 40, 45
            elif self.breakingOption == 1:
                if self.imageValue == 0:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_2\\Box_3.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 57
                elif self.imageValue == 1:
                    self.specialTile_image = load_image('..\\Sprite\\03.InGame\\Map_2\\Box_4.png')
                    self.isFrameMove = False
                    self.imageSizeX, self.imageSizeY = 40, 70

    def exit(self):
        del (self.specialTile_image)

        #�������� ���
        if self.breakingOption == 0:
            if self.dropItem < 50:
                if self.type == 0:
                    tempItem = Object_Item.Item(self.X, self.Y, self.type, 0)
                    tempItem.enter()
                    Scene_NormalStage.gObjList[4].append(tempItem)
                elif self.type == 1:
                    tempItem = Object_Item.Item(self.X, self.Y, self.type, 0)
                    tempItem.enter()
                    Scene_BossStage.gObjList[4].append(tempItem)

    def update(self, _events):
        if self.isDeath == True:
            return False

        #�浹üũ
        self.collisionBubbleEffect()
        self.collisionBubble()

        #�浹�Ǹ� ������ �����ϰ� �����ϴ°�
        self.bush_frame_move()
        if (self.isCollision == True) and (self.isFrameMove == True):
            self.frame_move()

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if self.breakingOption == 0:#�μ����� Ÿ��
            if self.imageValue == 0 or self.imageValue == 1:
                tempFrame = (self.frame % 3)
                tempScene = (int)(self.frame / 3)
                self.specialTile_image.clip_draw(tempFrame * self.imageSizeX, 135 - (tempScene + 1) * self.imageSizeY,
                                                 self.imageSizeX, self.imageSizeY,
                                                 self.X, self.Y + ((self.imageSizeY - self.sizeY) / 2))
        elif self.breakingOption == 2:#�ν�
            self.specialTile_image.clip_draw(self.frame * self.imageSizeX, 0, self.imageSizeX, self.imageSizeY,
                                             self.X, self.Y + ((self.imageSizeY - self.sizeY) / 2) - 5)
        else:#������ Ÿ��
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
                    isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(i, self)
                    if isCollision == True:
                        self.isCollision = True
                        break
        elif self.type == 1:
            if self.breakingOption != 1:
                for i in Scene_BossStage.gObjList[6]:
                    isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(i, self)
                    if isCollision == True:
                        self.isCollision = True
                        break

    def collisionBubble(self):
        if self.type == 0:
            if self.breakingOption == 2:
                for i in Scene_NormalStage.gObjList[5]:
                    isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(self, i)
                    if isCollision == True:
                        i.isBushCheck = True
                    else:
                        i.isBushCheck = False
            else: pass
        elif self.type == 1: pass
