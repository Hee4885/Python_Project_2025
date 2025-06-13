#coding=utf-8
import pygame

pygame.init()

ourScreen = pygame.display.set_mode((400,300)) #화면 크기
pygame.display.set_caption("파이게임") #창 제목
finsh = False #게임 끝났나?
colorBlue = True #색상 이벤트 체크용도

#안 끝났으면
while not finsh :
    for event in pygame.event.get() :
        #이벤트 타입이 끝났으면
        if event.type == pygame.QUIT :
            finsh = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
            colorBlue = not colorBlue # 스페이스를 누르면(keyDown) 파랑이 아닌 걸로
        if colorBlue : color = (0,128,255)
        else : color = (255,255,255)
        #사각형 그리기 -> 푸른색
        pygame.draw.rect(ourScreen, color , pygame.Rect(20,20,60,60)) #x,y,가로,세로
        #display 화면 업데이트
        pygame.display.update()