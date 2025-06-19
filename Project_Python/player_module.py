import pygame

pygame.init()

bg_img = pygame.image.load("../img/교실1.png")

#폰트
font_path = '../font/HBIOS-SYS.ttf'
font = pygame.font.Font(font_path, 30)
font2 = pygame.font.Font(font_path, 20)

# 플레이어 이미지 로드
img_front = pygame.image.load('../img/앞.png')
img_front_walk1 = pygame.image.load('../img/앞_걷기1.png')
img_front_walk2 = pygame.image.load('../img/앞_걷기2.png')

img_back = pygame.image.load('../img/뒤.png')
img_back_walk1 = pygame.image.load('../img/뒤_걷기1.png')
img_back_walk2 = pygame.image.load('../img/뒤_걷기2.png')

img_left = pygame.image.load('../img/왼쪽.png')
img_left_walk1 = pygame.image.load('../img/왼쪽_걷기1.png')
img_left_walk2 = pygame.image.load('../img/왼쪽_걷기2.png')

img_right = pygame.image.load('../img/오른쪽.png')
img_right_walk1 = pygame.image.load('../img/오른쪽_걷기1.png')
img_right_walk2 = pygame.image.load('../img/오른쪽_걷기2.png')

# 아이템 이미지
img_flash = pygame.image.load('../img/손전등.png')

# 아이템 충돌 유무
item_crash = False

# 플레이어 동작 프레임
frame = 0
frameCount = 0

# 플레이어
x, y = 700, 400
last_moving = ''
myImg = pygame.image.load('../img/앞.png')
player_rect = img_front.get_rect()
player_rect.topleft = (x, y)
crash_rect = pygame.Rect(x, y, 10, 10)

iImg = pygame.image.load('../img/손전등.png')

def draw_item(screen, ix=800, iy=600):
    global item_crash
    if item_crash:
        return None
    i_rect = pygame.Rect(ix, iy, iImg.get_width() // 5, iImg.get_height() // 5)
    screen.blit(iImg, (ix, iy))
    return i_rect

def load_player(item_use, keyPress, screen, get_object_rect, w, h, draw_text2, show_endCheck, show_dialog, friend_obj):
    global x, y, frame, frameCount, myImg, player_rect, last_moving, crash_rect, item_crash

    player_img = pygame.image.load("../img/앞.png")
    player_rect = player_img.get_rect(topleft=(x, y))


    speed = 0
    keys = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    is_moving = False
    mods = pygame.key.get_mods()

    if mods & pygame.KMOD_SHIFT:
        print("Shift 누르림!")
        speed = 12
        frameCount = 3.6
    else:
        print("Shift 안 누르림!")
        speed = 9
        frameCount = 7.2

    if keys[pygame.K_w]:
        move_y = -speed
        myImg = img_back_walk1 if frame < frameCount else img_back_walk2
        last_moving = 'up'
        is_moving = True
    elif keys[pygame.K_s]:
        move_y = speed
        myImg = img_front_walk1 if frame < frameCount else img_front_walk2
        last_moving = 'down'
        is_moving = True
    elif keys[pygame.K_a]:
        move_x = -speed
        myImg = img_left_walk1 if frame < frameCount else img_left_walk2
        last_moving = 'left'
        is_moving = True
    elif keys[pygame.K_d]:
        move_x = speed
        myImg = img_right_walk1 if frame < frameCount else img_right_walk2
        last_moving = 'right'
        is_moving = True

    if not is_moving:
        if last_moving == 'up':
            myImg = img_back
        elif last_moving == 'down':
            myImg = img_front
        elif last_moving == 'right':
            myImg = img_right
        elif last_moving == 'left':
            myImg = img_left

    crash_rect = pygame.Rect(x + move_x, y + move_y, myImg.get_width(), myImg.get_height())
    x = max(0, min(x, w - myImg.get_width()))
    y = max(0, min(y, h - myImg.get_height()))

    f_rect = pygame.Rect(0, 0, 0, 0)
    if friend_obj:
        try:
            f_rect = friend_obj(screen)
        except Exception as e:
            print(f"friend_obj error: {e}")
            f_rect = pygame.Rect(0, 0, 0, 0)

    obstacles = get_object_rect(w)
    door1 = obstacles[-2]
    door2 = obstacles[-1]
    i_rect = draw_item(screen)

    blocked = False
    for obj in get_object_rect(w):
        if crash_rect.colliderect(obj):
            blocked = True
            print("장애물과 충돌")
            break

    if crash_rect.colliderect(f_rect):
        blocked = True
        print("친구와 충돌")
        show_dialog("f", w, h, screen, draw_text2)

    if i_rect and crash_rect.colliderect(i_rect):
        blocked = True
        print("손전등과 충돌")
        item_crash = True

    if crash_rect.colliderect(door1):
        if not item_crash or not item_use:
            door_lock_text = font2.render("앞이 잘 안 보여 열 수 없다..", True, (255, 255, 255))
            text_rect = door_lock_text.get_rect(midbottom=(crash_rect.centerx, crash_rect.top - 25))
            screen.blit(door_lock_text, text_rect)
        else:
            import stage4_play2
            stage4_play2.gamePlay2(screen, show_endCheck, draw_text2, w, h, load_player, x=100, y=500)

    if crash_rect.colliderect(door2):
        door_lock_text = font2.render("문이 잠겨 있다..", True, (255, 255, 255))
        text_rect = door_lock_text.get_rect(midbottom=(crash_rect.centerx, crash_rect.top - 25))
        screen.blit(door_lock_text, text_rect)

    if not blocked:
        x += move_x
        y += move_y

    frame += 1
    if frame >= frameCount * 2:
        frame = 0

    screen.blit(myImg, (x, y))

    return x, y, myImg, move_x, move_y
