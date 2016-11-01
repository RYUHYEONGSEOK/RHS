# coding: cp949
from pico2d import *
import math

import Scene_NormalStage
import Scene_BossStage

#기본 노드
class Node:
    def __init__(self, _index, _parent = None, _cost = 0):
        self.indexNumber = _index
        self.parent = _parent
        self.cost = _cost

    def equal(self, _node):
        if (self.indexNumber == _node.indexNumber):
            return True
        else:
            return False

#변수들
gStartIndex = 0
gGoalIndex = 0
#open, close, best List
gOpenList = [ Node(0) ]
gCloseList = [ Node(0) ]
gBestList = [ 0 ]

def AStarStart(_startX, _startY, _goalX, _goalY, _type):
    #같은지 체크
    tempStartIndex = GetTileIndex(_startX, _startY)
    tempGoalIndex = GetTileIndex(_goalX, _goalY)
    if (tempStartIndex == tempGoalIndex):
        return
    #거리체크
    distance = math.sqrt((_goalX - _startX) * (_goalX - _startX) + (_goalY - _startY) * (_goalY - _startY))
    if (distance > (40 * 10)):
        return
    #인덱스 지정
    global gStartIndex, gGoalIndex
    gStartIndex = tempStartIndex
    gGoalIndex = tempGoalIndex
    #도착장소의 옵션값 확인
    if _type == 0:
        if (Scene_NormalStage.gTileList[gGoalIndex].option == 1):
            gStartIndex, gGoalIndex = 0, 0
            return
    elif _type == 1:
        if (Scene_BossStage.gTileList[gGoalIndex].option == 1):
            gStartIndex, gGoalIndex = 0, 0
            return
    #초기화
    ClearList()
    #길생성
    MakeRoute(_type)

def MakeRoute(_type):
    global gStartIndex, gGoalIndex
    parentNode = Node(gStartIndex, None, 0)

    global gOpenList, gCloseList, gBestList
    gCloseList.append(parentNode)

    if _type == 0:
        #맵의 인덱스 + 옵션값0(지나감) + 오픈,클로즈리스트확인
        while(True):
            # X 13, Y 15
            #상
            tempIndex = parentNode.indexNumber - 13
            if (parentNode.indexNumber - 13 >= 0) and (Scene_NormalStage.gTileList[tempIndex].option != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)
            #하
            tempIndex = parentNode.indexNumber + 13
            if (parentNode.indexNumber + 13 < (13 * 15)) and (Scene_NormalStage.gTileList[tempIndex].option != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)
            #좌
            tempIndex = parentNode.indexNumber - 1
            if (parentNode.indexNumber % 13 != 0) and (Scene_NormalStage.gTileList[tempIndex].option != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)
            #우
            tempIndex = parentNode.indexNumber + 1
            if (parentNode.indexNumber % 13 != (13 - 1)) and (Scene_NormalStage.gTileList[tempIndex].option != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)

            gOpenList.sort()######걸리는 부분
            parentNode = gOpenList[0]

            gCloseList.append(parentNode)
            gOpenList.remove(gOpenList[0])

            parentNode = gCloseList[len(gCloseList) - 1]

            if parentNode.indexNumber == gGoalIndex:
                while (True):
                    gBestList.append(parentNode.indexNumber)
                    parentNode = parentNode.parent

                    if (parentNode.indexNumber == gStartIndex):
                        break

                gBestList.reverse()
                break
            
    elif _type == 1:
        #맵의 인덱스 + 옵션값0(지나감) + 오픈,클로즈리스트확인
        while(True):
            # X 13, Y 15
            #상
            tempIndex = parentNode.indexNumber - 13
            if (parentNode.indexNumber - 13 >= 0) and (Scene_BossStage.gTileList[tempIndex] != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)
            #하
            tempIndex = parentNode.indexNumber + 13
            if (parentNode.indexNumber + 13 < (13 * 15)) and (Scene_BossStage.gTileList[tempIndex] != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)
            #좌
            tempIndex = parentNode.indexNumber - 1
            if (parentNode.indexNumber % 13 != 0) and (Scene_BossStage.gTileList[tempIndex] != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)
            #우
            tempIndex = parentNode.indexNumber + 1
            if (parentNode.indexNumber % 13 != (13 - 1)) and (Scene_BossStage.gTileList[tempIndex] != 1) and (CheckList(tempIndex)):
                tempNode = MakeNode(tempIndex, parentNode)
                gOpenList.append(tempNode)

            gOpenList.sort()######걸리는 부분
            parentNode = gOpenList[0]

            gCloseList.append(parentNode)
            gOpenList.remove(parentNode)

            parentNode = gCloseList[len(gCloseList) - 1]

            if parentNode.indexNumber == gGoalIndex:
                while (True):
                    gBestList.append(parentNode.indexNumber)
                    parentNode = parentNode.parent

                    if (parentNode.indexNumber == gStartIndex):
                        break

                gBestList.reverse()
                break

def CheckList(_inputIndex):
    global gOpenList, gCloseList
    for i in gOpenList:
        if (i.indexNumber == _inputIndex):
            return False
    for i in gCloseList:
        if (i.indexNumber == _inputIndex):
            return False
    return True

def MakeNode(_type, _indexNumber, _parentNode = None):
    global gStartIndex, gGoalIndex

    tempNode = Node(_indexNumber, _parentNode)

    if _type == 0:
        startX, startY = Scene_NormalStage.gTileList[_indexNumber].X, Scene_NormalStage.gTileList[_indexNumber].Y
        goalX, goalY = Scene_NormalStage.gTileList[_parentNode.indexNumber].X, Scene_NormalStage.gTileList[_indexNumber.indexNumber].Y
        pCost = math.sqrt((goalX - startX) * (goalX - startX) + (goalY - startY) * (goalY - startY))
        
        goalX, goalY = Scene_NormalStage.gTileList[gGoalIndex].X, Scene_NormalStage.gTileList[gGoalIndex].Y
        fCost = math.sqrt((goalX - startX) * (goalX - startX) + (goalY - startY) * (goalY - startY))

        tempNode.cost = pCost + fCost
        return tempNode
    elif _type == 1:
        startX, startY = Scene_BossStage.gTileList[_indexNumber].X, Scene_BossStage.gTileList[_indexNumber].Y
        goalX, goalY = Scene_BossStage.gTileList[_parentNode.indexNumber].X, Scene_BossStage.gTileList[_indexNumber.indexNumber].Y
        pCost = math.sqrt((goalX - startX) * (goalX - startX) + (goalY - startY) * (goalY - startY))
        
        goalX, goalY = Scene_BossStage.gTileList[gGoalIndex].X, Scene_BossStage.gTileList[gGoalIndex].Y
        fCost = math.sqrt((goalX - startX) * (goalX - startX) + (goalY - startY) * (goalY - startY))

        tempNode.cost = pCost + fCost
        return tempNode

def GetTileIndex(_x, _y):
    indexX, indexY = (int)((_x - 20) / 40), (int)((560 - _y) / 40)
    return indexX + indexY * 13
    
def ClearList():
    global gStartIndex, gGoalIndex
    gStartIndex = 0
    gGoalIndex = 0

    global gOpenList, gCloseList, gBestList
    for i in gOpenList:
        gOpenList.remove(i)
    for i in gCloseList:
        gCloseList.remove(i)
    gBestList.clear()