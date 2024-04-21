from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#123


font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "background.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.jpg"
img_asteroid = 'chel.jpg'
score = 0
lost = 0
goal = 10
max_lost = 3
life = 3
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

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
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0
            lost +=1


class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()


for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)


run = True
finish = False
reload_time = False
num_fire = 0
clock = time.Clock()
FPS = 30

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish: ###
            if e.key == K_SPACE:
                if num_fire < 10 and reload_time ==  False:
                    num_fire +=1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 10 and reload_time == False :
                    last_time = timer()
                    reload_time = True

    if not finish:
        window.blit(background, (0, 0))

        text = font1.render("Рахунок: " + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))
        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)


        if reload_time == True:
            now_time = timer()
            if now_time - reload_time > 2:
                reload = font2.render('Wait for reload', 1, (150,0,0))
                window.blit(reload,(win_width/2-200, win_height-100))
            else:
                num_fire = 0
                reload_time = 0

        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)


        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        #if sprite.spritecollide(ship, monsters, False) or lost > max_lost:
         #   finish = True # програли, ставимо тло і більше не керуємо спрайтами.
          #  window.blit(lose, (200, 200))

        if sprite.spritecollide(ship, monsters, False):  
            sprite.spritecollide(ship, monsters, True)
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)
            life -=1

            
        if lost > max_lost or life == 0:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()

    clock.tick(FPS)