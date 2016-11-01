# coding: cp949
from pico2d import *
import time
import math

import Manager_ASTAR

import Scene_NormalStage
import Scene_BossStage

import Object

class Monster(Object.GameObject):
    def __init__(self, _x, _y, _type, _dir = 0, _state = 0):
        #몬스터 위치 및 이미지와 충돌 체크용 사이즈
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 39, 39
        #몬스터의 속성(노말은0, 보스면1)
        #state는 0이면 움직임 1이면 죽는과정
        #방향은 0하 1좌 2우 3상 (4죽음 5죽음)
        self.type = _type
        self.dir, self.state = _dir, _state
        self.speed = 2
        self.isDelete, self.isCollision = False, False
        # 이미지 사용용도의 변수
        self.monster_image = None
        self.imageSizeX, self.imageSizeY = 41, 39
        self.frame = None
        self.frameTime = None

        #AStar용 리스트
        self.AStarList = []
        self.targetIndex = 0

    def __del__(self):
        self.exit()

    def enter(self):
        # 이미지 사용용도의 변수
        self.monster_image = load_image('..\\Sprite\\03.InGame\\Monster\\Monster_Normal.png')
        self.imageSizeX, self.imageSizeY = 41, 39
        self.frame = 0
        self.frameTime = time.time()

    def exit(self):
        del (self.monster_image)
        self.AStarList.clear()

    def update(self, _events):
        #프레임 움직임
        if (self.frameTime + 0.25 < time.time()):
            self.frameTime = time.time()
            self.frame += 1
            if self.state == 0:
                if self.frame > 1:
                    self.frame = 0
            elif self.state == 1:#죽는 프레임 전부 지났을경우
                if self.frame > 3:
                    self.frame = 0
                    self.isDelete = True
        #죽음처리
        if (self.isCollision == True) and (self.state == 0):
            self.state = 1
            self.frame = 0
        #삭제처리
        if self.isDelete == True:
            return False
        #에이스타 만들기
        if self.type == 0:
            if (self.astarTargetCheck()) and (len(Scene_NormalStage.gObjList[0]) > 0):
                self.AStarList.clear()
                Manager_ASTAR.AStarStart(self.X, self.Y, Scene_NormalStage.gObjList[0][0].X, Scene_NormalStage.gObjList[0][0].Y, self.type)
                for i in Manager_ASTAR.gBestList:
                    self.AStarList.append(i)
        elif self.type == 1:
            pass
        #에이스타 움직임
        self.astarMove()

    def draw(self):
        # 프레임이 시작하는 그림에서의 X좌표, Y좌표(Y좌표는 아래서부터 1) => 왼쪽 아래부터 오른쪽 위까지 하나를 그림
        if self.state == 0:
            self.monster_image.clip_draw(self.imageSizeX * self.frame, 234 - ((self.dir + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y)
        elif self.state == 1:
            tempX = (int)(self.frame % 2)
            tempY = (int)(self.frame / 2) + 4
            self.monster_image.clip_draw(self.imageSizeX * tempX, 234 - ((tempY + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y)

    #astar
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

            if distance < 5:
                self.AStarList.remove(self.AStarList[0])
        elif self.type == 1:
            pass
        