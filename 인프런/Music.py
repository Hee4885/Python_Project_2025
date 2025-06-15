# coding = utf-8
import pygame

pygame.init()

# 음악 재생
pygame.mixer.music.load('../music/달리기.mp3')
pygame.mixer.music.play(-1)

# 화면 크기
# display_width = 800
# display_height = 600
ourScreen = pygame.display.set_mode()

# 이미지 미리 로드

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


# 위치 및 이미지 설정
x = 400
y = 500
myImg = img_front


clock = pygame.time.Clock()
frame = 0

last_moving = 'down'
finshed = False
while not finshed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finshed = True

    # 키 입력 확인
    keys = pygame.key.get_pressed()
    is_moving = False

    #캐릭터의 움직임을 조정할 카운트 프레임 -> while문을 통해 빠르게 갱신됨 30프레임 당 0.5초
    frame += 1
    if frame > 30:
        frame = 0

    # 방향키에 따라 이동 및 이미지 설정
    if keys[pygame.K_UP]:
        y -= 5
        myImg = img_back_walk1 if frame < 15 else img_back_walk2
        is_moving = True
        last_moving = 'up'

    elif keys[pygame.K_DOWN]:
        y += 5
        myImg = img_front_walk1 if frame < 15 else img_front_walk2
        is_moving = True
        last_moving = "down"

    elif keys[pygame.K_LEFT]:
        x -= 5
        myImg = img_left_walk1 if frame < 15 else img_left_walk2
        is_moving = True
        last_moving = 'left'

    elif keys[pygame.K_RIGHT]:
        x += 5
        myImg = img_right_walk1 if frame < 15 else img_right_walk2
        is_moving = True
        last_moving = 'right'




    if not is_moving:
        if last_moving == 'up' :
            myImg = img_back  # 키 안 누를 때 기본 이미지
        elif last_moving == 'down' :
            myImg = img_front  # 키 안 누를 때 기본 이미지
        elif last_moving == 'right' :
            myImg = img_right  # 키 안 누를 때 기본 이미지
        elif last_moving == 'left' :
            myImg = img_left  # 키 안 누를 때 기본 이미지



    # 화면 그리기
    ourScreen.fill((0, 0, 0))
    ourScreen.blit(myImg, (x, y))
    # ourScreen.blit(startImg, (0, 0))


    pygame.display.flip()


    clock.tick(60)

pygame.quit()
quit()





# #coding = utf-8
# import pygame
# from pygame.examples.go_over_there import clock
#
# pygame.init()
# pygame.mixer.music.load('music/달리기.mp3') #음악 로드
# pygame.mixer.music.play(0) #음악 재생 횟수 1번은 0, 무한반복은 -1
#
#
# display_width = 800
# display_height = 600
#
# ourScreen = pygame.display.set_mode((display_width,display_height))
#
# myImg = pygame.image.load('img/앞.PNG') #이미지 로드하기
# def myimg(x,y) :
#     ourScreen.blit(myImg,(x,y)) #로드한 이미지 그리기, 그리고 x,y 값
#
# x = (display_width * 0.5) #400픽셀 -> 이미지 위치
# y = (display_height * 0.5)
#
# #이벤트 핸들링
# finshed = False
# while not finshed :
#     for event in pygame.event.get() :
#         if event.type == pygame.QUIT :
#             finshed = True
#     ourScreen.fill((255,255,200))#배경색
#     myimg(x,y) #이미지 그리기
#     pressed = pygame.key.get_pressed()
#     if pressed[pygame.K_UP] :
#         y -= 0.5
#         for event in pygame.event.get():  # 발생하는 이벤트들 event 변수에 넣기
#             while event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
#                 myImg = pygame.image.load('img/뒤_걷기.PNG')  # 이미지 로드하기
#                 myImg = pygame.image.load('img/뒤_걷기2.PNG')  # 이미지 로드하기
#     if pressed[pygame.K_DOWN] :
#         y += 0.5
#         # myImg = pygame.image.load('img/앞.PNG')  # 이미지 로드하기 -> 키를 때면
#         myImg = pygame.image.load('img/앞_걷기.PNG')  # 이미지 로드하기
#     if pressed[pygame.K_LEFT] :
#         x -= 0.5
#         # myImg = pygame.image.load('img/왼쪽 걷기.PNG')  # 이미지 로드하기
#         myImg = pygame.image.load('img/왼쪽_걷기.PNG')  # 이미지 로드하기
#
#     if pressed[pygame.K_RIGHT] :
#         x += 0.5
#         myImg = pygame.image.load('img/오른쪽_걷기.PNG')  # 이미지 로드하기
#
#     pygame.display.flip() #화면 업데이트
#
# clock.tick(60)
# pygame.quit() #파이 게임 종료
# quit() # 종료
#
#
# # #이벤트 핸들링
# # finshed = False
# # while not finshed :
# #     for event in pygame.event.get() :
# #         if event.type == pygame.QUIT :
# #             finshed = True
# #     ourScreen.fill((255,255,200))#배경색
# #     myimg(x,y) #이미지 그리기
# #     pygame.display.flip()
# # pygame.quit() #파이 게임 종료
# # quit() # 종료


