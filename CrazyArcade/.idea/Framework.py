from pico2d import *

import Scene_Logo
import Scene_Lobby

gRunning = None
gStack = None

def change_scene(_scene):
    global gStack
    #바꾸는 경우에는 기존에 있는것 없애고 새로운 씬은 집어놓고 초기화
    pop_scene()
    gStack.append(_scene)
    _scene.enter()

def push_scene(_scene):
    global gStack
    #존재하는 경우 멈추는 것
    if (len(gStack) > 0):
        gStack[-1].pause()
    #클래스 넣고 초기화까지 하는 과정
    gStack.append(_scene)
    _scene.enter()

def pop_scene():
    global gStack
    #기존에 존재하는 씬 나가는 함수 + 제거
    if (len(gStack) > 0):
        gStack[-1].exit()
        gStack.pop()
    #그래도 남아있는 스택은 실행
    if (len(gStack) > 0):
        gStack[-1].resume()

def quit():
    global gRunning
    gRunning = False

def run(_scene):
    global gRunning, gStack
    #메인의 초기화
    gRunning = True
    open_canvas()
    gStack = [_scene]
    _scene.enter()

    #게임의 구동부분
    while (gRunning):
        gStack[-1].handle_events()
        gStack[-1].update()
        gStack[-1].draw()

    #게임이 끝나게 되면 모든 데이터 삭제
    while (len(gStack) > 0):
        gStack[-1].exit()
        gStack.pop()

    close_canvas()