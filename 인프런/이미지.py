#coding = utf-8
import pygame
from pygame.examples.go_over_there import clock

pygame.init()
display_width = 800
display_height = 600

ourScreen = pygame.display.set_mode((display_width,display_height))

myImg = pygame.image.load('../img/앞.png') #이미지 로드하기
def myimg(x,y) :
    ourScreen.blit(myImg,(x,y)) #로드한 이미지 그리기, 그리고 x,y 값

x = (display_width * 0.5) #400픽셀 -> 이미지 위치
y = (display_height * 0.5)

#이벤트 핸들링
finshed = False
while not finshed :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            finshed = True
    ourScreen.fill((255,255,200))#배경색
    myimg(x,y) #이미지 그리기
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] : y -= 1
    if pressed[pygame.K_DOWN] :
        y += 1
        myImg = pygame.image.load('../img/앞.png')  # 이미지 로드하기
    if pressed[pygame.K_LEFT] :
        x -= 1
        myImg = pygame.image.load('img/왼쪽 걷기.PNG')  # 이미지 로드하기
    if pressed[pygame.K_RIGHT] :
        x += 1
        myImg = pygame.image.load('img/오른쪽 걷기.PNG')  # 이미지 로드하기

    pygame.display.flip() #화면 업데이트

clock.tick(60)
pygame.quit() #파이 게임 종료
quit() # 종료