# coding = utf-8
# import pygame
#
# pygame.init()
#
# # 음악 재생
# pygame.mixer.music.load('music/달리기.mp3')
# pygame.mixer.music.play(0)
#
# # 화면 크기
# display_width = 800
# display_height = 600
# ourScreen = pygame.display.set_mode((display_width, display_height))
#
# # 캐릭터 이미지 미리 로드
# img_front = pygame.image.load('img/앞.png')
# img_front_walk1 = pygame.image.load('img/앞_걷기.png')
# img_front_walk2 = pygame.image.load('img/앞_걷기2.png')
#
# img_back_walk1 = pygame.image.load('img/뒤_걷기.png')
# img_back_walk2 = pygame.image.load('img/뒤_걷기2.png')
#
# img_left_walk1 = pygame.image.load('img/왼쪽_걷기.png')
# img_left_walk2 = pygame.image.load('img/왼쪽_걷기2.png')
#
# img_right_walk1 = pygame.image.load('img/오른쪽_걷기.png')
# img_right_walk2 = pygame.image.load('img/오른쪽_걷기2.png')
#
# # 장애물 이미지
# img_goat = pygame.image.load('img/장애물_염소.png')
#
# # 캐릭터 위치
# x = display_width * 0.5
# y = display_height * 0.5
# myImg = img_front
#
# # 장애물들 위치 리스트
# obstacles = [
#     pygame.Rect(150, 100, 50, 50),
#     pygame.Rect(300, 200, 50, 50),
#     pygame.Rect(500, 400, 50, 50)
# ]
#
# clock = pygame.time.Clock()
# frame = 0
#
# def check_collision(new_rect):
#     for obs in obstacles:
#         if new_rect.colliderect(obs):
#             return True
#     return False
#
# finshed = False
# while not finshed:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             finshed = True
#
#     keys = pygame.key.get_pressed()
#     is_moving = False
#     move_x, move_y = 0, 0
#
#     frame += 1
#     if frame > 30:
#         frame = 0
#
#     # 방향키 입력 처리 (일단 이동값 저장만 함)
#     if keys[pygame.K_UP]:
#         move_y = -5
#         myImg = img_back_walk1 if frame < 15 else img_back_walk2
#         is_moving = True
#     elif keys[pygame.K_DOWN]:
#         move_y = 5
#         myImg = img_front_walk1 if frame < 15 else img_front_walk2
#         is_moving = True
#     elif keys[pygame.K_LEFT]:
#         move_x = -5
#         myImg = img_left_walk1 if frame < 15 else img_left_walk2
#         is_moving = True
#     elif keys[pygame.K_RIGHT]:
#         move_x = 5
#         myImg = img_right_walk1 if frame < 15 else img_right_walk2
#         is_moving = True
#
#     # 캐릭터 새 위치 계산
#     new_rect = pygame.Rect(x + move_x, y + move_y, 50, 50)
#
#     # 충돌 없을 때만 이동
#     if not check_collision(new_rect):
#         x += move_x
#         y += move_y
#     else:
#         myImg = img_front  # 충돌 시 멈춘 이미지
#
#     if not is_moving:
#         myImg = img_front
#
#     # 화면 그리기
#     ourScreen.fill((255, 255, 200))
#     ourScreen.blit(myImg, (x, y))
#     for obs in obstacles:
#         ourScreen.blit(img_goat, (obs.x, obs.y))
#     pygame.display.flip()
#
#     clock.tick(60)
#
# pygame.quit()
# quit()


