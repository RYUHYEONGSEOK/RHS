# coding: cp949
class GameObject:
    def __init__(self, _x = 0, _y = 0):
        self.X, self.Y = _x, _y
        self.sizeX, self.sizeY

    def getCollisionBox(self):
        #���� �Ʒ���ǥ + ������ ����ǥ
        return self.X - (self.sizeX / 2), self.Y - (self.sizeY / 2), self.X + (self.sizeX / 2), self.Y + (self.sizeY / 2)