import stage2_cutscene
import pygame
import sys

# from pygame.examples.music_drop_fade import volume

# from pygame import FULLSCREEN
# from pygame.examples.moveit import WIDTH, HEIGHT

#초기화
pygame.init() #파이 게임 초기화
pygame.mixer.init() #사운드 시스템 초기화

# 초기 음량 설정 - 전역 변수
volume = 50

#음악 재생
pygame.mixer.music.load('../music/달리기.mp3')
pygame.mixer.music.play(-1)


#창 기본 설정
screen = pygame.display.set_mode()
WIDTH,HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("Goat's Curse")


#색상
WHITE = (255,255,255)
GRAY = (100,100,100)
BLACK = (0,0,0)
RED = (80,10,20)
GREEN = (0,255,1)

#화면 이미지
start_img = pygame.image.load('../img/시작화면3.png')
scaled_img = pygame.transform.scale(start_img,(WIDTH,HEIGHT))

#버튼 이미지
BtnImg = pygame.image.load('../img/버튼.png')

#폰트 및 크기
# font = pygame.font.SysFont("malgungothic", 30)
font_path = '../font/HBIOS-SYS.ttf'
font = pygame.font.Font(font_path, 30) # 별도 폰트 사용 시
font2 = pygame.font.Font(font_path, 50) # 별도 폰트 사용 시
font3 = pygame.font.Font(font_path, 40) # 별도 폰트 사용 시


#게임 종료 확인 화면 생성 함수
def show_endCheck(screen):
    pygame.display.set_caption("종료 확인")
    cWIDTH, cHEIGHT = screen.get_width(), screen.get_height()

    checkText = "정말 종료하시겠습니까?"

    checkText_surface = font2.render(checkText, True,(255,255,255),(0,0,0))

    checkText_rect = checkText_surface.get_rect()

    checkText_rect.center = (cWIDTH//2+30,cHEIGHT//2-100)


    running = True

    while running :
        screen.fill((0,0,0))

        screen.blit(checkText_surface, checkText_rect)
        okBtn = draw_button(str("예"),cWIDTH//2-210,cHEIGHT//2,150,100)
        noBtn = draw_button(str("아니요"),cWIDTH//2-50,cHEIGHT//2,400,100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if okBtn.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    sys.exit()

                elif noBtn.collidepoint(event.pos) :
                    return #호출한 메인 화면으로 돌아감




#게임 방법 버튼 함수
def how_to_play() :
    running = True
    while running :
        screen.fill((0, 0, 0))
        goBack_button = draw_button("Go Back", 20, 950, 170, 80)

        #render는 글씨로 이미지로 바꾸는 함수 (text, 곡선 부드럽게 처리, color)
        title = font.render("【게임 방법】", True, WHITE)
        line1 = font.render("방향키로 이동:", True, WHITE)
        line2 = font.render("↑ ↓ ← →", True, GREEN)
        line3 = font.render("(화살표 방향별로 캐릭터 이동)", True, WHITE)
        line4 = font.render("[F] 키: 대화 및 상호작용", True, WHITE)
        line5 = font.render("[e] 키: 인벤토리 창 띄우기", True, WHITE)
        line6 = font.render("space 바 : 대화 및 컷신 건너뛰기", True, WHITE)



        screen.blit(title, (WIDTH//2-50, HEIGHT//2-400))
        screen.blit(line1, (WIDTH//2-300, HEIGHT//2-200))
        screen.blit(line2, (WIDTH//2-74, HEIGHT//2-200))
        screen.blit(line3, (WIDTH//2+100, HEIGHT//2-200))

        screen.blit(line4, (WIDTH//2-300, HEIGHT//2-50))
        screen.blit(line5, (WIDTH//2-300, HEIGHT//2+100))
        screen.blit(line6, (WIDTH//2-300, HEIGHT//2+250))



        for event in pygame.event.get(): # 발생한 이벤트를 계속 받기
            if event.type == pygame.MOUSEBUTTONDOWN: # 마우스를 클릭한 이벤트면
                if goBack_button.collidepoint(event.pos): # 클릭한 위치가 goBack 버튼이면
                    running = False # 실행 중지
        pygame.display.flip() # 전체적인 업데이트

#설정 버튼 함수
def settings_menu():
    running = True
    global volume # 전역 변수로 사용 및 선언 -> 변경된 음량 유지 / 기존 지역 변수를 가져옴
    while running:
        screen.fill((0, 0, 0))
        text1 = font2.render("【설정】", True, WHITE)
        text2 = font3.render(f"음량: {volume}%", True, WHITE)
        goBack_button = draw_button("Go Back", 20,950,230,80)

        screen.blit(text1, (WIDTH//2-100, HEIGHT//2-400))
        screen.blit(text2, (WIDTH//2-100, HEIGHT//2))

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN :
                if goBack_button.collidepoint(event.pos) :
                    running = False

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    volume = min(100, volume + 1) #음량 최대 증가값은 100
                    #pygame.mixer.music은 음악 제어 / set_volume()은 실수값으로 음량 조절
                    pygame.mixer.music.set_volume(volume/100) #1.0이 최대이므로 변환함
                elif event.key == pygame.K_DOWN:
                    volume = max(0, volume - 1) #최대 감소값은 0
                    pygame.mixer.music.set_volume(volume/100)

        pygame.display.flip()


#버튼 생성 함수
def draw_button(text,x,y,w,h) :
    rect = pygame.Rect(x,y,w,h) #버튼 내용, 위치, 크기
    mouse_pos = pygame.mouse.get_pos()

    # 마우스 커서 위치가 사각형 안에 있는지 확인
    if rect.collidepoint(mouse_pos):
        button_img = pygame.transform.scale(BtnImg,(w,h)) #버튼 이미지를 비율만큼 변형 시키는 함수
        screen.blit(button_img,(x,y)) #버튼 출력

    label = font.render(text,True,WHITE) #텍스트 표면 만들기
    label_rect = label.get_rect(center=rect.center) #텍스트 담는 버튼을 중앙에 배치
    screen.blit(label,label_rect) #텍스트 그리기
    return rect #버튼 영역 반환해서 체크용

#메인 메뉴 루프 시작
def main_menu(screen):
    next_Action = None
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(scaled_img, (0, 0))  # 이미지 출력

        # 버튼 4개 생성 - 마우스 클릭 감지
        start_button = draw_button(str("Start Game"), 400, 450, 300, 80)
        howto_button = draw_button(str("How to Play"), 350, 560, 400, 80)
        setting_button = draw_button(str("Settings"), 400, 670, 300, 80)
        quit_button = draw_button(str("QUIT"), 400, 780, 300, 80)


        # 이벤트 처리 - 사용자의 행동 감지
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Alt + F4 버튼을 누르면 자동으로 이 이벤트를 넘겨줌
                show_endCheck(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("게임 시작!")
                    next_Action = "start"
                    running = False
                elif howto_button.collidepoint(event.pos):
                    print("게임 방법!")
                    how_to_play()
                elif quit_button.collidepoint(event.pos):
                    print("게임 종료!")
                    show_endCheck(screen)
                elif setting_button.collidepoint(event.pos):
                    print("설정!")
                    settings_menu()

        pygame.display.flip()

    return next_Action

action = main_menu(screen)

#순환 참조 해결 방법2
if action == "start" :
    pygame.mixer.music.pause()
    stage2_cutscene.play_cutscene(screen,show_endCheck)
