from pygame import *

from random import randint

from time import time as timer


#Класс для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, size, speed):
        super().__init__()
        #Размер спрайта
        self.size = size
        # Картинка спрайта
        self.image = transform.scale(image.load(img), size) 
        # Скорость спрайта
        self.speed = speed
        # "Физическая модель" спрайта (прямоугольник, в который вписан спрайт)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#Класс для игрока, двойное наследование
class Player(GameSprite):
    def __init__(self, img, x, y, size, speed, key_up, key_down):
        super().__init__(img, x, y, size, speed)
        self.key_up = key_up
        self.key_down = key_down

    def update(self):
        keys = key.get_pressed()

        if keys[self.key_up] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[self.key_down] and self.rect.y < win_size[1] - self.size[1] - 5:
            self.rect.y += self.speed


# Класс для мяча
class Ball(GameSprite):
    def __init__(self, img, x, y, size, speed, speed_x, speed_y):
        super().__init__(img, x, y, size, speed)
        self.speed_x= speed_x
        self.speed_y= speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_x(self):
        self.speed_x *= -1

    def bounce_y(self):
        self.speed_y *= -1


#Настройка игровой сцены
win_size = (700, 500)
window = display.set_mode(win_size)
display.set_caption("Ping-Pong")
back_img = image.load("background.jpg")
background = transform.scale(back_img, win_size)

#Паоаметры игры
game = True
finish = False
clock = time.Clock()
FPS = 60
racket_img = "racket.png"
score_1 = 0
score_2 = 0

#Создание игроков
player_1 = Player(racket_img, 30, 200, (40, 140), 4, K_UP, K_DOWN)
player_2 = Player(racket_img, 620, 200, (40, 140), 4, K_w, K_s)

#Создание мяча
ball_img = "ball.png"
ball = Ball(ball_img, 300, 300, (40, 40), 0, 3, 3)
# Надписи игры
font.init()
my_font = font.SysFont("verdana", 20, bold = True)
endgame_font = font.SysFont("verdana", 76)
lose_1 = endgame_font.render("Игрок 1 проиграл!", True, (180, 0, 0))
lose_2 = endgame_font.render("Игрок 2 проиграл!", True, (180, 0, 0))
goal_font = font.SysFont("verdana", 20)
goal_1 = goal_font.render("Игрок 1 забивает!", True, (0, 0, 255))
goal_2 = goal_font.render("Игрок 2 забивает!", True, (255, 0, 0))


#Игровой цикл
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        score_1_text = my_font.render(f"Счёт 1: {score_1}", True, (0, 0 , 0))
        score_2_text = my_font.render(f"Счёт 2: {score_2}", True, (0, 0 , 0))
        window.blit(score_1_text, (10, 15))
        window.blit(score_2_text, (win_size[0]-115, 15))


        player_1.update()
        player_2.update()
        ball.update()

        player_1.reset()
        player_2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)