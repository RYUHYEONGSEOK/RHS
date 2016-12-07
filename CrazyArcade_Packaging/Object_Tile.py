# coding: cp949
from pico2d import *

import Object

class Tile(Object.GameObject):
    def __init__(self, _x = 0, _y = 0, _type = 0, _value = 0, _option = 0):
        # Ÿ�� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 40, 40
        # Ÿ���� �Ӽ�
        self.type = _type  # �븻��0, ������1
        self.value = _value # � �̸̹� ���������� ����
        self.option = _option # ���������ִ� Ÿ������ �ƴ���(0���� / 1�Ұ���)
        # �̹��� ���뵵�� ����
        self.tile_image = None

    def __del__(self):
        self.exit()

    def enter(self):
        # �̹��� ���뵵�� ����
        if self.type == 0:
            self.tile_image = load_image('.\\Sprite\\03.InGame\\Map_1\\Tile.bmp')
        elif self.type == 1:
            self.tile_image = load_image('.\\Sprite\\03.InGame\\Map_2\\Tile.bmp')

    def exit(self):
        del (self.tile_image)

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        self.tile_image.clip_draw((self.value * self.sizeX), 0, self.sizeX, self.sizeY, self.X, self.Y)

    def changeOption(self, _changeOptionValue):
        self.option = _changeOptionValue#0����/ 1�Ұ���