import pygame

def gamePlay3(screen, show_endCheck, draw_text2, w, h):
    running = True
    clock = pygame.time.Clock()

    # 이미지 한 번만 로드
    corridor_img = pygame.image.load('../img/복도.png')
    corridor_img = pygame.transform.scale(corridor_img, (w, h))  # 창 크기에 맞게 조정

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_endCheck(screen)

        screen.blit(corridor_img, (0, 0))


        pygame.display.flip()
        clock.tick(60)  # FPS 제한

