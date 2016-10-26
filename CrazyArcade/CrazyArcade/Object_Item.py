# coding: cp949
from pico2d import *

import Scene_NormalStage
import Scene_BossStage

import Manager_Collision

import Object

class Item(Object.GameObject):
    def __init__(self, _x, _y, _type, _itemNum, _dir = 0):
        #아이템 위치 및 이미지와 충돌 체크용 사이즈
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 38, 38
        #아이템의 속성(노말은0, 보스면1)
        #아이템의 번호(0~8) : 물풍선,파워,신발,파워최대,속도최대,제외,제외,바나나,다트
        self.type, self.itemNumber = _type, _itemNum
        #다트의 경우에는 방향
        #상하우좌 0 1 2 3
        self.dir = _dir
        # 이미지 사용용도의 변수
        self.item_image = None
        self.isBushCheck = False

    def __del__(self):
        self.exit()

    def enter(self):
        # 이미지 사용용도의 변수
        if self.itemNumber == 8:
            self.item_image = load_image('..\\Sprite\\03.InGame\\Item\\Dart.png')
        else:
            self.item_image = load_image('..\\Sprite\\03.InGame\\Item\\Item.png')

    def exit(self):
        del (self.item_image)

    def update(self, _events):
        #다트만 움직임을 가짐
        #넘어가면 False 반환으로 삭제
        if self.itemNumber == 8:
            if self.dir == 0:
                pass
            elif self.dir == 1:
                pass
            elif self.dir == 2:
                pass
            elif self.dir == 3:
                pass

        #충돌
        #타일(부쉬타일이랑) + 플레이어(다트빼고) + 물풍선(다트일때만) + 물풍선효과(다트빼고) 충돌

    def draw(self):
        # 프레임이 시작하는 그림에서의 X좌표, Y좌표(Y좌표는 아래서부터 1) => 왼쪽 아래부터 오른쪽 위까지 하나를 그림
        if self.isBushCheck: pass
        elif self.itemNumber == 8:
            self.item_image.clip_draw((self.dir * 40), 0, 40, 40, self.X, self.Y)
        else:
            self.item_image.clip_draw((self.itemNumber * 40), 0, 40, 40, self.X, self.Y)