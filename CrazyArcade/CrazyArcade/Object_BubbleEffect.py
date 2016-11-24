# coding: cp949
from pico2d import *
import time

import Scene_NormalStage
import Scene_BossStage

import Manager_Collision
import Manager_Sound

import Object

class BubbleEffect(Object.GameObject):
    def __init__(self, _x, _y, _type, _dir):
        #ǳ��ȿ�� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 30, 30
        #ǳ��ȿ���� �Ӽ�
        self.type = _type  # �븻��0, ������1
        self.dir = _dir #0���,1��,2�Ʒ�,3������,4����,5������,6�Ʒ�����,7�����ʿ���,8���ʿ���
        self.isDamage = False
        # �̹��� ���뵵�� ����
        self.bubbleEffect_image = None
        self.frame = None
        self.frameMax = None
        self.frameTime = 0

    def __del__(self):
        self.exit()

    def enter(self):
        # �̹��� ���뵵�� ����
        self.bubbleEffect_image = load_image('..\\Sprite\\03.InGame\\Bubble\\BubbleFlow.png')
        self.frame = 0
        self.frameMax = 3
        self.frameTime = time.time()

    def exit(self):
        del (self.bubbleEffect_image)

    def update(self, _frametime, _events):
        #������ ����
        if (self.frameTime + 0.1 < time.time()):
            self.frameTime = time.time()
            self.frame += 1
            if self.frame > self.frameMax:
                self.frame = 0
                return False
        #�浹
        self.collisionPlayer()
        self.collisionBubble()

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        self.bubbleEffect_image.clip_draw((self.frame * 40), (360 - ((self.dir + 1) * 40)),
                                        40, 40, self.X, self.Y)

    def collisionPlayer(self):
        if self.type == 0:
            if (len(Scene_NormalStage.gObjList[0]) > 0):
                if (Scene_NormalStage.gObjList[0][0].birth == 0) and (Manager_Collision.collisionMiniIntersectRect(Scene_NormalStage.gObjList[0][0], self)):
                    Scene_NormalStage.gObjList[0][0].player_state = 'STATE_BUBBLE'
                    Scene_NormalStage.gObjList[0][0].birth = 1
                    Scene_NormalStage.gObjList[0][0].frame = 0
                    Scene_NormalStage.gObjList[0][0].isSlidingPlayer = False
                    Manager_Sound.PlayEffectSound('CHAR_FIXED')
        elif self.type == 1:
            if (len(Scene_BossStage.gObjList[0]) > 0):
                if (Scene_BossStage.gObjList[0][0].birth == 0) and (Manager_Collision.collisionMiniIntersectRect(Scene_BossStage.gObjList[0][0], self)):
                    Scene_BossStage.gObjList[0][0].player_state = 'STATE_BUBBLE'
                    Scene_BossStage.gObjList[0][0].birth = 1
                    Scene_BossStage.gObjList[0][0].frame = 0
                    Scene_BossStage.gObjList[0][0].isSlidingPlayer = False
                    Manager_Sound.PlayEffectSound('CHAR_FIXED')

    def collisionBubble(self):
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[5]:
                if Manager_Collision.collisionMiniIntersectRect(i, self):
                    Scene_NormalStage.gObjList[5].remove(i)
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[5]:
                if Manager_Collision.collisionMiniIntersectRect(i, self):
                    Scene_BossStage.gObjList[5].remove(i)