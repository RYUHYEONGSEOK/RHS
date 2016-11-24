# coding: cp949
from pico2d import *
import time

import Object

class Banner(Object.GameObject):
    def __init__(self, _x, _y, _type, _bannertype):
        #배너 위치 및 이미지와 충돌 체크용 사이즈
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 405, 62
        #배너의 속성(노말은0, 보스면1)
        #배너의 종류(0시작 1허리업 2윈 5루즈)
        self.type, self.bannerType = _type, _bannertype
        self.isDelete = False
        # 이미지 사용용도의 변수
        self.banner_image = None
        self.start_time = None

    def __del__(self):
        self.exit()

    def enter(self):
        # 이미지 사용용도의 변수
        self.banner_image = load_image('..\\Sprite\\03.InGame\\InGame_Image_Word.png')
        self.start_time = time.time()

    def exit(self):
        del (self.banner_image)

    def update(self, _frametime, _events):
        #3초 지나면 삭제
        if (self.start_time + 3 < time.time()):
            self.start_time = time.time()
            self.isDelete = True
        
        #삭제처리
        if self.isDelete == True:
            return False

    def draw(self):
        # 프레임이 시작하는 그림에서의 X좌표, Y좌표(Y좌표는 아래서부터 1) => 왼쪽 아래부터 오른쪽 위까지 하나를 그림
        self.banner_image.clip_draw(0, 372 - ((self.bannerType + 1) * self.sizeY), self.sizeX, self.sizeY, self.X, self.Y)