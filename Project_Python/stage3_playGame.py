

import pygame
import sys

# 초기화
pygame.init()  # 파이 게임 초기화
pygame.mixer.init()  # 사운드 시스템 초기화

# 배경음악 설정
pygame.mixer.music.load('../music/달리기.mp3')
pygame.mixer.music.play()

# 이미지 미리 로드

# 배경요소
img_class = pygame.image.load('../img/교실1.jpg')

# 캐릭터
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


def draw_background(screen, w, h):
    scaled_img2 = pygame.transform.scale(img_class, (w, h))

    screen.fill((0, 0, 0))
    screen.blit(scaled_img2, (0, 0))

    # 화면 크기에 맞게 비율 계산
    scale_x = w / 1366  # 원본 이미지 가로 크기 기준
    scale_y = h / 768  # 원본 이미지 세로 크기 기준

    # 책상 크기 (더 작게)
    desk_width = int(50 * scale_x)
    desk_height = int(40 * scale_y)

    # 교탁 크기 (더 작게)
    podium_width = int(120 * scale_x)
    podium_height = int(50 * scale_y)

    # TV 크기 (더 작게)
    tv_width = int(80 * scale_x)
    tv_height = int(50 * scale_y)

    # 각 책상의 개별 위치 (더 오른쪽으로 이동하고 위로 올림)
    desks = [
        # 맨 위줄 (첫 번째 행) - 오른쪽으로 50px, 위로 30px 이동
        (int(260 * scale_x), int(240 * scale_y)),  # 책상 1 (왼쪽 첫 번째)
        (int(390 * scale_x), int(240 * scale_y)),  # 책상 2 (왼쪽 두 번째)
        (int(760 * scale_x), int(240 * scale_y)),  # 책상 3 (오른쪽 첫 번째)
        (int(890 * scale_x), int(240 * scale_y)),  # 책상 4 (오른쪽 두 번째)

        # 두 번째 행 - 오른쪽으로 50px, 위로 30px 이동
        (int(260 * scale_x), int(350 * scale_y)),  # 책상 5
        (int(390 * scale_x), int(350 * scale_y)),  # 책상 6
        (int(760 * scale_x), int(350 * scale_y)),  # 책상 7
        (int(890 * scale_x), int(350 * scale_y)),  # 책상 8

        # 세 번째 행 - 오른쪽으로 50px, 위로 30px 이동
        (int(260 * scale_x), int(460 * scale_y)),  # 책상 9
        (int(390 * scale_x), int(460 * scale_y)),  # 책상 10
        (int(760 * scale_x), int(460 * scale_y)),  # 책상 11
        (int(890 * scale_x), int(460 * scale_y)),  # 책상 12

        # 네 번째 행 (맨 아래줄) - 오른쪽으로 50px, 위로 30px 이동
        (int(260 * scale_x), int(570 * scale_y)),  # 책상 13
        (int(390 * scale_x)+20, int(570 * scale_y)+20),  # 책상 14
        (int(760 * scale_x), int(570 * scale_y)),  # 책상 15
        (int(890 * scale_x), int(570 * scale_y)),  # 책상 16
    ]

    # 교탁 위치 (오른쪽으로 50px, 위로 30px 이동)
    teacher_desk = (int(550 * scale_x), int(170 * scale_y))

    # TV 위치 (오른쪽, 위로 이동)
    tv = (int(80 * scale_x), int(100 * scale_y))

    obstacles = []

    # 책상 충돌박스 생성
    for x, y in desks:
        rect = pygame.Rect(x, y, desk_width, desk_height)
        obstacles.append(rect)

    # 교탁 충돌박스 생성
    podium_rect = pygame.Rect(teacher_desk[0], teacher_desk[1], podium_width, podium_height)
    obstacles.append(podium_rect)

    # TV 충돌박스 생성
    tv_rect = pygame.Rect(tv[0], tv[1], tv_width, tv_height)
    obstacles.append(tv_rect)

    # 문 영역 설정 (하단 중앙 부분)
    door_width = int(200 * scale_x)
    door_height = int(50 * scale_y)
    door_x = int(int(210 * scale_x)-50)
    door_y = int(h - door_height)  # 화면 하단
    door_rect = pygame.Rect(door_x, door_y, door_width, door_height)

    return obstacles, door_rect


