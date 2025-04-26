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

#Игровой цикл
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))

    display.update()
    clock.tick(FPS)