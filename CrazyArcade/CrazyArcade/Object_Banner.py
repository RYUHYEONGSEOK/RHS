# coding: cp949
from pico2d import *
import time

import Object

class Banner(Object.GameObject):
    def __init__(self, _x, _y, _type, _bannertype):
        #��� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 405, 62
        #����� �Ӽ�(�븻��0, ������1)
        #����� ����(0���� 1�㸮�� 2�� 5����)
        self.type, self.bannerType = _type, _bannertype
        self.isDelete = False
        # �̹��� ���뵵�� ����
        self.banner_image = None
        self.start_time = None

    def __del__(self):
        self.exit()

    def enter(self):
        # �̹��� ���뵵�� ����
        self.banner_image = load_image('..\\Sprite\\03.InGame\\InGame_Image_Word.png')
        self.start_time = time.time()

    def exit(self):
        del (self.banner_image)

    def update(self, _frametime, _events):
        #3�� ������ ����
        if (self.start_time + 3 < time.time()):
            self.start_time = time.time()
            self.isDelete = True
        
        #����ó��
        if self.isDelete == True:
            return False

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        self.banner_image.clip_draw(0, 372 - ((self.bannerType + 1) * self.sizeY), self.sizeX, self.sizeY, self.X, self.Y)