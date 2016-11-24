# coding: cp949
from pico2d import *
import time

import Scene_NormalStage
import Scene_BossStage

import Manager_Collision
import Manager_Sound

import Object
import Object_Bubble
import Object_Item

class Player(Object.GameObject):
    def __init__(self, _x, _y, _type, _ambul = 0, _dart = 0, _pin = 0, _banana = 0):
        #�÷��̾� ��ġ �� �̹����� �浹 üũ�� ������
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY = 38, 38
        self.image_size = 70
        #�÷��̾��� �Ӽ�
        self.type = _type #�븻��0, ������1
        self.dir = None
        self.speed, self.power, self.bubbleCount = 3, 1, 1
        self.isBushCheck, self.isSlidingPlayer = False, False
        self.birth, self.birthCount = None, 0
        #�̹���(BIRTH STAND WALK BUBBLE BUBBLE_WALK DEAD)
        self.player_image = None
        self.player_state = 'STATE_BIRTH'
        self.frame, self.frameMax, self.frameScene, self.frameTime = None, None, None, 0
        #������ ��������
        self.bananaCount = _banana
        self.dartCount = _dart
        self.pinCount = _pin
        self.ambulanceCount = _ambul

    def __del__(self):
        self.exit()

    def enter(self):
        # �̹��� ���뵵�� ����
        self.player_image = load_image('..\\Sprite\\03.InGame\\Character\\Character_Player.png')
        self.player_state = 'STATE_BIRTH'
        self.frame = 0
        self.frameMax = 4
        self.frameScene = 5
        self.dir = 1 #0��,1�Ʒ�,2������,3����
        self.birth = 0 #0��,1��ǳ������,2�״°���,3����
        self.frameTime = time.time()

    def exit(self):
        del (self.player_image)

    def update(self, _frametime, _events):
        if self.birth < 3:
            #��Ÿ�� �Լ� �߰�
            self.itemMaxCheck()

            #�ٳ��������� �ٳ������� üũ�ϰ� else�� keycheck
            if self.isSlidingPlayer:
                if self.dir == 0:
                    self.Y += 6 * _frametime * 50
                elif self.dir == 1:
                    self.Y -= 6 * _frametime * 50
                elif self.dir == 2:
                    self.X += 6 * _frametime * 50
                elif self.dir == 3:
                    self.X -= 6 * _frametime * 50
            else:
                self.keycheck(_events)

            #�浹üũ(�����Ÿ�� + ��)
            self.collisionSpecialTile()
            self.collisionWall()
            #������¿� ���� �ִϸ��̼� �κ�
            self.frame_move(_frametime, self.player_state)

        # �÷��̾� ����
        elif self.birth == 3:
            return False

    def draw(self):
        if self.isBushCheck == True:
            pass
        #�������� �����ϴ� �׸������� X��ǥ, Y��ǥ(Y��ǥ�� �Ʒ������� 1) => ���� �Ʒ����� ������ ������ �ϳ��� �׸�
        else:
            self.player_image.clip_draw((self.frame * self.image_size), 560 - ((self.frameScene + 1) * self.image_size),
                                        self.image_size, self.image_size,
                                        self.X, self.Y + 13)#�������� �÷��̾� ��ġ ������

    def keycheck(self, _events):
        for event in _events:
            if event.type == SDL_KEYDOWN:
                #����Ű
                if event.key == SDLK_UP:
                    if self.birth == 0:
                        self.dir = 0
                        self.frame, self.frameMax = 0, 4
                        self.player_state = 'STATE_WALK'
                    elif self.birth == 1:
                        self.dir = 0
                        self.player_state = 'STATE_BUBBLE_WALK'
                elif event.key == SDLK_DOWN:
                    if self.birth == 0:
                        self.dir = 1
                        self.frame, self.frameMax = 0, 4
                        self.player_state = 'STATE_WALK'
                    elif self.birth == 1:
                        self.dir = 1
                        self.player_state = 'STATE_BUBBLE_WALK'
                if event.key == SDLK_RIGHT:
                    if self.birth == 0:
                        self.dir = 2
                        self.frame, self.frameMax = 0, 3
                        self.player_state = 'STATE_WALK'
                    elif self.birth == 1:
                        self.dir = 2
                        self.player_state = 'STATE_BUBBLE_WALK'
                elif event.key == SDLK_LEFT:
                    if self.birth == 0:
                        self.dir = 3
                        self.frame, self.frameMax = 0, 3
                        self.player_state = 'STATE_WALK'
                    elif self.birth == 1:
                        self.dir = 3
                        self.player_state = 'STATE_BUBBLE_WALK'
                #��ǳ��
                if event.key == SDLK_SPACE:
                    #�� ���� ������Ʈ �Ŵ����� �ֱ�
                    if (self.type == 0) and (self.birth == 0):
                        if (len(Scene_NormalStage.gObjList[5]) < self.bubbleCount):
                            indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
                            posX, posY = 40 + (indexX * 40), (600 - 60) - (40 * indexY)
                            isCheck = False
                            for i in Scene_NormalStage.gObjList[5]:
                                if (Manager_Collision.collisionMiniIntersectRect(i, self)):
                                    isCheck = True
                                    break
                            if isCheck == False:
                                tempBubble = Object_Bubble.Bubble(posX, posY, self.type, self.power)
                                tempBubble.enter()
                                Scene_NormalStage.gObjList[5].append(tempBubble)
                    elif (self.type == 1) and (self.birth == 0):
                        if (len(Scene_BossStage.gObjList[5]) < self.bubbleCount):
                            indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
                            posX, posY = 40 + (indexX * 40), (600 - 60) - (40 * indexY)
                            isCheck = False
                            for i in Scene_BossStage.gObjList[5]:
                                if (Manager_Collision.collisionMiniIntersectRect(i, self)):
                                    isCheck = True
                                    break
                            if isCheck == False:
                                tempBubble = Object_Bubble.Bubble(posX, posY, self.type, self.power)
                                tempBubble.enter()
                                Scene_BossStage.gObjList[5].append(tempBubble)
                #�����ۻ��
                if event.key == SDLK_q:
                    if (self.ambulanceCount > 0) and (self.birth == 1):
                        self.ambulanceCount -= 1
                        self.birth = 0
                        self.birthCount = 0
                        self.player_state = 'STATE_BIRTH'
                        self.frameScene = 5
                        self.frame = 0
                        Manager_Sound.PlayEffectSound('CHAR_REVIVAL')
                        
                if event.key == SDLK_w:
                    if (self.dartCount > 0) and (self.birth == 0):
                        self.dartCount -= 1
                    else: return
                    #��Ʈ����
                    indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
                    posX, posY = 40 + (indexX * 40), (600 - 60) - (40 * indexY)
                    tempDart = Object_Item.Item(posX, posY, self.type, 8, self.dir)
                    tempDart.enter()
                    Manager_Sound.PlayEffectSound('ITEM_DART')
                    if self.type == 0:
                        Scene_NormalStage.gObjList[4].append(tempDart)
                    elif self.type == 1:
                        Scene_BossStage.gObjList[4].append(tempDart)
                if event.key == SDLK_e:
                    if (self.pinCount > 0) and (self.birth == 0):
                        self.pinCount -= 1
                if event.key == SDLK_r:
                    if (self.bananaCount > 0) and (self.birth == 0):
                        self.bananaCount -= 1
                    else: return
                    #�ٳ�������
                    indexX, indexY = (int)((self.X - 20) / 40), (int)((560 - self.Y) / 40)
                    posX, posY = 40 + (indexX * 40), (600 - 60) - (40 * indexY)
                    tempBanana = Object_Item.Item(posX, posY, self.type, 7, self.dir)
                    tempBanana.enter()
                    Manager_Sound.PlayEffectSound('ITEM_ON')
                    if self.type == 0:
                        Scene_NormalStage.gObjList[4].append(tempBanana)
                    elif self.type == 1:
                        Scene_BossStage.gObjList[4].append(tempBanana)
                #ġƮŰ(��� ������ �ִ� + �Ӽ� �ִ�)
                if event.key == SDLK_RETURN:
                    if self.birth == 0:
                        self.speed, self.bubbleCount, self.power = 5, 5, 5
                        self.bananaCount, self.ambulanceCount, self.pinCount, self.dartCount = 9, 9, 9, 9
                        self.birth = 1
                        self.frame = 0
                        self.player_state = 'STATE_BUBBLE'
                        Manager_Sound.PlayEffectSound('CHAR_FIXED')
            elif event.type == SDL_KEYUP:
                #����Ű���� ���� ���� ���
                if self.player_state == 'STATE_WALK':
                    if (event.key == SDLK_UP and self.dir == 0) or (event.key == SDLK_DOWN and self.dir == 1) \
                        or (event.key == SDLK_RIGHT and self.dir == 2) or (event.key == SDLK_LEFT and self.dir == 3):
                        self.player_state = 'STATE_STAND'
                elif self.player_state == 'STATE_BUBBLE_WALK':
                    if (event.key == SDLK_UP and self.dir == 0) or (event.key == SDLK_DOWN and self.dir == 1) \
                        or (event.key == SDLK_RIGHT and self.dir == 2) or (event.key == SDLK_LEFT and self.dir == 3):
                        self.player_state = 'STATE_BUBBLE'

    def frame_move(self, _frametime, _player_state):
        #ó�� �¾ ��� �¾�� �ִϸ��̼� ����
        if ((self.player_state == 'STATE_BIRTH') and (self.frameTime + 1 < time.time())):
            self.frameTime = time.time()
            _player_state = 'STATE_STAND'
        elif (self.player_state != _player_state):
            self.frame = 0
            self.player_state = _player_state

        #���°� ��ȭ
        if self.player_state == 'STATE_BIRTH':
            if self.frameTime + 0.25 < time.time():
                self.frameTime = time.time()
                self.frame += 1
                if self.frame > self.frameMax:
                    self.frame = 0
                    self.player_state = 'STATE_STAND'
                    self.frameScene = self.dir

        elif self.player_state == 'STATE_STAND':
            self.frame = 0
            self.frameScene = self.dir

        elif self.player_state == 'STATE_WALK':
            if self.frameScene != self.dir:
                self.frameScene = self.dir

            if self.frameTime + 0.2 < time.time():
                self.frameTime = time.time()
                self.frame += 1
                if self.frame > self.frameMax:
                    self.frame = 0
            #������ �߰�
            if self.dir == 0:
                self.Y += self.speed * _frametime * 50
            elif self.dir == 1:
                self.Y -= self.speed * _frametime * 50
            elif self.dir == 2:
                self.X += self.speed * _frametime * 50
            elif self.dir == 3:
                self.X -= self.speed * _frametime * 50

        elif self.player_state == 'STATE_BUBBLE':
            if self.frameScene != 4:
                self.frameScene = 4

            if self.frameMax != 3:
                self.frameMax = 3

            if self.frameTime + 0.5 < time.time():
                self.frameTime = time.time()
                self.frame += 1
                if self.frame > self.frameMax:
                    self.frame = 0
                    self.birthCount += 1
                    if self.birthCount != 3:
                        Manager_Sound.PlayEffectSound('CHAR_FIXED')
                    if self.birthCount > 2:
                        self.birthCount = 0
                        self.birth = 2
                        self.player_state = 'STATE_DEAD'
                        self.frameScene = 6
                        self.frameMax = 6
                        Manager_Sound.PlayEffectSound('CHAR_DIE')

        elif self.player_state == 'STATE_BUBBLE_WALK':
            if self.frameScene != 4:
                self.frameScene = 4

            if self.frameTime + 0.5 < time.time():
                
                self.frameTime = time.time()
                self.frame += 1
                if self.frame > self.frameMax:
                    self.frame = 0
                    self.birthCount += 1
                    if self.birthCount != 3:
                        Manager_Sound.PlayEffectSound('CHAR_FIXED')
                    if self.birthCount > 2:
                        self.birthCount = 0
                        self.birth = 2
                        self.player_state = 'STATE_DEAD'
                        self.frameScene = 6
                        self.frameMax = 6
                        Manager_Sound.PlayEffectSound('CHAR_DIE')
            #������ �߰�
            if self.dir == 0:
                self.Y += 1 * _frametime * 50
            elif self.dir == 1:
                self.Y -= 1 * _frametime * 50
            elif self.dir == 2:
                self.X += 1 * _frametime * 50
            elif self.dir == 3:
                self.X -= 1 * _frametime * 50

        elif self.player_state == 'STATE_DEAD':
            if self.frameScene != 6:
                self.frameScene = 6

            if self.frameTime + 0.2 < time.time():
                self.frameTime = time.time()
                self.frame += 1
                if self.frame > self.frameMax:
                    self.birth = 3

    def itemMaxCheck(self):
        if self.speed > 6:
            self.speed = 6
        if self.bubbleCount > 4:
            self.bubbleCount = 4
        if self.power > 4:
            self.power = 4

    def collisionWall(self):
        if self.X < 40:
            self.X = 40
            self.isSlidingPlayer = False
            return
        elif self.X > 600:
            self.X = 600
            self.isSlidingPlayer = False
            return
        if self.Y < 60:
            self.Y = 60
            self.isSlidingPlayer = False
            return
        elif self.Y > 540:
            self.Y = 540
            self.isSlidingPlayer = False
            return

    def collisionSpecialTile(self):
        self.isBushCheck = False
        if self.type == 0:
            for i in Scene_NormalStage.gObjList[3]:
                if i.breakingOption == 2:
                    i.isPlayerCollision = False
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(self, i)
                if (isCollision == True) and (i.breakingOption != 2):
                    Manager_Collision.collisionAABB(self, i, left, top, right, bottom)
                    self.isSlidingPlayer = False
                elif (isCollision == True) and (i.breakingOption == 2):
                    self.isBushCheck = True
                    i.isPlayerCollision = True
        elif self.type == 1:
            for i in Scene_BossStage.gObjList[3]:
                isCollision, left, top, right, bottom = Manager_Collision.collisionIntersectRect(self, i)
                if (isCollision == True) and (i.breakingOption != 2):
                    Manager_Collision.collisionAABB(self, i, left, top, right, bottom)
                    self.isSlidingPlayer = False