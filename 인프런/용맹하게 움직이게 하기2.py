#coding=utf-8
import pygame

pygame.init()

ourScreen = pygame.display.set_mode((400,300)) #화면 크기
pygame.display.set_caption("파이게임") #창 제목
finsh = False #게임 끝났는지 체크 용도
colorBlue = True #색상 이벤트 체크용도
x = 30
y = 30
#초당 프레임
clock = pygame.time.Clock()

#안 끝났으면
while not finsh :
    for event in pygame.event.get() : #발생하는 이벤트들 event 변수에 넣기
        #이벤트 타입이 끝났으면
        if event.type == pygame.QUIT : #event 타입이 QUIT면 즉, 창 닫기이면
            finsh = True #게임이 끝났다고 바꾸기
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
            colorBlue = not colorBlue # 스페이스를 누르면(keyDown) 파랑이 아닌 걸로

    pressed = pygame.key.get_pressed() #어떤 키보드를 누르는지
    if pressed[pygame.K_UP] : y -= 3 #위로 가는 키보드면 -3 으로 y감소
    if pressed[pygame.K_DOWN] : y += 3
    if pressed[pygame.K_LEFT] : x -= 3
    if pressed[pygame.K_RIGHT] : x += 3
    ourScreen.fill((0,0,0)) #검은 화면으로 채우기

    if colorBlue : color = (0,128,255)
    else : color = (255,255,255)
    #사각형 그리기 -> 푸른색
    pygame.draw.rect(ourScreen, color , pygame.Rect(x,y,60,60)) #x,y,가로,세로
    #display 화면 업데이트 -> update는 일부 화면만 flip은 전체 화면
    pygame.display.flip()
    clock.tick(60) #초당 60프레임