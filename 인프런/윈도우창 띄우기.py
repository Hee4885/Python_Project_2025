import pygame

pygame.init()

ourScreen = pygame.display.set_mode((400,300)) #화면 크기
pygame.display.set_caption("파이게임") #창 제목
finsh = False #게임 끝났나?

#안 끝났으면
while not finsh :
    for event in pygame.event.get() :
        #이벤트 타입이 끝났으면
        if event.type == pygame.QUIT :
            finsh = True
        #display 화면 업데이트
        pygame.display.update()