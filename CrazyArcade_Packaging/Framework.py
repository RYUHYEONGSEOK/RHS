# coding: cp949
from pico2d import *
#import os

import Manager_Sound

import Scene_Logo
import Scene_Lobby

gRunning = None
gStack = None
gCurrent_time = None

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
    global gRunning, gStack, gCurrent_time
    #frame_time
    gCurrent_time = get_time()
    #�������� Load
    Manager_Sound.LoadSoundData()
    #������ �ʱ�ȭ
    gRunning = True
    open_canvas()
    gStack = [_scene]
    _scene.enter()

    #������ �����κ�
    while (gRunning):
        #frame_time
        frame_time = get_time() - gCurrent_time
        gCurrent_time += frame_time
        #Ű�Է� + update + draw
        gStack[-1].handle_events()
        gStack[-1].update(frame_time)
        gStack[-1].draw()

    #������ ������ �Ǹ� ��� �� ����
    while (len(gStack) > 0):
        gStack[-1].exit()
        gStack.pop()
    close_canvas()