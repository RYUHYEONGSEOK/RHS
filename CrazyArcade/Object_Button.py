from pico2d import *

class Button:
    def __init__(self, _x, _y, _type):
        self.buttonType = _type
        self.X ,self.Y = _x, _y
        self.mouseX, self.mouseY = 0, 0
        self.events = None;
        #충돌인지 아닌지 체크하는 부분과 이미지
        self.frame = 0

    def __del__(self):
        self.exit()

    def enter(self):
        #버튼의 종류를 인식(1.시작버튼 2.맵선택1 3.맵선택2 4.나가기 5~8.로비아이템수증가)
        if self.buttonType == 1:
            self.sizeX, self.sizeY = 192, 55
            self.buttonImage = load_image('Sprite\\02.Lobby\\Lobby_Button_Start.png')
        elif self.buttonType == 2:
            self.sizeX, self.sizeY = 135, 21
            self.buttonImage = load_image('Sprite\\02.Lobby\\Loddy_Image_SelectMap_0.png')
        elif self.buttonType == 3:
            self.sizeX, self.sizeY = 135, 21
            self.buttonImage = load_image('Sprite\\02.Lobby\\Loddy_Image_SelectMap_1.png')
        elif self.buttonType == 4:
            self.sizeX, self.sizeY = 140, 32
            self.buttonImage = load_image('Sprite\\03.InGame\\InGame_Button_Out.png')
        elif self.buttonType == 5:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('Sprite\\02.Lobby\\Lobby_QButton.bmp')
        elif self.buttonType == 6:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('Sprite\\02.Lobby\\Lobby_WButton.bmp')
        elif self.buttonType == 7:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('Sprite\\02.Lobby\\Lobby_EButton.bmp')
        elif self.buttonType == 8:
            self.sizeX, self.sizeY = 33, 26
            self.buttonImage = load_image('Sprite\\02.Lobby\\Lobby_RButton.bmp')

    def exit(self):
        del (self.buttonImage)

    def update(self, _events):
        if (((self.X - self.sizeX / 2) < self.mouseX) and ((self.X + self.sizeX / 2) > self.mouseX)) \
                and (((self.Y - self.sizeY / 2) < (600 - self.mouseY)) and ((self.Y + self.sizeY / 2) > (600 - self.mouseY))):
            self.frame = 1
        else:
            self.frame = 0

        # 키의 종류에 따라서 달라지는 리턴값들
        if(self.keycheck(_events)):
            return self.buttonType

    def draw(self):
        #프레임이 시작하는 그림에서의 X좌표, Y좌표(Y좌표는 아래서부터 1) => 왼쪽 아래부터 오른쪽 위까지 하나를 그림
        if (self.buttonType == 1) or (self.buttonType == 4):
            self.buttonImage.clip_draw((self.frame * self.sizeX), 0,
                                        self.sizeX, self.sizeY,
                                        self.X, self.Y)
        elif (self.buttonType == 2) or (self.buttonType == 3):
            self.buttonImage.clip_draw(((self.frame - 1) * self.sizeX), 0,
                                       self.sizeX, self.sizeY,
                                       self.X, self.Y)
        elif (self.buttonType >= 5) and (self.buttonType <= 8):
            self.buttonImage.clip_draw(0, 0,
                                       self.sizeX, self.sizeY,
                                       self.X, self.Y)

    def keycheck(self, _events):
        # 마우스값을 받음
        self.events = _events

        for event in self.events:
            if event.type == SDL_MOUSEMOTION:
                self.mouseX, self.mouseY = event.x, event.y
            if (event.type, self.frame) == (SDL_MOUSEBUTTONUP, 1):
                return True