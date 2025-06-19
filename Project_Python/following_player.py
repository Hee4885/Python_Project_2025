import pygame
import player_module

pygame.init()

bg_img = pygame.image.load("../img/교실1.jpg")

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

#아이템 이미지
img_flash = pygame.image.load('../img/손전등.png')

#아이템 충돌 유무
item_crash = False

#플레이어 동작 프레임
frame = 0
frameCount = 0

#플레이어
x, y = 200,300
last_moving = ''
myImg = pygame.image.load('../img/앞.png')
player_rect = img_front.get_rect()  # 이미지 크기만한 rect 생성 -> 현재 위치를 가짐
player_rect.topleft = (x, y)  # 캐릭터 초기 위치 지정 -> top left corner", 즉 왼쪽 위 꼭짓점 / Rect 위치 지정 또는 업데이트
crash_rect = pygame.Rect(x,y,10,10)


def following_players(keyPress, screen, w, h, show_endCheck, x, y):
    global frame,frameCount,myImg,player_rect,last_moving,crash_rect,item_crash # 값이 누적되야 되기 때문에 전역 변수로 관리
    # 이동 처리
    speed = 0
    keys = keyPress
    move_x, move_y = 0, 0
    is_moving = False
    #현재 modifier 키 상태 가져오기
    mods = pygame.key.get_mods()

    # Shift 키가 눌렸는지 확인 -> pygame.key.get_mods()는 비트 플래그 값을 반환. 1이면 참
    if mods & pygame.KMOD_SHIFT:
        print("Shift 눌림!")
        speed = 3
        frameCount = 15
    else :
        print("Shift 안 눌림!")
        speed = 1
        frameCount = 30
    if keys[pygame.K_w]:
        move_y = -speed
        # 파이썬 삼항 연산자 : A if 조건 else B -> 참이면 A, 거짓이면 B
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



    crash_rect = pygame.Rect(x+move_x,y+move_y, myImg.get_width(), myImg.get_height()) #이동할 위치에 캐릭터의 위치 사본


    #화면 경계 충돌 감지 -> x,는 0보다 작아질 수 없고, 화면 너비와 높이를 넘지 앟음
    x = max(0, min(x, w - myImg.get_width()))
    y = max(0, min(y, h - myImg.get_height()))

    # f_rect = friend_obj(screen)  # 친구 객체 Rect 가져오기


    #게임 루프가 한 번 돌 때 마다 1씩 증가, 60프레임은 1초
    frame += 1
    if frame>=frameCount*2 :
        frame = 0

    screen.blit(myImg,(x,y))

    return x,y,myImg,move_x,move_y
