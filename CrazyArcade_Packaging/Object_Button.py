# coding: cp949
from pico2d import *

import Manager_Sound

class Button:
    def __init__(self, _x, _y, _type):
        self.buttonType = _type
        self.X ,self.Y = _x, _y
        self.mouseX, self.mouseY = 0, 0
        self.events = None;
        #�浹���� �ƴ��� üũ�ϴ� �κа� �̹���
        self.frame = 0
        self.isFirst = False

    def __del__(self):
        self.exit()

    def enter(self):
        #��ư�� ������ �ν�(1.���۹�ư 2.�ʼ���1 3.�ʼ���2 4.������ 5~8.�κ�����ۼ�����)
        if self.buttonType == 1:
            self.sizeX, self.sizeY = 192, 55
            self.buttonImage = load_image('.\\Sprite\\02.Lobby\\Lobby_Button_Start.png')
        elif self.buttonType == 2:
            self.sizeX, self.sizeY = 135, 21
            self.buttonImage = load_image('.\\Sprite\\02.Lobby\\Loddy_Image_SelectMap_0.png')
        elif self.buttonType == 3:
            self.sizeX, self.sizeY = 135, 21
            self.buttonImage = load_image('.\\Sprite\\02.Lobby\\Loddy_Image_SelectMap_1.png')
        elif self.buttonType == 4:
            self.sizeX, self.sizeY = 140, 32
            self.buttonImage = load_image('.\\Sprite\\03.InGame\\InGame_Button_Out.png')
        elif self.buttonType == 5:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('.\\Sprite\\02.Lobby\\Lobby_QButton.bmp')
        elif self.buttonType == 6:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('.\\Sprite\\02.Lobby\\Lobby_WButton.bmp')
        elif self.buttonType == 7:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('.\\Sprite\\02.Lobby\\Lobby_EButton.bmp')
        elif self.buttonType == 8:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('.\\Sprite\\02.Lobby\\Lobby_RButton.bmp')

    def exit(self):
        del (self.buttonImage)

    def update(self, _events):
        if (((self.X - self.sizeX / 2) < self.mouseX) and ((self.X + self.sizeX / 2) > self.mouseX)) \
                and (((self.Y - self.sizeY / 2) < (600 - self.mouseY)) and ((self.Y + self.sizeY / 2) > (600 - self.mouseY))):
            self.frame = 1
            if self.isFirst == False:
                self.isFirst = True
                Manager_Sound.PlayEffectSound('BUTTON_ON')
        else:
            self.frame = 0
            if self.isFirst == True:
                self.isFirst = False
                Manager_Sound.PlayEffectSound('BUTTON_OFF')

        # Ű�� ������ ���� �޶����� ���ϰ���
        if(self.keycheck(_events)):
            return self.buttonType

    def draw(self):
        #�������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if (self.buttonType == 1) or (self.buttonType == 4):
            self.buttonImage.clip_draw((self.frame * self.sizeX), 0,
                                        self.sizeX, self.sizeY,
                                        self.X, self.Y)
        elif (self.buttonType == 2) or (self.buttonType == 3):
            self.buttonImage.clip_draw(((self.frame - 1) * self.sizeX), 0,
                                       self.sizeX, self.sizeY,
                                       self.X, self.Y)
        elif (self.buttonType >= 5) and (self.buttonType <= 8):
            self.buttonImage.clip_draw(0, 0,
                                       self.sizeX, self.sizeY,
                                       self.X, self.Y)

    def keycheck(self, _events):
        # ���콺���� ����
        self.events = _events

        for event in self.events:
            if event.type == SDL_MOUSEMOTION:
                self.mouseX, self.mouseY = event.x, event.y
            if (event.type, self.frame) == (SDL_MOUSEBUTTONUP, 1):
                Manager_Sound.PlayEffectSound('EMPTY_ON')
                return True