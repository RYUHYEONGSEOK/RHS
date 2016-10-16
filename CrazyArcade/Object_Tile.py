from pico2d import *

import Object

class Tile(Object.GameObject):
    def __init__(self, _x, _y, _type, _value, _option = 0):
        # 타일 위치 및 이미지와 충돌 체크용 사이즈
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 40, 40
        # 타일의 속성
        self.type = _type  # 노말은0, 보스면1
        self.value = _value # 어떤 이미를 보여줄지에 대한
        self.option = _option # 지나갈수있는 타일인지 아닌지(0가능 / 1불가능)
        # 이미지 사용용도의 변수
        self.tile_image = None

    def __del__(self):
        self.exit()

    def enter(self):
        # 이미지 사용용도의 변수
        if self.type == 0:
            self.tile_image = load_image('Sprite\\03.InGame\\Map_1\\Tile.bmp')
        elif self.type == 1:
            self.tile_image = load_image('Sprite\\03.InGame\\Map_2\\Tile.bmp')

    def exit(self):
        del (self.tile_image)

    def draw(self):
        # 프레임이 시작하는 그림에서의 X좌표, Y좌표(Y좌표는 아래서부터 1) => 왼쪽 아래부터 오른쪽 위까지 하나를 그림
        self.tile_image.clip_draw((self.value * self.sizeX), 0, self.sizeX, self.sizeY, self.X, self.Y)

    def changeOption(self, _changeOptionValue):
        self.option = _changeOptionValue#0가능/ 1불가능