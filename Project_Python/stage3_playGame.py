import pygame
import sys

#초기화
pygame.init() #파이 게임 초기화
pygame.mixer.init() #사운드 시스템 초기화

#배경음악 설정
pygame.mixer.music.load('../music/cutsceneBGM.mp3')
pygame.mixer.music.play()

def play_Game(screen, show_endCheck) :
    import stage1_start_menu
    print("게임 플레이!")
    running = True
    screen = pygame.display.set_mode()
    while running :
        screen.fill((255,255,60))
        pygame.display.flip()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                stage1_start_menu.show_endCheck(screen)




#순환 참조를 막기 위한 방법 -> 함수 내부에서 imprt하기
# 그러니깐 stage1에서 실행을 해서 해당 모듈을 바로 실행 시키는 건데
# 그 해당 모듈 파일에서 다시 역으로 참조시키니깐
# 해당 모듈에 있는 함수를 정의하지도 못하고 다시 돌아간다는 거네?