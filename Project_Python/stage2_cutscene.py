import pygame
import sys


def play_cutscene(screen, show_endCheck):
    import stage3_playGame
    print("컷신 실행")

    pygame.display.set_caption("컷신 예시")
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()

    font = pygame.font.SysFont("malgungothic", 40)

    slides = [
        {"image": pygame.image.load("../img/컷신1.jpg"), "text": "모든 일은 한 마을에서 시작되었다..."},
        {"image": pygame.image.load("../img/컷신2.jpg"), "text": "그 마을에는 무언가... 이상한 것이 있었다."},
        {"image": pygame.image.load("../img/컷신3.jpg"), "text": "그리고, 주인공은 그 마을로 향한다."},
    ]

    def draw_text(text):
        label = font.render(text, True, (255, 255, 255))
        label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(label, label_rect) # (source, dext) -> (복사할 원본, 복사할 위치)

    clock = pygame.time.Clock() #FPS(초당 프레임 수) 제어 객체 -> 초당 최대 60번 루프, 속도 제한
    slide_index = 0 #현재 보여줄 컷신 장면 번호
    slide_start_time = pygame.time.get_ticks() #파이게임 시작된 이후 흐른 시간 / 경과 시간 체크

    running = True
    while running:
        screen.fill((0, 0, 0))
        current_slide = slides[slide_index] #현재 슬라이드

        screen.blit(pygame.transform.scale(current_slide["image"], (WIDTH, HEIGHT)), (0, 0)) #현재 슬라이드를 화면 사이즈로 키우고, 전체 화면에 위치하게 그리기
        draw_text(current_slide["text"]) #슬라이드에 해당하는 문장 출력

        pygame.display.flip() #화면 업데이트
        clock.tick(60) #일정한 프레임 속도 제어 / 해당 루프가 1초에 60번 실행

        pressed = pygame.key.get_pressed()

        #수동 넘김
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_endCheck(screen)
            if pressed[pygame.K_SPACE] :
                slide_index += 1
                if slide_index >= len(slides): #마지막 슬라이드에 도달하면
                    running = False #루프 종료
                else:
                    slide_start_time = pygame.time.get_ticks() #해당 슬라이드가 띄워진 시간 저장

        # 2초가 지나면 다음 슬라이드로 자동 전환 - 자동 넘김(2초간격)
        if pygame.time.get_ticks() - slide_start_time > 2000: #지금 시각 - 시작 시각이 2초를 넘으면
            slide_index += 1 #다음 슬라이드로 전환하기 위한 인덱스 증가
            if slide_index >= len(slides): #슬라이드가 마지막에 도달하면
                running = False # 종료
            else:
                slide_start_time = pygame.time.get_ticks()

    # 컷신 끝나면 다음 스테이지로
    stage3_playGame.play_Game(screen, show_endCheck)



# 시작 버튼이 컷신으로 안 넘어간 이유

# 파이썬의 순환 참조라는 것 때문이다.

# 순환 참조란 두 개의 모듈이 서로를 import 하기 때문이다.

# 하나의 모듈을 import 했을 때 또 다른 모듈에서 이전과 같은 모듈을 참조하면
# 이전에 import 한 모듈이 다 끝나지 않고 내부의 함수나 변수들을 정의하지 못하게 됨

# 이 때문에 AttributeError 또는 NameError 또는 이상 작동이 발생함

# 파이썬은 import를 할 때 실제로 한 번 실행해서 해당 파일의 함수와 변수를 로딩함

# 하지만 이때 순환 참조가 발생하면 아직 로딩되지 않은 상태에서 정의되지 않은 함수를 호출하려다
# 그냥 아무 실행 없이 넘기거나 이상 동작을 발생하는 것이다.


# 따라서 내부적으로 모듈 캐시와 지연 로딩을 사용했기 때문에 그랬던 것이며, 이를 반드시 주의해야함
