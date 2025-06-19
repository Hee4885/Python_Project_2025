import pygame
import math
import following_player

# 폰트
font_path = "../font/HBIOS-SYS.ttf"
font = pygame.font.Font(font_path, 60)

# 염소악마 설정
ghost_img = pygame.image.load("../img/염소1.png")
ghost_x, ghost_y = 0, 670
ghost_speed = 2
ghost_active = False
escape_triggered = False

# 걷는 애니메이션 이미지
ghost_right_imgs = [
    pygame.image.load("../img/염소1.png"),
    pygame.image.load("../img/염소2.png")
]
ghost_left_imgs = [
    pygame.image.load("../img/염소3.png"),
    pygame.image.load("../img/염소4.png")
]

ghost_img_index = 0
ghost_img_timer = 0
ghost_direction = "right"

# 아이템 이미지
paper = pygame.image.load("../img/종이.png")
hint = pygame.image.load("../img/힌트.png")
show_hint = False
hint_start_time = 0

pW, pH = paper.get_width(), paper.get_height()
paper_x, paper_y = 785, 650
pRect = pygame.Rect(paper_x, paper_y, pW, pH)

getKey = False
pGet = False

def update_ghost(player_x, player_y):
    global ghost_x, ghost_y, ghost_direction, ghost_img_index, ghost_img_timer

    #플레이어와 유령 간의 x, y 거리 차이
    dx = player_x - ghost_x
    dy = player_y - ghost_y
    ghost_direction = "right" if dx >= 0 else "left"

    distance = math.hypot(dx, dy)
    if distance != 0:
        ghost_x += ghost_speed * dx / distance
        ghost_y += ghost_speed * dy / distance

    ghost_img_timer += 1
    if ghost_img_timer > 12:
        ghost_img_index = (ghost_img_index + 1) % 2
        ghost_img_timer = 0

def draw_ghost(screen):
    img = ghost_right_imgs if ghost_direction == "right" else ghost_left_imgs
    screen.blit(img[ghost_img_index], (ghost_x, ghost_y))

def GAME_OVER(text, screen):
    screen.fill((0, 0, 0))
    label = font.render(text, True, (155, 17, 30))
    rect = label.get_rect(center=(775, 520))
    screen.blit(label, rect)

def draw_paper(screen, w, h, player_rect):
    global pGet, show_hint, hint_start_time, pRect
    if not pGet:
        screen.blit(paper, (paper_x, paper_y))
    if not pGet and pRect and player_rect.colliderect(pRect):
        pGet = True
        show_hint = True
        pRect = None
        hint_start_time = pygame.time.get_ticks()

def get_obj_rect2(w):
    global ghost_active
    obj = [
        pygame.Rect(0, 0, w, 500),        # 위
        pygame.Rect(0, 850, w, 400),      # 아래
        pygame.Rect(w//2 + 250, 520, 300, 100),  # 사물함1
        pygame.Rect(w//2 + 550, 520, 100, 100)   # 사물함2
    ]
    return obj

def obj_rect2(screen, w, get_obj_rect2, x, y, move_x, move_y, myImg, show_endCheck, draw_text2, h, load_player):
    global getKey, ghost_active
    crash_rect = pygame.Rect(x + move_x, y + move_y, myImg.get_width(), myImg.get_height())
    wall = get_obj_rect2(w)
    blocked = False

    for rect in wall:
        pygame.draw.rect(screen, (0, 0, 0), rect)
        if crash_rect.colliderect(rect):
            blocked = True

    locker_None, locker_key = wall[2], wall[3]

    if crash_rect.colliderect(locker_None):
        draw_text2("[사물함이 비어있음]")
        return True
    if crash_rect.colliderect(locker_key):
        draw_text2("[열쇠를 얻었다!]")
        getKey = True
        ghost_active = True
        return True

    return blocked

def gamePlay3(screen, show_endCheck, draw_text2, w, h, load_player, x=900, y=400):
    global show_hint, getKey, ghost_active

    screen.fill((0, 0, 0))
    corridor_img = pygame.image.load('../img/복도2.png')
    corridor_img = pygame.transform.scale(corridor_img, (w, h // 2))

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_endCheck(screen)

        keyPress = pygame.key.get_pressed()
        x, y, myImg, move_x, move_y = following_player.following_players(
            keyPress, screen, w, h, show_endCheck, x, y
        )

        blocked = obj_rect2(screen, w, get_obj_rect2, x, y, move_x, move_y, myImg,
                            show_endCheck, draw_text2, h, load_player)
        if not blocked:
            x += move_x
            y += move_y

        player_rect = pygame.Rect(x, y, myImg.get_width(), myImg.get_height())
        screen.blit(corridor_img, (0, h // 2 - 200))
        draw_paper(screen, w, h, player_rect)

        if ghost_active:
            update_ghost(x, y)
            draw_ghost(screen)

        screen.blit(myImg, (x, y))

        # 탈출 통로 충돌 감지
        escape_rect = pygame.Rect(0, 400, 200, 400)
        pygame.draw.rect(screen, (100, 0, 0), escape_rect, 2)  # 디버깅용 시각화

        if player_rect.colliderect(escape_rect):
            print("탈출 경로 충돌 감지")
            if getKey:
                print("열쇠 있음 → 탈출 성공")
                import stage6_play4
                stage6_play4.gamePlay4(screen, show_endCheck, draw_text2, w, h, load_player)
                return
            else:
                draw_text2("문이 잠겨 있다... 열쇠가 필요하다!")


        if ghost_active:
            ghost_rect = pygame.Rect(
                ghost_x + ghost_img.get_width() * 0.3,
                ghost_y + ghost_img.get_height() * 0.3,
                ghost_img.get_width() * 0.4,
                ghost_img.get_height() * 0.4
            )
            if ghost_rect.colliderect(player_rect):
                GAME_OVER("GAME OVER", screen)
                pygame.display.flip()
                pygame.time.delay(2000)
                show_endCheck(screen)

        if show_hint:
            now = pygame.time.get_ticks()
            if now - hint_start_time < 2000:
                x_hint = (w // 2) - (hint.get_width() // 2)
                y_hint = (h // 2) - (hint.get_height() // 2)
                screen.blit(hint, (x_hint, y_hint))
        else:
            show_hint = False

        pygame.display.flip()
        clock.tick(60)