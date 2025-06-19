import pygame
import sys
import stage2_cutscene

pygame.init()
pygame.mixer.init()

# 전역 변수
volume = 50

# 화면 설정
screen = pygame.display.set_mode()
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("Goat's Curse")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 이미지, 폰트 등
start_img = pygame.image.load('../img/시작화면3.png')
scaled_img = pygame.transform.scale(start_img, (WIDTH, HEIGHT))
BtnImg = pygame.image.load('../img/버튼.png')

font_path = '../font/HBIOS-SYS.ttf'
font = pygame.font.Font(font_path, 30)
font2 = pygame.font.Font(font_path, 50)
font3 = pygame.font.Font(font_path, 40)

def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        button_img = pygame.transform.scale(BtnImg, (w, h))
        screen.blit(button_img, (x, y))

    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)
    return rect

def show_endCheck(screen):
    pygame.display.set_caption("종료 확인")
    cWIDTH, cHEIGHT = screen.get_width(), screen.get_height()

    checkText = "정말 종료하시겠습니까?"
    checkText_surface = font2.render(checkText, True, WHITE, BLACK)
    checkText_rect = checkText_surface.get_rect(center=(cWIDTH // 2 + 30, cHEIGHT // 2 - 100))

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(checkText_surface, checkText_rect)
        okBtn = draw_button("예", cWIDTH // 2 - 210, cHEIGHT // 2, 150, 100)
        noBtn = draw_button("아니요", cWIDTH // 2 - 50, cHEIGHT // 2, 400, 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if okBtn.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    sys.exit()
                elif noBtn.collidepoint(event.pos):
                    return

def how_to_play():
    running = True
    while running:
        screen.fill(BLACK)
        goBack_button = draw_button("Go Back", 20, 0, 170, 80)

        title = font.render("【게임 방법】", True, WHITE)
        line1 = font.render("[WASD] 키로 이동:", True, WHITE)
        line2 = font.render("    ↑ ↓ ← →", True, (0, 255, 1))
        line3 = font.render("     (화살표 방향별로 캐릭터 이동)", True, WHITE)
        line4 = font.render("[F] 키: 대화 및 상호작용", True, WHITE)
        line5 = font.render("[e] 키: 인벤토리 창 띄우기", True, WHITE)
        line6 = font.render("[shift] 키 : 달리기", True, WHITE)

        screen.blit(title, (WIDTH // 2 - 50, HEIGHT // 2 - 400))
        screen.blit(line1, (WIDTH // 2 - 300, HEIGHT // 2 - 200))
        screen.blit(line2, (WIDTH // 2 - 74, HEIGHT // 2 - 200))
        screen.blit(line3, (WIDTH // 2 + 100, HEIGHT // 2 - 200))
        screen.blit(line4, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
        screen.blit(line5, (WIDTH // 2 - 300, HEIGHT // 2 + 100))
        screen.blit(line6, (WIDTH // 2 - 300, HEIGHT // 2 + 250))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if goBack_button.collidepoint(event.pos):
                    running = False
        pygame.display.flip()

def settings_menu():
    global volume
    running = True
    while running:
        screen.fill(BLACK)
        text1 = font2.render("【설정】", True, WHITE)
        text2 = font3.render(f"음량: {volume}%", True, WHITE)
        goBack_button = draw_button("Go Back", 20, 0, 230, 80)

        screen.blit(text1, (WIDTH // 2 - 100, HEIGHT // 2 - 400))
        screen.blit(text2, (WIDTH // 2 - 100, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if goBack_button.collidepoint(event.pos):
                    running = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    volume = min(100, volume + 1)
                    pygame.mixer.music.set_volume(volume / 100)
                elif event.key == pygame.K_DOWN:
                    volume = max(0, volume - 1)
                    pygame.mixer.music.set_volume(volume / 100)
        pygame.display.flip()

def main_menu(screen):
    pygame.mixer.music.load('../music/lobbyBGM.mp3')
    pygame.mixer.music.play(-1)

    running = True
    next_Action = None

    while running:
        screen.fill(BLACK)
        screen.blit(scaled_img, (0, 0))

        start_button = draw_button("Start Game", 400, 450, 300, 80)
        howto_button = draw_button("How to Play", 350, 560, 400, 80)
        setting_button = draw_button("Settings", 400, 670, 300, 80)
        quit_button = draw_button("QUIT", 400, 780, 300, 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_endCheck(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("게임 시작!")
                    next_Action = "start"
                    running = False
                elif howto_button.collidepoint(event.pos):
                    print("게임 방법!")
                    how_to_play()
                elif setting_button.collidepoint(event.pos):
                    print("설정!")
                    settings_menu()
                elif quit_button.collidepoint(event.pos):
                    print("게임 종료!")
                    show_endCheck(screen)

        pygame.display.flip()

    return next_Action


action = main_menu(screen)

if action == "start":
    pygame.mixer.music.stop()
    stage2_cutscene.play_cutscene(screen,show_endCheck)
