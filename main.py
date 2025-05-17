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
    def __init__(self, img, playerx, playery, size, speed, key_up, key_down):
        super().__init__(img, playerx, playery, size, speed)
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
        self.max_speed = speed_x * 4
        self.start_pos = (x, y)
        self.start_speed_x = speed_x
        self.start_speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_x(self, player = None):
        kick_sound.play()
        self.speed_x *= -1
        #Если передали игрока, делаем более реалистичный отскок
        if player:
            #Находим, в какую часть ракетки попал мяч
            player_center = player.rect.y + player.rect.height/2
            ball_center = self.rect.y + self.rect.height/2

            # находим относительную точку удара
            # < 0 = верх ракетки
            # 0 = середина ракетки
            # > 0 = низ ракетки
            relative_kick = (ball_center - player_center) / (player.rect.height/2)            

            # Меняем скорость по Y
            self.speed_y = relative_kick * 5

            #Немного ускоряем мяч при каждом отскоке
            if abs(self.speed_x) < self.max_speed:
                self.speed_x *= 1.1

    def bounce_y(self):
        kick_sound.play()
        self.speed_y *= -1

    def reset_ball(self):
        self.rect.x = self.start_pos[0]
        self.rect.y = self.start_pos[1]
        self.speed_x = self.start_speed_x
        self.speed_y = self.start_speed_y


#Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, color = (73, 200, 73), hover_color=(189, 250, 189), font_size = 24):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font.SysFont("verdana", font_size)
        self.text_image = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def draw(self):
        # Отрисовка основы кнопки
        draw.rect(window, self.current_color, self.rect)
        #Размещение текста в центре кнопки
        window.blit(self.text_image, self.text_rect)
    
    #Метод для проверки наведения мышки на кнопку
    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        else:
            self.current_color = self.color
            return False


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
max_score = 5

#Создание игроков
player_1 = Player(racket_img, 30, 200, (40, 140), 4, K_w, K_s )
player_2 = Player(racket_img, 620, 200, (40, 140), 4, K_UP, K_DOWN)

#Создание мяча
ball_img = "ball.png"
ball = Ball(ball_img, 300, 300, (40, 40), 0, 3, 3)
# Надписи игры
font.init()
my_font = font.SysFont("verdana", 20, bold = True)
endgame_font = font.SysFont("verdana", 40)
win_1 = endgame_font.render("Игрок 1 победил!", True, (0, 180, 60))
win_2 = endgame_font.render("Игрок 2 победил!", True, (0, 180, 60))
goal_font = font.SysFont("verdana", 30)
goal_1 = goal_font.render("Игрок 1 забивает!", True, (0, 0, 255))
goal_2 = goal_font.render("Игрок 2 забивает!", True, (255, 0, 0))

# Звуки игры
mixer.init()
back_sound = "soccer-stadium.mp3"
mixer.music.load(back_sound)
mixer.music.set_volume(0.2) #громкость
mixer.music.play()
kick_sound = mixer.Sound("soccer-kick.ogg")
goal_sound = mixer.Sound("soccer-goal.ogg")

