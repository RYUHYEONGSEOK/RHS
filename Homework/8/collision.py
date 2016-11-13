from pico2d import *

import game_framework


from boy import Boy # import Boy class from boy.py
from ball import Ball, BigBall
from grass import Grass
from brick import Brick



name = "collision"

boy = None
balls = None
big_balls = None
grass = None
brick = None

def create_world():
    global boy, grass, balls, big_balls, brick

    boy = Boy()
    balls = [Ball() for i in range(10)]
    big_balls = [BigBall() for i in range(10)]
    balls = big_balls + balls
    grass = Grass()
    brick = Brick()


def destroy_world():
    global boy, grass, balls, big_balls, brick

    del(boy)
    del(balls)
    del(grass)
    del(big_balls)
    del(brick)


def enter():
    open_canvas()
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                boy.handle_event(event)



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collideAABB(a, b):
    object1_x1, object1_y1, object1_x2, object1_y2 = a.get_bb()
    object2_x1, object2_y1, object2_x2, object2_y2 = b.get_bb()
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


def update(frame_time):
    global boy, brick
    #moving
    boy.update(frame_time)
    brick.update(frame_time)
    if boy.isBrickCollision == True:
        if brick.isLeftMoving:
            boy.x -= brick.moving_speed * frame_time
        else:
            boy.x += brick.moving_speed * frame_time

    for ball in balls:
        ball.update(frame_time)
        if ball.isBrickCollision == True:
            if brick.isLeftMoving:
                ball.x -= brick.moving_speed * frame_time
            else:
                ball.x += brick.moving_speed * frame_time

    #ball vs grass collision
    for ball in balls:
        if collide(grass, ball):
            ball.stop()

    #boy vs grass collision
    if collide(boy, grass):
        boy.stop()
        boy.y = 100
    else:
        boy.fall_speed = 100

    #ball vs boy collision
    for ball in balls:
        if collide(boy, ball):
            balls.remove(ball)

    #ball vs brick collision
    for ball in balls:
        isCollision, left, top, right, bottom = collideAABB(ball, brick)
        if isCollision == True:
            width = right - left
            length = bottom - top
            if width > length:
                if ball.y > brick.y:
                    ball.isBrickCollision = True
                    ball.stop()
            
    #boy vs brick collision
    isCollision, left, top, right, bottom = collideAABB(boy, brick)
    if isCollision == True:
        boy.isBrickCollision = True
        width = right - left
        length = bottom - top
        #top, bottom
        if width > length:
            #top
            if boy.y > brick.y:
                boy.stop()
                boy.isJump = False
            #bottom
            else:
                boy.isJump = False
        #right,left
        else:
            #left
            if boy.x > brick.x:
                boy.x += width
            #right
            else:
                boy.x -= width
    elif isCollision == False:
        boy.isBrickCollision = False
        boy.fall_speed = 100




def draw(frame_time):
    clear_canvas()

    grass.draw()
    grass.draw_bb()

    boy.draw()
    boy.draw_bb()

    brick.draw()
    brick.draw_bb()

    for ball in balls:
        ball.draw()
        ball.draw_bb()


    update_canvas()