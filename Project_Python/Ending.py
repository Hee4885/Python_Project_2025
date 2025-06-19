import pygame
import sys

def ending_cutscene(screen, show_endCheck):
    print("엔딩 시작")

    pygame.mixer.music.stop()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load("../music/엔딩브금.mp3")
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("엔딩")
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    font = pygame.font.Font("../font/HBIOS-SYS.ttf", 70)

    End_slides = [
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "무사히 폐교를 빠져나간 주인공.."},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "그런데... 주인공의 친구가 안 보였다."},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "순간 당황한 주인공은 경찰에 전화를 한다."},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "하지만 경찰에게 돌아오는 답변은..."},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "경찰: 아 예, 저희가 다 수색해봤는데"},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "경찰: 그 폐가에 아무도 없던데요?"},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "경찰: cctv에도 신고자분 혼자만 찍히셨어요."},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "그렇다. 사실 주인공은 혼자 간 것이였던 것..."},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "주인공: 뭐라고..? 나 혼자였다고? 그러면..."},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "주인공: 같이 있었던 걔는 누구지....?"},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": ""},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "END"},
        {"image": pygame.image.load("../img/１컷.jpg"), "text": "감사합니다."}
    ]

    def draw_text(text):
        label = font.render(text, True, (255, 255, 255))
        label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(label, label_rect)

    clock = pygame.time.Clock()
    slide_index = 0
    slide_start_time = pygame.time.get_ticks()
    running = True

    while running:
        screen.fill((0, 0, 0))
        current_slide = End_slides[slide_index]

        screen.blit(pygame.transform.scale(current_slide["image"], (WIDTH, HEIGHT)), (0, 0))
        draw_text(current_slide["text"])
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_endCheck(screen)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    slide_index += 1
                    if slide_index >= len(End_slides):
                        running = False

            if pygame.time.get_ticks() - slide_start_time > 2000:
                slide_index += 1
                if slide_index >= len(End_slides):
                    running = False
                else:
                    slide_start_time = pygame.time.get_ticks()

    # 루프 종료 후 완전 종료 처리
    pygame.quit()
    sys.exit()

