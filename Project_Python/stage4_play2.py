import pygame
import following_player


#장애물 위치 전달 함수
def get_wall_rect(w) :
    #가벽
    wall = [
        #위
        pygame.Rect(0,  0, w//2-100,400 ),
        pygame.Rect(990, 0, w //2-100 , 400),

        #아래
        pygame.Rect(0, 800, w // 2 - 100, 200),
        pygame.Rect(990, 800, w // 2 - 100, 200),

        #오른쪽 통로
        pygame.Rect(1650, 415, 100, 400),

    ]

    return wall


#장애물 설치 함수
def wall_rect(screen,w,get_wall_rect,x,y,move_x,move_y,myImg,show_endCheck,draw_text2,h,load_player) :
    crash_rect = pygame.Rect(x+move_x,y+move_y, myImg.get_width(), myImg.get_height()) #이동할 위치에 캐릭터의 위치 사본
    wall = get_wall_rect(w) # 벽 위치
    blocked = False

    for rect in get_wall_rect(w) :
        pygame.draw.rect(screen,(0,0,255),rect) #그릴 배경, 색상, 위치 및 크기 요소
        if crash_rect.colliderect(rect) :
            print("벽과 충돌")
            blocked =True

    right_wall = wall[-1]
    if crash_rect.colliderect(right_wall):
        print("오른쪽 벽과 충돌")
        import stage5_play3
        stage5_play3.gamePlay3(screen, show_endCheck, draw_text2, w, h, load_player,x=100, y=700)

    return blocked #충돌 없음




def gamePlay2(screen, show_endCheck, draw_text2, w, h, load_player,x,y):
    global block
    clock = pygame.time.Clock()
    corridor_img = pygame.image.load('../img/복도.jpg')
    corridor_img = pygame.transform.scale(corridor_img, (w, h))

    running = True
    while running:

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                show_endCheck(screen)

        keyPress = pygame.key.get_pressed()

        # 위치와 이미지 동시 갱신
        x, y, myImg,move_x,move_y = following_player.following_players(keyPress, screen, w, h, show_endCheck, x, y)

        blocked = wall_rect(screen,w,get_wall_rect,x,y,move_x,move_y,myImg,show_endCheck,draw_text2,h,load_player)


        if not blocked:
            x += move_x
            y += move_y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                show_endCheck(screen)

        screen.blit(corridor_img, (0, 0))
        screen.blit(myImg, (x, y))

        clock.tick(120) # 1초에 최대 60번만 루프 돌기
        pygame.display.flip()
