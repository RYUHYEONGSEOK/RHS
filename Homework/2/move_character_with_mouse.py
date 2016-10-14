from pico2d import *
import math

def handle_events():
    global running
    global x, y
    global halflength
    global angle

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                halflength += 10
            elif event.key == SDLK_d:
                halflength -= 10
            elif event.key == SDLK_UP:
                y += 10
            elif event.key == SDLK_DOWN:
                y -= 10
            elif event.key == SDLK_RIGHT:
                x += 10
            elif event.key == SDLK_LEFT:
                x -= 10
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, 600 - event.y

    if halflength > 300:
        halflength = 300
    elif halflength < 20:
        halflength = 20


open_canvas()
character = load_image('run_animation.png')

running = True
x, y = 400, 300
angle = 0
halflength = 100

while (running):
    clear_canvas()
    angle += 0.02
    character.clip_draw(100, 0, 100, 100, x + halflength * math.cos(angle), y + halflength * math.sin(angle))
    update_canvas()

    delay(0.05)
    handle_events()

close_canvas()