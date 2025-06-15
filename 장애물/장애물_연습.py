import pygame

pygame.init()

# 화면 설정
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("NPC 대화 및 표정 변경")

clock = pygame.time.Clock()

# 폰트
font = pygame.font.SysFont("malgungothic", 24)
hint_font = pygame.font.SysFont("malgungothic", 20)

# 플레이어 이미지 로드
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

# NPC 클래스
class NPC:
    def __init__(self, name, images, x, y, dialog_lines, face_imgs):
        self.name = name
        self.images = images  # npc 기본 이미지
        self.x = x
        self.y = y
        self.dialog_lines = dialog_lines
        self.face_imgs = face_imgs  # 대화 중 표정 이미지 리스트
        self.rect = pygame.Rect(x, y, images.get_width(), images.get_height())

# NPC 인스턴스 생성 (예시)
npc_list = [
    NPC(
        name="수호자",
        images=pygame.image.load('../img/오른쪽_걷기1.png'),
        x=500, y=300,
        dialog_lines=[
            "이곳은 금지된 숲이야...",
            "너무 깊이 들어가지 않는 게 좋아.",
            "하지만 네가 용감하다면 말릴 수는 없지."
        ],
        face_imgs=[
            pygame.image.load('../img/표정_기본.png'),
            pygame.image.load('../img/표정_놀람1.png'),
            pygame.image.load('../img/표정_탄식.png'),
        ]
    ),
    NPC(
        name="마을사람",
        images=pygame.image.load('../img/앞.png'),
        x=200, y=150,
        dialog_lines=[
            "여행자시군요!",
            "이 마을엔 위험이 도사리고 있어요.",
            "준비가 되었나요?"
        ],
        face_imgs=[
            pygame.image.load('../img/표정_기본.png'),
            pygame.image.load('../img/표정_놀람1.png'),
            pygame.image.load('../img/표정_탄식.png'),
        ]
    ),
]

# 플레이어 초기 위치 및 상태
x, y = 400, 300
myImg = img_front
frame = 0
last_moving = 'down'

# 대화 상태 변수
current_npc = None
dialog_index = 0
showing_dialog = False
dialog_possible = False

