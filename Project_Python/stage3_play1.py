import pygame

from player_module import load_player,draw_item

#아이템 충돌 유무
item_crash = False

#대화 창 반복 여부
play_dialog = False

bg_img = pygame.image.load('../img/교실1.jpg')

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
        load_player(keyPress, screen, get_object_rect, WIDTH, HEIGHT, draw_text2, show_endCheck,show_dialog,friend_obj,draw_item)

        pygame.display.flip() #화면 업데이트