#Гланвое меню
#Кнопки
btn_2_players = Button(win_size[0] // 2 - 150, 150, 300, 50, "2 человека")
btn_vs_ai = Button(win_size[0] // 2 - 150, 250, 300, 50, "Компьютер") 
btn_exit = Button(win_size[0] // 2 - 150, 350, 300, 50, "Выход") 

#Состояние игры
MENU = 0
GAME_2_PLAYERS = 1
GAME_VS_AI = 2
current_mode = MENU

#Функция для сброса игры
def reset_game():
    global score_1, score_2, finish
    score_1 = 0
    score_2 = 0
    finish = False
    ball.reset_ball()

#Игровой цикл
while game:
    for e in event.get():
        #Обработка закрытия окна
        if e.type == QUIT:
            game = False
        
        # Обработка кликов мыши в меню
        if e.type == MOUSEBUTTONDOWN and current_mode == MENU:
            if btn_2_players.check_hover(mouse.get_pos()):
                current_mode = GAME_2_PLAYERS
                reset_game()
            elif btn_vs_ai.check_hover(mouse.get_pos()):
                current_mode = GAME_VS_AI
                reset_game()
            elif btn_exit.check_hover(mouse.get_pos()):
                game = False

    if current_mode == MENU:
        window.blit(background, (0, 0))
        # Обновляем цвет кнопок при наведении мышки
        btn_2_players.check_hover(mouse.get_pos())
        btn_vs_ai.check_hover(mouse.get_pos())
        btn_exit.check_hover(mouse.get_pos())

        #Отрисовываем кнопки
        btn_2_players.draw()
        btn_vs_ai.draw()
        btn_exit.draw()
    elif current_mode == GAME_2_PLAYERS or current_mode == GAME_VS_AI:
        if not finish:
            window.blit(background, (0, 0))
            score_1_text = my_font.render(f"Счёт 1: {score_1}", True, (0, 0 , 0))
            score_2_text = my_font.render(f"Счёт 2: {score_2}", True, (0, 0 , 0))
            window.blit(score_1_text, (10, 15))
            window.blit(score_2_text, (win_size[0]-115, 15))

            # Отскок от верхней и нижней границ
            if ball.rect.y <= 0 :
                #Если мяч ушёл за верхнюю границу - смещаем его вниз
                ball.rect.y = 1
                ball.bounce_y()
            elif ball.rect.y >= win_size[1] - ball.rect.height:
                #Если мяч ушёл за нижнюю границу - смещаем его ввверх
                ball.rect.y = win_size[1] - ball.rect.height - 1
                ball.bounce_y()

            #Отскок от ракетки 1
            if sprite.collide_rect(ball, player_1):
                # Проверяем, с какой стороны произошло столкновение

                #Мяч слева от ракетки - обычный отскок
                if ball.rect.left < player_1.rect.right:
                    ball.rect.left = player_1.rect.right + 1 #Предотвращаем застревание
                    ball.bounce_x(player_1)
                #Мяч попал сверху или снизу
                else:
                    # Попал сверху
                    if ball.rect.centery < player_1.rect.centery:
                        ball.rect.bottom = player_1.rect.top - 1 #Свдигаем вверх
                    #Попал снизу
                    else:
                        ball.rect.bottom = player_1.rect.top + 1 #Свдигаем вниз
                    ball.bounce_y()
            
            # Отскок от ракетки 2
            if sprite.collide_rect(ball, player_2):
                # Проверяем, с какой стороны произошло столкновение

                #Мяч справа от ракетки - обычный отскок
                if ball.rect.right > player_2.rect.left:
                    ball.rect.right = player_2.rect.left + 1 #Предотвращаем застревание
                    ball.bounce_x(player_2)
                #Мяч попал сверху или снизу
                else:
                    # Попал сверху
                    if ball.rect.centery < player_2.rect.centery:
                        ball.rect.bottom = player_2.rect.top - 1 #Свдигаем вверх
                    #Попал снизу
                    else:
                        ball.rect.bottom = player_2.rect.top + 1 #Свдигаем вниз
                    ball.bounce_y()

            #Система гола
            if ball.rect.x < 0:
                goal_sound.play(maxtime=3500)
                finish = True
                score_2 += 1
                if score_2 >= max_score:
                    window.blit(win_2, (180, 200))
                else:
                    window.blit(goal_2, (210, 200))

            if ball.rect.x > win_size[0] - 50:
                goal_sound.play(maxtime=3500)
                finish = True
                score_1 += 1
                if score_1 >= max_score:
                    window.blit(win_1, (180, 200))
                else:
                    window.blit(goal_1, (210, 200))
                

            player_1.update()
            player_2.update()
            ball.update()

            player_1.reset()
            player_2.reset()
            ball.reset()
        else:
            ball.reset_ball()
            if not score_1 >= max_score and not score_2 >= max_score:
                finish = False
                time.delay(3000)

    display.update()
    clock.tick(FPS)