# 대화창 그리기 함수
def draw_dialog(surface, text, face_img):
    dialog_width = display_width
    dialog_height = 200
    dialog_x = 0
    dialog_y = display_height - dialog_height

    # 어두운 배경 오버레이
    overlay = pygame.Surface((display_width, display_height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    # 대화 상자
    pygame.draw.rect(surface, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height), 3)
    pygame.draw.rect(surface, (30, 30, 30), (dialog_x + 3, dialog_y + 3, dialog_width - 6, dialog_height - 6))

    # 텍스트 출력
    rendered_text = font.render(text, True, (255, 255, 255))
    surface.blit(rendered_text, (dialog_x + 200, dialog_y + 70))

    # NPC 얼굴 이미지 출력
    face_y = dialog_y - face_img.get_height() + 84
    surface.blit(face_img, (20, face_y))

# 게임 루프
running = True
while running:
    screen.fill((255, 255, 200))
    frame = (frame + 1) % 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if showing_dialog:
                if event.key == pygame.K_SPACE:
                    dialog_index += 1
                    if dialog_index >= len(current_npc.dialog_lines):
                        showing_dialog = False
                        dialog_index = 0
                        current_npc = None
                elif event.key == pygame.K_ESCAPE:
                    showing_dialog = False
                    dialog_index = 0
                    current_npc = None
            else:
                if dialog_possible and event.key == pygame.K_f:
                    showing_dialog = True
                    dialog_index = 0

    # 이동 처리
    keys = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    is_moving = False

    if not showing_dialog:
        prev_x, prev_y = x, y

        if keys[pygame.K_UP]:
            move_y = -5
            myImg = img_back_walk1 if frame < 15 else img_back_walk2
            last_moving = 'up'
            is_moving = True
        elif keys[pygame.K_DOWN]:
            move_y = 5
            myImg = img_front_walk1 if frame < 15 else img_front_walk2
            last_moving = 'down'
            is_moving = True
        elif keys[pygame.K_LEFT]:
            move_x = -5
            myImg = img_left_walk1 if frame < 15 else img_left_walk2
            last_moving = 'left'
            is_moving = True
        elif keys[pygame.K_RIGHT]:
            move_x = 5
            myImg = img_right_walk1 if frame < 15 else img_right_walk2
            last_moving = 'right'
            is_moving = True

        x += move_x
        y += move_y

        # 플레이어 충돌 박스 (캐릭터 크기에 맞게 조절하세요)
        player_rect = pygame.Rect(x, y, 50, 50)

        # NPC 충돌 검사 - 이동 제한
        collided = False
        for npc in npc_list:
            if player_rect.colliderect(npc.rect):
                collided = True
                break
        if collided:
            x, y = prev_x, prev_y

    if not is_moving:
        if last_moving == 'up':
            myImg = img_back
        elif last_moving == 'down':
            myImg = img_front
        elif last_moving == 'right':
            myImg = img_right
        elif last_moving == 'left':
            myImg = img_left

    # 대화 가능 NPC 찾기 (충돌한 NPC가 있으면 대화 가능)
    dialog_possible = False
    current_npc = None
    player_rect = pygame.Rect(x, y, 100, 100)
    for npc in npc_list:
        if player_rect.colliderect(npc.rect):
            dialog_possible = True
            current_npc = npc
            break

    # 그리기
    screen.blit(myImg, (x, y))
    for npc in npc_list:
        screen.blit(npc.images, (npc.x, npc.y))

    # 대화 가능 표시
    if dialog_possible and not showing_dialog:
        hint = hint_font.render("[F] 키로 대화하기", True, (0, 0, 0))
        screen.blit(hint, (x - 30, y - 30))

    # 대화창 및 NPC 표정 표시
    if showing_dialog and current_npc:
        face_index = min(dialog_index, len(current_npc.face_imgs) - 1)
        draw_dialog(screen, current_npc.dialog_lines[dialog_index], current_npc.face_imgs[face_index])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


# # import pygame
# #
# # pygame.init()
# #
# # # 화면 설정
# # display_width = 800
# # display_height = 600
# # screen = pygame.display.set_mode((display_width, display_height))
# # pygame.display.set_caption("대화창 예제")
# #
# # clock = pygame.time.Clock()
# #
# # # 음악
# # pygame.mixer.music.load('../music/달리기.mp3')
# # pygame.mixer.music.play(-1)
# #
# # # 이미지 로드
# # img_front = pygame.image.load('../img/앞.png')
# # img_front_walk1 = pygame.image.load('../img/앞_걷기1.png')
# # img_front_walk2 = pygame.image.load('../img/앞_걷기2.png')
# #
# # img_conversation = pygame.image.load('../img/표정_탄식.png')
# #
# # img_back = pygame.image.load('../img/뒤.png')
# # img_back_walk1 = pygame.image.load('../img/뒤_걷기1.png')
# # img_back_walk2 = pygame.image.load('../img/뒤_걷기2.png')
# #
# # img_left = pygame.image.load('../img/왼쪽.png')
# # img_left_walk1 = pygame.image.load('../img/왼쪽_걷기1.png')
# # img_left_walk2 = pygame.image.load('../img/왼쪽_걷기2.png')
# #
# # img_right = pygame.image.load('../img/오른쪽.png')
# # img_right_walk1 = pygame.image.load('../img/오른쪽_걷기1.png')
# # img_right_walk2 = pygame.image.load('../img/오른쪽_걷기2.png')
# #
# # # NPC 이미지
# # npc_img = pygame.image.load('../img/npc.png')
# #
# # # 위치
# # x, y = 400, 300
# # npc_x, npc_y = 500, 300
# # myImg = img_front
# #
# # frame = 0
# # last_moving = 'down'
# #
# # # 대화 관련
# # dialog_lines = [
# #     "이곳은 금지된 숲이야...",
# #     "너무 깊이 들어가지 않는 게 좋아.",
# #     "하지만 네가 용감하다면 말릴 수는 없지."
# # ]
# # current_dialog_index = 0
# # showing_dialog = False
# # dialog_possible = False  # C 키로 대화 가능 여부
# # dialog_font = pygame.font.SysFont("malgungothic", 24)
# #
# # def draw_dialog(surface, text):
# #     dialog_width = display_width
# #     dialog_height = 200
# #     dialog_x = 0
# #     dialog_y = display_height - dialog_height
# #
# #     # 어둡게
# #     overlay = pygame.Surface((display_width, display_height))
# #     overlay.set_alpha(180)
# #     overlay.fill((0, 0, 0))
# #     surface.blit(overlay, (0, 0))
# #
# #     # 대화 상자
# #     pygame.draw.rect(surface, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height), 3)
# #     pygame.draw.rect(surface, (30, 30, 30), (dialog_x + 3, dialog_y + 3, dialog_width - 6, dialog_height - 6))
# #
# #     # 텍스트
# #     rendered = dialog_font.render(text, True, (255, 255, 255))
# #     surface.blit(rendered, (dialog_x + 200, dialog_y + 70))
# #
# #     # 대화 얼굴 이미지
# #     char_x = 20
# #     char_y = dialog_y - img_front.get_height() + 84
# #     surface.blit(img_conversation, (char_x, char_y))
# #
# # # 게임 루프
# # running = True
# # while running:
# #     screen.fill((255, 255, 200))
# #
# #     for event in pygame.event.get():
# #         if event.type == pygame.QUIT:
# #             running = False
# #
# #         if event.type == pygame.KEYDOWN:
# #             if showing_dialog:
# #                 if event.key == pygame.K_SPACE:
# #                     current_dialog_index += 1
# #                     if current_dialog_index >= len(dialog_lines):
# #                         showing_dialog = False
# #                         current_dialog_index = 0
# #                 elif event.key == pygame.K_ESCAPE:
# #                     showing_dialog = False
# #                     current_dialog_index = 0
# #             else:
# #                 if dialog_possible and event.key == pygame.K_f:
# #                     showing_dialog = True
# #                     current_dialog_index = 0
# #
# #     keys = pygame.key.get_pressed()
# #     is_moving = False
# #     move_x, move_y = 0, 0
# #
# #     frame += 1
# #     if frame > 30:
# #         frame = 0
# #
# #     if not showing_dialog:
# #         if keys[pygame.K_UP]:
# #             move_y = -5
# #             myImg = img_back_walk1 if frame < 15 else img_back_walk2
# #             last_moving = 'up'
# #             is_moving = True
# #         elif keys[pygame.K_DOWN]:
# #             move_y = 5
# #             myImg = img_front_walk1 if frame < 15 else img_front_walk2
# #             last_moving = 'down'
# #             is_moving = True
# #         elif keys[pygame.K_LEFT]:
# #             move_x = -5
# #             myImg = img_left_walk1 if frame < 15 else img_left_walk2
# #             last_moving = 'left'
# #             is_moving = True
# #         elif keys[pygame.K_RIGHT]:
# #             move_x = 5
# #             myImg = img_right_walk1 if frame < 15 else img_right_walk2
# #             last_moving = 'right'
# #             is_moving = True
# #
# #         x += move_x
# #         y += move_y
# #
# #     if not is_moving:
# #         if last_moving == 'up':
# #             myImg = img_back
# #         elif last_moving == 'down':
# #             myImg = img_front
# #         elif last_moving == 'right':
# #             myImg = img_right
# #         elif last_moving == 'left':
# #             myImg = img_left
# #
# #     # 충돌 감지
# #     player_rect = pygame.Rect(x, y, 100, 100)
# #     npc_rect = pygame.Rect(npc_x, npc_y, 100, 100)
# #     dialog_possible = player_rect.colliderect(npc_rect)
# #
# #     # 캐릭터와 NPC 그리기
# #     screen.blit(myImg, (x, y))
# #     screen.blit(npc_img, (npc_x, npc_y))
# #
# #     # 힌트 메시지 표시 (C 키로 대화 시작)
# #     if dialog_possible and not showing_dialog:
# #         hint_font = pygame.font.SysFont("malgungothic", 20)
# #         hint_text = hint_font.render("[F] 키로 대화하기", True, (0, 0, 0))
# #         screen.blit(hint_text, (x - 30, y - 30))
# #
# #     # 대화창 표시 -> 표정 변화 및 대화 내용 번갈아 가며 바꾸기 구현
# #     if showing_dialog:
# #         draw_dialog(screen, dialog_lines[current_dialog_index])
# #
# #     pygame.display.flip()
# #     clock.tick(60)
# #
# # pygame.quit()
#
#
# import pygame
#
# pygame.init()
#
# # 화면 설정
# display_width = 800
# display_height = 600
# screen = pygame.display.set_mode((display_width, display_height))
# pygame.display.set_caption("대화창 예제")
#
# clock = pygame.time.Clock()
#
# # 배경 음악
# pygame.mixer.music.load('../music/달리기.mp3')
# pygame.mixer.music.play(-1)
#
# # 폰트
# dialog_font = pygame.font.SysFont("malgungothic", 24)
# hint_font = pygame.font.SysFont("malgungothic", 20)
#
# # 플레이어 이미지
# img_front = pygame.image.load('../img/앞.png')
# img_front_walk1 = pygame.image.load('../img/앞_걷기1.png')
# img_front_walk2 = pygame.image.load('../img/앞_걷기2.png')
#
# img_back = pygame.image.load('../img/뒤.png')
# img_back_walk1 = pygame.image.load('../img/뒤_걷기1.png')
# img_back_walk2 = pygame.image.load('../img/뒤_걷기2.png')
#
# img_left = pygame.image.load('../img/왼쪽.png')
# img_left_walk1 = pygame.image.load('../img/왼쪽_걷기1.png')
# img_left_walk2 = pygame.image.load('../img/왼쪽_걷기2.png')
#
# img_right = pygame.image.load('../img/오른쪽.png')
# img_right_walk1 = pygame.image.load('../img/오른쪽_걷기1.png')
# img_right_walk2 = pygame.image.load('../img/오른쪽_걷기2.png')
#
# # NPC 클래스
# class NPC:
#     def __init__(self, name, image, x, y, dialog, face_img):
#         self.name = name
#         self.image = image
#         self.x = x
#         self.y = y
#         self.dialog = dialog
#         self.face_img = face_img
#         self.rect = pygame.Rect(x, y, 100, 100)
#
# # NPC 목록
# npc_list = [
#     NPC("수호자", pygame.image.load('../img/npc.png'), 500, 300,
#         ["이곳은 금지된 숲이야...", "너무 깊이 들어가지 않는 게 좋아.", "하지만 네가 용감하다면 말릴 수는 없지."],
#         pygame.image.load('../img/표정_탄식.png')),
#
#     NPC("마을사람", pygame.image.load('../img/npc2.png'), 200, 150,
#         ["여행자시군요!", "이 마을엔 위험이 도사리고 있어요.", "준비가 되었나요?"],
#         pygame.image.load('../img/표정_놀람.png'))
# ]
#
# # 플레이어 위치 및 상태
# x, y = 400, 300
# myImg = img_front
# frame = 0
# last_moving = 'down'
#
# # 대화 상태
# current_npc = None
# current_dialog_index = 0
# showing_dialog = False
# dialog_possible = False
#
# # 대화창 그리기 함수
# def draw_dialog(surface, text, face_img):
#     dialog_width = display_width
#     dialog_height = 200
#     dialog_x = 0
#     dialog_y = display_height - dialog_height
#
#     # 배경 어둡게
#     overlay = pygame.Surface((display_width, display_height))
#     overlay.set_alpha(180)
#     overlay.fill((0, 0, 0))
#     surface.blit(overlay, (0, 0))
#
#     # 대화 상자
#     pygame.draw.rect(surface, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height), 3)
#     pygame.draw.rect(surface, (30, 30, 30), (dialog_x + 3, dialog_y + 3, dialog_width - 6, dialog_height - 6))
#
#     # 텍스트
#     rendered = dialog_font.render(text, True, (255, 255, 255))
#     surface.blit(rendered, (dialog_x + 200, dialog_y + 70))
#
#     # 얼굴 이미지
#     char_x = 20
#     char_y = dialog_y - face_img.get_height() + 84
#     surface.blit(face_img, (char_x, char_y))
#
# # 게임 루프
# running = True
# while running:
#     screen.fill((255, 255, 200))
#     frame = (frame + 1) % 30
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         elif event.type == pygame.KEYDOWN:
#             if showing_dialog:
#                 if event.key == pygame.K_SPACE:
#                     current_dialog_index += 1
#                     if current_dialog_index >= len(current_npc.dialog):
#                         showing_dialog = False
#                         current_dialog_index = 0
#                 elif event.key == pygame.K_ESCAPE:
#                     showing_dialog = False
#                     current_dialog_index = 0
#             else:
#                 if dialog_possible and event.key == pygame.K_f:
#                     showing_dialog = True
#                     current_dialog_index = 0
#
#     # 이동 처리
#     keys = pygame.key.get_pressed()
#     move_x, move_y = 0, 0
#     is_moving = False
#
#     if not showing_dialog:
#         if keys[pygame.K_UP]:
#             move_y = -5
#             myImg = img_back_walk1 if frame < 15 else img_back_walk2
#             last_moving = 'up'
#             is_moving = True
#         elif keys[pygame.K_DOWN]:
#             move_y = 5
#             myImg = img_front_walk1 if frame < 15 else img_front_walk2
#             last_moving = 'down'
#             is_moving = True
#         elif keys[pygame.K_LEFT]:
#             move_x = -5
#             myImg = img_left_walk1 if frame < 15 else img_left_walk2
#             last_moving = 'left'
#             is_moving = True
#         elif keys[pygame.K_RIGHT]:
#             move_x = 5
#             myImg = img_right_walk1 if frame < 15 else img_right_walk2
#             last_moving = 'right'
#             is_moving = True
#
#         x += move_x
#         y += move_y
#
#     if not is_moving:
#         if last_moving == 'up':
#             myImg = img_back
#         elif last_moving == 'down':
#             myImg = img_front
#         elif last_moving == 'right':
#             myImg = img_right
#         elif last_moving == 'left':
#             myImg = img_left
#
#     # NPC 충돌 검사
#     dialog_possible = False
#     current_npc = None
#     player_rect = pygame.Rect(x, y, 100, 100)
#
#     for npc in npc_list:
#         if player_rect.colliderect(npc.rect):
#             dialog_possible = True
#             current_npc = npc
#             break
#
#     # NPC와 캐릭터 그리기
#     screen.blit(myImg, (x, y))
#     for npc in npc_list:
#         screen.blit(npc.image, (npc.x, npc.y))
#
#     # 힌트
#     if dialog_possible and not showing_dialog:
#         hint_text = hint_font.render("[F] 키로 대화하기", True, (0, 0, 0))
#         screen.blit(hint_text, (x - 30, y - 30))
#
#     # 대화창 표시
#     if showing_dialog and current_npc:
#         draw_dialog(screen, current_npc.dialog[current_dialog_index], current_npc.face_img)
#
#     pygame.display.flip()
#     clock.tick(60)
#
# pygame.quit()

