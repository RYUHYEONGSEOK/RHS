# coding: cp949
from pico2d import *
import time

import Manager_Sound

import Scene_Logo
import Scene_Lobby

gRunning = None
gStack = None
gFrameTime = time.time()

def change_scene(_scene, _ambul = 0, _dart = 0, _pin = 0, _banana = 0):
    global gStack
    #�ٲٴ� ��쿡�� ������ �ִ°� ���ְ� ���ο� ���� ������� �ʱ�ȭ
    pop_scene()
    gStack.append(_scene)
    _scene.enter(_ambul, _dart, _pin, _banana)

def push_scene(_scene):
    global gStack
    #�����ϴ� ��� ���ߴ� ��
    if (len(gStack) > 0):
        gStack[-1].pause()
    #Ŭ���� �ְ� �ʱ�ȭ���� �ϴ� ����
    gStack.append(_scene)
    _scene.enter()

def pop_scene():
    global gStack
    #������ �����ϴ� �� ������ �Լ� + ����
    if (len(gStack) > 0):
        gStack[-1].exit()
        gStack.pop()
    #�׷��� �����ִ� ������ ����
    if (len(gStack) > 0):
        gStack[-1].resume()

def quit():
    global gRunning
    gRunning = False

def run(_scene):
    global gRunning, gStack
    #�������� Load
    Manager_Sound.LoadSoundData()
    #������ �ʱ�ȭ
    gRunning = True
    open_canvas(sync = True)
    gStack = [_scene]
    _scene.enter()

    #������ �����κ�
    while (gRunning):
        #frame 40���� ����
        global gFrameTime
        if gFrameTime + 0.025 < time.time() :
            gFrameTime = time.time()
            #Ű�Է� + update + draw
            gStack[-1].handle_events()
            gStack[-1].update()
            gStack[-1].draw()

    #������ ������ �Ǹ� ��� �� ����
    while (len(gStack) > 0):
        gStack[-1].exit()
        gStack.pop()
    close_canvas()
    #�������� Load
    Manager_Sound.ClearAllSound()