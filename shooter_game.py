#Создай собственный Шутер!
from random import *
from pygame import *
from time import time as timer

rel_time = False
num_fire = 0

score = 0
goal = 10
lost = 0
max_lost = 3

font.init()
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("shoter")
background = transform.scale(image.load("galaxy.jpg"),(win_width, win_height))
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
bullets = sprite.Group()
text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
window.blit(text, (10, 20))



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (40, 40))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        self.rect.y > win_height
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0 
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1, 2))
    monsters.add(monster)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
a = 50
b = 650
player = Player('rocket.png', randint(a, b), 400, 3)
fire_sound = mixer.Sound('fire.ogg')

game = True
finish = False
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:               

                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                            

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        player.reset()
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        player.update()
        monsters.update()
        bullets.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reolad = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reolad, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, randint(1, 5))
            monsters.add(monster)
    if sprite.spritecollide(player, monsters, False)  or lost >= max_lost:
        finish = True
        window.blit(lose, (200, 200))

    if score >= goal:
        finish = True
        window.blit(win, (200, 200))
    display.update()
    time.delay(40)