def play_Game(screen, show_endCheck):
    print("게임 플레이!")
    running = True
    pygame.mixer.music.stop()
    pygame.mixer.init()  # 사운드 시스템 초기화

    WIDTH, HEIGHT = screen.get_width(), screen.get_height()

    clock = pygame.time.Clock()
    frame = 60  # 초당 60번 화면을 갱신함

    # 캐릭터 위치
    player_x = 900
    player_y = 100  # 초기 위치를 화면 내부로 설정

    # 걷기 애니메이션 타이머
    walk_frame = 0

    myImg = pygame.image.load("../img/앞_걷기1.png")
    player_width = myImg.get_width()
    player_height = myImg.get_height()

    # 마지막 이동 방향 (정지 상태일 때 사용할 이미지)
    last_moving = 'down'

    while running:
        # 배경 그리기 및 장애물 정보 가져오기
        obstacles, door_rect = draw_background(screen, WIDTH, HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_endCheck(screen)

        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        is_moving = False

        # 이동 키 처리
        if keys[pygame.K_w]:
            move_y = -5
            is_moving = True
            last_moving = 'up'
        elif keys[pygame.K_s]:
            move_y = 5
            is_moving = True
            last_moving = 'down'
        elif keys[pygame.K_a]:
            move_x = -5
            is_moving = True
            last_moving = 'left'
        elif keys[pygame.K_daa]:
            move_x = 5
            is_moving = True
            last_moving = 'right'

        # 걷기 프레임 업데이트
        if is_moving:
            walk_frame = (walk_frame + 1) % 30  # 0~29

        # 이동 예상 위치 계산
        new_x = player_x + move_x
        new_y = player_y + move_y

        # 화면 경계 제한 (캐릭터가 화면 밖으로 나가지 못하게)
        new_x = max(0, min(new_x, WIDTH - player_width))
        new_y = max(0, min(new_y, HEIGHT - player_height))

        new_rect = pygame.Rect(new_x, new_y, player_width, player_height)

        # 문 영역 체크 (복도로 이동)
        if new_rect.colliderect(door_rect):
            print("복도로 이동!")
            # 여기에 복도 화면으로 전환하는 코드를 추가하세요
            # 예: corridor_screen() 함수 호출
            # 또는 상태 변경: current_scene = "corridor"
            # 임시로 메시지만 출력
            running = False  # 임시로 게임 종료
            return

        # 장애물 충돌 체크
        can_move = True
        for obs in obstacles:
            if new_rect.colliderect(obs):
                can_move = False
                break

        # 충돌이 없으면 위치 업데이트
        if can_move:
            player_x = new_x
            player_y = new_y

        # 캐릭터 이미지 선택
        if is_moving:
            if last_moving == 'up':
                myImg = img_back_walk1 if walk_frame < 15 else img_back_walk2
            elif last_moving == 'down':
                myImg = img_front_walk1 if walk_frame < 15 else img_front_walk2
            elif last_moving == 'left':
                myImg = img_left_walk1 if walk_frame < 15 else img_left_walk2
            elif last_moving == 'right':
                myImg = img_right_walk1 if walk_frame < 15 else img_right_walk2
        else:
            # 정지 상태 이미지
            if last_moving == 'up':
                myImg = img_back
            elif last_moving == 'down':
                myImg = img_front
            elif last_moving == 'left':
                myImg = img_left
            elif last_moving == 'right':
                myImg = img_right

        # 캐릭터 그리기
        screen.blit(myImg, (player_x, player_y))
        pygame.display.flip()
        clock.tick(frame)


#순환 참조를 막기 위한 방법 -> 함수 내부에서 import하기
# 그러니깐 stage1에서 실행을 해서 해당 모듈을 바로 실행 시키는 건데
# 그 해당 모듈 파일에서 다시 역으로 참조시키니깐
# 해당 모듈에 있는 함수를 정의하지도 못하고 다시 돌아간다는 것