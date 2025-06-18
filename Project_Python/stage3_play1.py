import pygame

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


#플레이어 동작 프레임
frame = 0
frameCount = 0

#플레이어
x, y = 700, 400
last_moving = ''
myImg = pygame.image.load('../img/앞.png')
player_rect = img_front.get_rect()  # 이미지 크기만한 rect 생성 -> 현재 위치를 가짐
player_rect.topleft = (x, y)  # 캐릭터 초기 위치 지정 -> top left corner", 즉 왼쪽 위 꼭짓점 / Rect 위치 지정 또는 업데이트
crash_rect = pygame.Rect(x,y,10,10)

#대화 창 반복 여부
play_dialog = False

#아이템 충돌 여부
item_crash = False

def show_dialog(speaker, w, h, screen, draw_text2):
    global  play_dialog
    dialog_rect = pygame.Rect(0, 700, w, h - 400)

    FdialogList = [
        {"image": pygame.image.load("../img/친구_표정_짜증.png"), "text": "여기가 어디야.. 뭐야... 잘 못 되는 거 아니야?!?!"},
        {"image": pygame.image.load("../img/표정_기본.png"), "text": "조용히 해봐! 빨리 여기서 나갈 준비나 해.."}
    ]

    if not play_dialog :
        if speaker == "f":
            play_dialog = True
            for Fdialog in FdialogList:
                # 1. 대화창 영역 초기화 (검정 배경 + 흰색 테두리)
                pygame.draw.rect(screen, (0, 0, 0), dialog_rect)
                pygame.draw.rect(screen, (255, 255, 255), dialog_rect, 10)  # 흰 테두리

                # 2. 캐릭터 이미지
                screen.blit(pygame.transform.scale(Fdialog["image"], (200, 250)), (70, 755))

                # 3. 텍스트 출력
                draw_text2(Fdialog["text"])

                # 4. 업데이트 및 대기
                pygame.display.update(dialog_rect)
                pygame.time.delay(1500)
            # 대화 다 끝났으면 대화창 제거
            pygame.display.flip()

def load_player(keyPress,screen, get_object_rect,w,h,draw_text2,show_endCheck) :
    global x,y,frame,frameCount,myImg,player_rect,last_moving,crash_rect,item_crash # 값이 누적되야 되기 때문에 전역 변수로 관리
    # 이동 처리
    speed = 0
    keys = pygame.key.get_pressed()
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


    #화면 경계 충돌 감지 -> x,ㅛ는 0보다 작아질 수 없고, 화면 너비와 높이를 넘지 앟음
    x = max(0, min(x, w - myImg.get_width()))
    y = max(0, min(y, h - myImg.get_height()))

    #친구와 충돌했을 때
    f_rect = friend_obj(screen)  # 친구 객체 Rect 가져오기

    #충돌 감지
    blocked = False
    #문 위치
    obstacles = get_object_rect(w)
    door1 = obstacles[-2] #2번째로 마지막 요소
    door2 = obstacles[-1] #1번째로 마지막 요소

    i_rect = draw_item(screen)
    f_rect = friend_obj(screen)
    for obj in get_object_rect(w) : #object 리스트에 있는 위치들 비교
        # 이동한 위치가 리스트에 있는 위치와 같으면 / colliderect은 요소들 간에 겹침을 판단함 / 겹치면 True, 아니면 False 리턴
        if crash_rect.colliderect(obj) :
            blocked = True
            print("장애물과 충돌")
            break

        if crash_rect.colliderect(f_rect) :
            blocked = True
            print("친구와 충돌")
            #대화창
            show_dialog("f",w,h,screen,draw_text2)
            break #이동 막기

        #i_rect가 None이 아닐 때, 캐릭터와 아이템이 충돌했을 때
        if i_rect and crash_rect.colliderect(i_rect) :
            blocked = True
            print("손전등과 충돌")
            #아이템 창 구현
            # inventory(screen, keyPress)
            #아이템 사라지기
            item_crash = True
            break #이동 막기

        # #첫번째 문과 닿으면
        if crash_rect.colliderect(door1) :
            import stage4_play2
            stage4_play2.gamePlay2(screen,show_endCheck,draw_text2,w,h)
        #두 번째 문과 닿으면
        if crash_rect.colliderect(door2) :
            #문이 잡겼다는 문구가 1초 동안 뜸
            door_lock_text = font2.render("문이 잠겨 있다..",True,(255,255,255))

            #crash_rect.centerx → 캐릭터 중앙 X 좌표  / crash_rect.top - 10 → 캐릭터 머리에서 약간 위
            #midbottom은 Rect 속성 중 하나이며 아래 중안 위치 좌표를 나타냄
            text_rect = door_lock_text.get_rect(midbottom=(crash_rect.centerx,crash_rect.top-15))

            screen.blit(door_lock_text,text_rect)

    #장애물이 없다면
    if not blocked :
        # 이미 이동한 위치
        x += move_x
        y += move_y


    #게임 루프가 한 번 돌 때 마다 1씩 증가, 60프레임은 1초
    frame += 1
    if frame>=frameCount*2 :
        frame = 0

    screen.blit(myImg,(x,y))


def background(screen,w,h) :
    scaled = pygame.transform.scale(bg_img, (w, h))
    screen.blit(scaled,(0,0))


def friend_obj (screen) :
    fx, fy = 900, 325
    FImg = pygame.image.load('../img/친구_앞.png')

    # 충돌 감지를 위한 작은 사각형 Rect 생성
    f_rect = pygame.Rect(fx + 10, fy + 20, FImg.get_width() // 3, FImg.get_height() // 3)

    # 친구 이미지 화면에 표시
    screen.blit(FImg,(fx,fy))

    return f_rect #충돌 감지를 위한 반환

#장애물 위치 전달 함수
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

#장애물 설치 함수
def object_rect(screen,w,get_object_rect) :
    for rect in get_object_rect(w) :
        pygame.draw.rect(screen,(0,0,255),rect) #그릴 배경, 색상, 위치 및 크기 요소


def draw_item (screen, ix=800,iy=600) :
    global item_crash
    if item_crash :
        return None

    iImg = pygame.image.load('../img/손전등.png')
    # 충돌 감지를 위한 작은 사각형 Rect 생성
    i_rect = pygame.Rect(ix, iy,iImg.get_width()//5, iImg.get_height()//5)
    # 아이템 이미지 화면에 표시
    screen.blit(iImg,(ix,iy))

    return i_rect #충돌 감지를 위한 반환


#stage1에 있는 함수에 대한 의존성을 버리기 위해 매개변수로 함수 받기
def gamePlay1(screen,show_endCheck,draw_text2) :
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
        draw_item(screen) #손전등 생성 함수


        # 캐릭터 이동 처리
        keyPress = pygame.key.get_pressed()
        # inventory(screen,keyPress)
        load_player(keyPress,screen,get_object_rect,WIDTH,HEIGHT,draw_text2,show_endCheck)

        pygame.display.flip() #화면 업데이트