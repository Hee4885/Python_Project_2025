import pygame
import following_player

def gamePlay3(screen, show_endCheck, draw_text2, w, h, load_player, x=100, y=500) :
    corridor_img = pygame.image.load('../img/복도3.jpg')
    corridor_img = pygame.transform.scale(corridor_img, (w, h))

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_endCheck(screen)

        keyPress = pygame.key.get_pressed()

        # 위치와 이미지 동시 갱신
        x, y, myImg, move_x, move_y = following_player.following_players(keyPress, screen, w, h, show_endCheck, x, y)

        # blocked = wall_rect(screen, w, get_wall_rect, x, y, move_x, move_y, myImg, show_endCheck, draw_text2, h,
        #                     load_player)

        # if not blocked:
        #     x += move_x
        #     y += move_y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                show_endCheck(screen)

        screen.blit(corridor_img, (0, 0))
        screen.blit(myImg, (x, y))

        pygame.display.flip()

