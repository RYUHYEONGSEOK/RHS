# coding: cp949
from pico2d import *
import time

import Manager_Collision
import Manager_Sound

import Scene_BossStage

import Object
import Object_BubbleEffect

class BossMonster(Object.GameObject):
    def __init__(self, _x, _y, _type, _dir = 0, _state = 0):
        #�������� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 100, 100
        #���������� �Ӽ�(�븻��0, ������1)
        #state�� 0������ 1���ݰ���(4��°�� �길4��) 2��ǳ�����ִ°���(5~11)
        #������ 0�� 1�� 2�� 3��
        self.type = _type
        self.dir, self.state = _dir, _state
        self.hp = 10
        self.speed, self.isCrzay = 1, False
        self.isDelete, self.isCollision = False, False
        # �̹��� ���뵵�� ����
        self.bossmonster_image = None
        self.bossHp_image, self.bossHpBar_image = None, None
        self.imageSizeX, self.imageSizeY = None, None
        self.frame = None
        self.frameMax = None
        self.frameTime = None

    def __del__(self):
        self.exit()
        #����
        if self.isDelete == True:
            Manager_Sound.PlayEffectSound('MONSTER_DIE')

    def enter(self):
        # �̹��� ���뵵�� ����
        self.bossmonster_image = load_image('..\\Sprite\\03.InGame\\Monster\\Monster_Boss.png')
        self.bossHp_image = load_image('..\\Sprite\\03.InGame\\Monster\\Monster_HP.png')
        self.bossHpBar_image = load_image('..\\Sprite\\03.InGame\\Monster\\Monster_HPBar.png')
        self.imageSizeX, self.imageSizeY = 120, 207
        self.frame = 0
        self.frameMax = 5
        self.frameTime = time.time()
        #����
        Manager_Sound.PlayEffectSound('BOSS_MOVE')

    def exit(self):
        del (self.bossmonster_image)
        del (self.bossHp_image)
        del (self.bossHpBar_image)

    def update(self, _frametime, _events):
        #����ó��
        if self.isDelete == True:
            return False

        #������
        self.move(_frametime)

        #�浹ó��(���°� �״°����� �ƴҰ�쿡 ����)
        if self.state != 2:
            self.collisionBubble()
            self.collisionBubbleEffect()
        self.collisionPlayer()

        #ü�¿� ���� ��
        if (self.hp < 1) and (self.state != 2):
            self.hp = 0
            self.state = 2
            self.frame = 0
            self.frameMax = 41
        if (self.isCrzay == False) and (self.hp < 6):
            self.isCrzay = True
            self.speed = 2

        #������
        self.framemove()

    def draw(self):
        # �������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        if self.state == 0:
            self.bossmonster_image.clip_draw(self.imageSizeX * self.frame, 2691 - ((self.dir + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y + 55)
            self.bossHpBar_image.clip_draw(0, 0, (int)(53 * (self.hp / 10)), 13, self.X + (int)((self.hp / 10.0 - 1) * 26), self.Y - 50)
            self.bossHp_image.clip_draw(0, 0, 53, 13, self.X, self.Y - 50)  
        elif self.state == 1:
            self.bossmonster_image.clip_draw(self.imageSizeX * self.frame, 2691 - ((4 + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y + 55)
            self.bossHpBar_image.clip_draw(0, 0, (int)(53 * (self.hp / 10)), 13, self.X + (int)((self.hp / 10.0 - 1) * 26), self.Y - 50)
            self.bossHp_image.clip_draw(0, 0, 53, 13, self.X, self.Y - 50)  
        elif self.state == 2:
            tempX = (int)(self.frame % 6)
            tempY = (int)(self.frame / 6) + 5
            self.bossmonster_image.clip_draw(self.imageSizeX * tempX, 2691 - ((tempY + 1) * self.imageSizeY), self.imageSizeX, self.imageSizeY, self.X, self.Y)

    def move(self, _frametime):
        if self.state == 0:
            #������ 0�� 1�� 2�� 3��
            if self.dir == 0:
                self.Y += self.speed * _frametime * 50
            elif self.dir == 1:
                self.Y -= self.speed * _frametime * 50
            elif self.dir == 2:
                self.X += self.speed * _frametime * 50
            elif self.dir == 3:
                self.X -= self.speed * _frametime * 50

            if self.X < 120:
                self.X = 120
                self.dir = 2
                self.state = 1
                self.frame = 0
                self.frameMax = 3
                self.AttackPlayer(0)
            elif self.X > 520:
                self.X = 520
                self.dir = 3
                self.state = 1
                self.frame = 0
                self.frameMax = 3
                self.AttackPlayer(1)

    def framemove(self):
        #state�� 0������ 1���ݰ���(4��°�� �길4��) 2��ǳ�����ִ°���(5~11)
        if self.state == 0:
            if (self.frameTime + 0.25 < time.time()):
                self.frameTime = time.time()
                self.frame += 1

                if self.frame > self.frameMax:
                    self.frame = 0
        elif self.state == 1:
            if (self.frameTime + 0.2 < time.time()):
                self.frameTime = time.time()
                self.frame += 1

                if self.frame > self.frameMax:
                    self.frame = 0
                    self.state = 0
                    self.frameMax = 5
                    #����
                    Manager_Sound.PlayEffectSound('BOSS_MOVE')
        elif self.state == 2:
            if (self.frameTime + 0.25 < time.time()):
                self.frameTime = time.time()
                self.frame += 1

                if self.frame > self.frameMax:
                    self.isDelete = True

    def AttackPlayer(self, _attacktype):
        if self.type == 1:
            if _attacktype == 0:
                for i in range(0, 4):
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(440 + i * 40, 100, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(440 + i * 40, 140, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(440 + i * 40, 180, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(440 + i * 40, 220, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)

            elif _attacktype == 1:
                for i in range(0, 4):
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(80 + i * 40, 100, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(80 + i * 40, 140, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(80 + i * 40, 180, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)
                    tempBubbleEffect = Object_BubbleEffect.BubbleEffect(80 + i * 40, 220, self.type, 0)
                    tempBubbleEffect.enter()
                    Scene_BossStage.gObjList[6].append(tempBubbleEffect)

    def collisionPlayer(self):
        if (len(Scene_BossStage.gObjList[0]) > 0):
            if Manager_Collision.collisionMiniIntersectRect(self, Scene_BossStage.gObjList[0][0]):
                if (self.state != 2):
                    Scene_BossStage.gObjList[0][0].birth = 1
                    Scene_BossStage.gObjList[0][0].player_state = 'STATE_BUBBLE'
                    Scene_BossStage.gObjList[0][0].isSlidingPlayer = False
                    Manager_Sound.PlayEffectSound('CHAR_FIXED')
                elif (self.state == 2) and (self.frame < 22):
                    self.frame = 22

    def collisionBubbleEffect(self):
        for i in Scene_BossStage.gObjList[6]:
            if ((Manager_Collision.collisionMiniIntersectRect(self, i))) and (i.isDamage == False):
                i.isDamage = True
                self.hp -= 1
                break

    def collisionBubble(self):
        for i in Scene_BossStage.gObjList[5]:
            if (Manager_Collision.collisionMiniIntersectRect(self, i)):
                i.birth = 3
                break