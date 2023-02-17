import random
import sys

import pygame

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4

#         R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 255, 255)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')
    # -----
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    #사운드파일 로드 pygame.mixer.Sound(사운드 생성자 함수)
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')


    #실행시 사용할 변수 초기화
    pattern = [] # 색깔 패턴
    currentStep = 0 # 눌러야 할 색깔
    lastClickTime = 0 # 마지막으로 버튼을 누른 시간 -> 이 시간부터 특정 시간을 초과하면 time out
    score = 0

    # wFI -> False 시뮬레이트의 패턴을 보여주는 모드
    # wFI -> True  패턴을 보여준 후 플레이어의 버튼 클릭을 기다리는 모드
    waitingForInput = False


    while True: # 시뮬레이트를 위한 루프
        clickedButton = None # 클릭된 버튼을 None으로 초기화
        DISPLAYSURF.fill(bgColor)
        drawButtons() # 4개의 색깔 버튼을 그리는 함수 호출

        # 점수 표시를 위한 텍스트 생성 <----
        scoreSurf = BASICFONT.render('Score:' + str(score), 1, WHITE) # 색깔을 맞출시 점수를 올려야 하기에 loop문 안에서 렌더 함수 호출
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        DISPLAYSURF.blit(infoSurf, infoRect)

        # 마우스 클릭 검사
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos # 마우스 클릭시 해당 포인터의 x,y 좌표를 각각에 저장
                clickedButton = getButtonClicked(mousex, mousey) # 4개의 버튼중 어떤 버튼을 클릭했는지 color 객체 반환

            # 해당 키 버튼 == 해당 색깔
            elif event.type == KEYDOWN:
                if event.key == K_q: # q = 노란색
                    clickedButton = YELLOW

                elif event.key == K_w: # w = 파란색
                    clickedButton = BLUE

                elif event.key == K_a: # a = 빨간색
                    clickedButton = RED

                elif event.key == K_s: # s = 초록색
                    clickedButton = GREEN

        # 사용자에게 패턴을 보여줌
        if notwaitingForInput:
            # 패턴을 자동으로 보여줌.
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice(YELLOW, BLUE, RED, GREEN))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True  # 사용자의 클릭을 기다림

        # 사용자의 버튼 클릭을 기다림
        else:
            if clickedButton and clickedButton == pattern[currentStep]: # 맞는 버튼을 누름
                flashButtonAnimation(clickedButton) # 플레이어가 누른 버튼을 반짝이게한다.
                currentStep +=1
                lastClickTime = time.time() # 마지막 클릭 시간을 현재 시간으로 바꾼다.

                if currentStep == len(pattern):
                    # 마지맥 패턴의 버튼 클릭
                    changeBackGroundAnimation():
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # 게임 종료 후 초기화

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # time.time() - TIMEOUT > lastClickTime -> 시간초과 검사
                # 버튼을 잘못 누르거나 시간 초과 시
                gameOverAnimation()
                # 새 게임을 위한 변수 초기화
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackGroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate() # QUIT 이벤트가 발생 시 종료
    for event in pygame.event.get(KEYUP):
        if event.key == k_ESCAPE:
            terminate() # KEYUP 이벤트가 Esc면 종료
        pygame.event.post(event)







