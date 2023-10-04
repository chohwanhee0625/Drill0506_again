from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024


def load_resources():
    global TUK_ground, character
    global arrow
    TUK_ground = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')
    arrow = load_image('hand_arrow.png')


def handle_events():
    global running
    global mx, my

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, TUK_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
            points.append((event.x, TUK_HEIGHT - 1 - event.y))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass


def reset_world():
    global running
    global cx, cy, mx, my
    global action
    global frame
    global points

    running = True
    cx, cy = TUK_WIDTH // 2, TUK_HEIGHT // 2
    frame = 0
    action = 3
    mx, my = cx, cy
    points = [ ]

    set_new_target_arrow()


def set_new_target_arrow():
    global sx, sy, hx, hy
    global action
    global t
    global target_exists
    
    if points:                  # points 리스트 안에 남아있는 점이 있으면
        sx, sy = cx, cy         # p1 : 시작점
        # hx, hy = 100, 100
        hx, hy = points[0]      # p2 : 끝점
        t = 0.0
        action = 1 if sx < hx else 0
        target_exists = True
    else:
        action = 3 if action == 1 else 2    # 이전 캐릭터의 움직임 방향에 따른 idle 동작 결정
        target_exists = False


def render_world():
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    arrow.draw(mx, my)
    for p in points:
        arrow.draw(p[0], p[1])
    character.clip_draw(frame * 100, 100 * action, 100, 100, cx, cy)
    update_canvas()


def update_world():
    global frame, t
    global cx, cy

    frame = (frame + 1) % 8

    if target_exists:
        if t <= 1.0:
            cx = (1 - t) * sx + t * hx  # 시작점과 끝점을 1-t:t 의 비율로 섞은 위치
            cy = (1 - t) * sy + t * hy
            t += 0.002
        else:                           # 목표 지점에 도달하면
            cx, cy = hx, hy             # 캐릭터 위치를 목적지 위치와 정확히 일치시킴
            del points[0]               # 목표지점에 도착했기 때문에 더 이상 필요 없는 점 삭제
            set_new_target_arrow()


open_canvas(TUK_WIDTH, TUK_HEIGHT)
hide_cursor()
load_resources()
reset_world()

while running:
    render_world()

    handle_events()
    update_world()

close_canvas()
