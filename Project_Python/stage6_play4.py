import pygame
import sys
import Ending

# 이미지 및 폰트 로딩
font_path = '../font/HBIOS-SYS.ttf'
font = pygame.font.Font(font_path, 30)

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


def gamePlay4(screen, show_endCheck, draw_text2, w, h, load_player=None):
    clock = pygame.time.Clock()
    bg = pygame.image.load('../img/복도.png')
    bg = pygame.transform.scale(bg, (w, h))

    # 출구 설정 (중앙 하단)
    exit_rect = pygame.Rect(w // 2 - 250, h - 150, 500, 150)

    # 초기 위치 (오른쪽 중앙)
    x, y = w - 200, h // 2
    frame = 0
    last_moving = 'down'

    running = True
    while running:
        screen.blit(bg, (0, 0))

        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()

        speed = 9 if mods & pygame.KMOD_SHIFT else 8
        frameCount = 3.6 if speed == 9 else 7.2
        move_x, move_y = 0, 0
        is_moving = False

        # 이동 처리 + 방향별 애니메이션
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
        else:
            # 멈춘 상태일 때 정지 이미지
            if last_moving == 'up':
                myImg = img_back
            elif last_moving == 'down':
                myImg = img_front
            elif last_moving == 'right':
                myImg = img_right
            elif last_moving == 'left':
                myImg = img_left

        # 이동 예정 위치 충돌 사각형
        crash_rect = pygame.Rect(x + move_x, y + move_y, myImg.get_width(), myImg.get_height())

        # 화면 경계 안으로 제한
        if 0 <= crash_rect.left <= w - myImg.get_width():
            x += move_x
        if 0 <= crash_rect.top <= h - myImg.get_height():
            y += move_y

        # 플레이어 출력
        screen.blit(myImg, (x, y))

        # 출구 충돌 시 엔딩 실행
        if crash_rect.colliderect(exit_rect):
            print("출구 도달 → 엔딩 실행")
            Ending.ending_cutscene(screen, show_endCheck)
            return

        pygame.display.update()
        frame = (frame + 1) % 8
        clock.tick(60)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
