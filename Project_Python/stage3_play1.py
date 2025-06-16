import pygame

pygame.init()

bg_img = pygame.image.load("../img/교실1.jpg")

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


#플레이어 동작 프레임
frame = 0

#플레이어
x, y = 700, 400
last_moving = ''
myImg = pygame.image.load('../img/앞.png')
player_rect = img_front.get_rect()  # 이미지 크기만한 rect 생성 -> 현재 위치를 가짐
player_rect.topleft = (x, y)  # 캐릭터 초기 위치 지정 -> top left corner", 즉 왼쪽 위 꼭짓점 / Rect 위치 지정 또는 업데이트


def load_player(keyPress,screen, get_object_rect,w,h) :
    global x,y,frame,myImg,player_rect,last_moving # 값이 누적되야 되기 때문에 전역 변수로 관리
    # 이동 처리
    keys = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    is_moving = False


    #파이썬 삼항 연산자 : A if 조건 else B -> 참이면 A, 거짓이면 B
    speed = 3
    if keys[pygame.K_w]:
        move_y = -speed
        myImg = img_back_walk1 if frame < 30 else img_back_walk2
        last_moving = 'up'
        is_moving = True
    elif keys[pygame.K_s]:
        move_y = speed
        myImg = img_front_walk1 if frame < 30 else img_front_walk2
        last_moving = 'down'
        is_moving = True
    elif keys[pygame.K_a]:
        move_x = -speed
        myImg = img_left_walk1 if frame < 30 else img_left_walk2
        last_moving = 'left'
        is_moving = True
    elif keys[pygame.K_d]:
        move_x = speed
        myImg = img_right_walk1 if frame < 30 else img_right_walk2
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


    #화면 경계 충돌 감지 -> x,ㅛ는 0보다 작아질 수 없고, 화면 너비와 높이를 넘지 앟음
    x = max(0, min(x, w - myImg.get_width()))
    y = max(0, min(y, h - myImg.get_height()))


    #충돌 감지
    blocked = False
    f_rect = friend_obj(screen)
    for obj in get_object_rect(w) : #object 리스트에 있는 위치들 비교
        # 이동한 위치가 리스트에 있는 위치와 같으면 / colliderect은 요소들 간에 겹침을 판단함 / 겹치면 True, 아니면 False 리턴
        if crash_rect.colliderect(obj)  :
            blocked = True
            break # 이동 막기
        if crash_rect.colliderect(f_rect) :
            blocked = True
            print("친구와 충돌")
            break # 이동 막기


    #장애물이 없다면
    if not blocked :
        # 이미 이동한 위치
        x += move_x
        y += move_y


    #게임 루프가 한 번 돌 때 마다 1씩 증가, 60프레임은 1초
    frame += 1
    if frame>=60 :
        frame = 0

    screen.blit(myImg,(x,y))

def background(screen,w,h) :
    scaled = pygame.transform.scale(bg_img, (w, h))
    screen.blit(scaled,(0,0))


def friend_obj (screen) :
    # 친구 위치 및 이미지
    x, y = 900, 325
    FImg = pygame.image.load('../img/친구_앞.png')

    # Rect를 통해 이미지 크기 기준 잡기
    f_rect = pygame.Rect(x + 10, y + 20, FImg.get_width()//3, FImg.get_height()//3)

    screen.blit(FImg,(x,y))

    return f_rect #충돌 감지를 위한 반환

def get_object_rect(w) :
    obstacle = [
        # 책상 (왼쪽 열)
        pygame.Rect(280, 360, 100, 70),
        pygame.Rect(280, 500, 100, 70),
        pygame.Rect(280, 645, 100, 70),
        pygame.Rect(280, 800, 100, 70),

        # 책상 (왼쪽 중앙 열)
        pygame.Rect(500, 360, 100, 70),
        pygame.Rect(500, 500, 100, 70),
        pygame.Rect(500, 645, 100, 70),
        pygame.Rect(500, 800, 100, 70),

        # 책상 (오른쪽 중앙 열)
        pygame.Rect(1055, 360, 100, 70),
        pygame.Rect(1055, 500, 100, 70),
        pygame.Rect(1055, 645, 100, 70),
        pygame.Rect(1055, 800, 100, 70),

        # 책상 (오른쪽 열)
        pygame.Rect(1290, 360, 100, 70),
        pygame.Rect(1290, 500, 100, 70),
        pygame.Rect(1290, 645, 100, 70),
        pygame.Rect(1290, 800, 100, 70),

        # 교탁 (중앙)
        pygame.Rect((w // 2) - 120, 295, 200, 20),

        # TV
        pygame.Rect(50, 120, 250, 90),

        # 문 2개
        pygame.Rect(400, 1050, 120, 50),
        pygame.Rect(1170, 1050, 120, 50)
    ]

    return obstacle

def object_rect(screen,w,get_object_rect) :
    for rect in get_object_rect(w) :
        pygame.draw.rect(screen,(0,0,255),rect) #그릴 배경, 색상, 위치 및 크기 요소


#stage1에 있는 함수에 대한 의존성을 버리기 위해 매개변수로 함수 받기
def gamePlay1(screen,show_endCheck) :
    pygame.mixer.music.stop()
    pygame.mixer.init()

    print("stage3 시작")
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()

    running = True

    while running:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                show_endCheck(screen)

        get_object_rect(WIDTH)
        object_rect(screen,WIDTH,get_object_rect) # 장애물 생성 함수
        background(screen,WIDTH,HEIGHT) # 배경 생성 함수

        friend_obj(screen) #친구 생성 함수


        # 캐릭터 이동 처리
        keyPress = pygame.key.get_pressed()
        load_player(keyPress,screen,get_object_rect,WIDTH,HEIGHT)

        pygame.display.flip() #화면 업데이트