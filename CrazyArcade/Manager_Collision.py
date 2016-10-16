def collisionIntersectRect(_object1, _object2):
    # 레프트 탑 라이트 바텀
    object1_x1, object1_y1, object1_x2, object1_y2 = _object1.getCollisionBox()
    object2_x1, object2_y1, object2_x2, object2_y2 = _object2.getCollisionBox()
    object3_x1, object3_y1, object3_x2, object3_y2 = 0, 0, 0, 0

    if (object1_y1 <= object2_y2) and (object1_x2 >= object2_x1) \
        and (object1_x1 <= object2_x2) and (object1_y2 >= object2_y1):
        #top
        if object1_y1 > object2_y1:
            object3_y1 = object1_y1
        elif object1_y1 <= object2_y1:
            object3_y1 = object2_y1
        #botton
        if object1_y2 < object2_y2:
            object3_y2 = object1_y2
        elif object1_y2 >= object2_y2:
            object3_y2 = object2_y2
        #right
        if object1_x2 < object2_x2:
            object3_x2 = object1_x2
        elif object1_x2 >= object2_x2:
            object3_x2 = object2_x2
        #left
        if object1_x1 > object2_x1:
            object3_x1 = object1_x1
        elif object1_x1 <= object2_x1:
            object3_x1 = object2_x1
        return True, object3_x1, object3_y1, object3_x2, object3_y2
    return False, object3_x1, object3_y1, object3_x2, object3_y2

def collisionPtInRect(_object, _x, _y):
    if (_object.X - (int)(_object.sizeX / 2) <= _x) and (_object.X + (int)(_object.sizeX / 2) >= _x):
        if (_object.Y - (int)(_object.sizeY / 2) <= _y) and (_object.Y + (int)(_object.sizeY / 2) >= _y):
            return True
    return False

def collisionAABB(_mainObject, _subObject, _left, _top, _right, _bottom):
    if (_right - _left) > (_bottom - _top):
        if _mainObject.Y > _subObject.Y:
            _mainObject.Y += (_bottom - _top)
        else:
            _mainObject.Y -= (_bottom - _top)
    else:
        if _mainObject.X > _subObject.X:
            _mainObject.X += (_right - _left)
        else:
            _mainObject.X -= (_right - _left)