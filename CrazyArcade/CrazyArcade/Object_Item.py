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
        #��Ʈ�� ��쿡�� ����
        #���Ͽ��� 0 1 2 3
        self.dir = _dir
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
        #�Ѿ�� False ��ȯ���� ����
        if self.itemNumber == 8:
            if self.dir == 0:
                pass
            elif self.dir == 1:
                pass
            elif self.dir == 2:
                pass
            elif self.dir == 3:
                pass

        #�浹
        #Ÿ��(�ν�Ÿ���̶�) + �÷��̾�(��Ʈ����) + ��ǳ��(��Ʈ�϶���) + ��ǳ��ȿ��(��Ʈ����) �浹

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if self.isBushCheck: pass
        elif self.itemNumber == 8:
            self.item_image.clip_draw((self.dir * 40), 0, 40, 40, self.X, self.Y)
        else:
            self.item_image.clip_draw((self.itemNumber * 40), 0, 40, 40, self.X, self.Y)