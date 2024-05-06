from pygame import *
from random import randint
from time import time as timer

#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')
#123
#chelik bude strylyatu
font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 80)


real_timer = timer()

img_back = "background.png"
win= image.load("win.png")
lose= image.load('Loser.png')

img_hero = "verhsteve.png"
img_enemy = "zombieverh.png"
img_asteroid = 'chel.jpg'
lost = 0
kil=0
max_lost = 3
life = 3
player_left = False
player_right = False
player_up = False
player_down = False
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, size_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
            player_left = True
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            player_right = True
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            player_left = True
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            player_right = True

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
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        # картинка стіни - прямокутник потрібних розмірів та кольору
        self.image = Surface((wall_width, wall_height))
        self.image.fill((color_1, color_2, color_3))
        # кожен спрайт повинен зберігати властивість rect - прямокутник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


win_width = 800
win_height = 800
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
w1 = Wall(0, 205, 0, 0, 650, 800, 10)

for i in range(1, 10):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 60, 60, randint(1, 3))
    monsters.add(monster)


run = True
finish = False
reload_time = False
num_fire = 0
clock = time.Clock()
FPS = 30
m=25

while run:
    for e in event.get():
        
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish: ###
            if e.key == K_SPACE:
                if num_fire < 25 and reload_time ==  False:
                    num_fire +=1
                    kil=m-num_fire
                    
                    #fire_sound.play()
                    ship.fire() 
                if num_fire >= 25 and reload_time == False :
                    last_time = timer()
                    reload_time = True


    if not finish: 

        if sprite.spritecollide(ship, monsters, False):  
            sprite.spritecollide(ship, monsters, True)
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 60, 60, randint(1, 3))
            monsters.add(monster)
            life -=3

        if sprite.spritecollide(w1, monsters, False):
            sprite.spritecollide(w1, monsters, True)
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 60, 60, randint(1, 3))
            monsters.add(monster)
            life -=1
        w1.draw_wall()
        window.blit(background, (0, 0))

        text_ammo = font1.render(str(kil)+'/'+str(m),1,(0,200,100))
        window.blit(text_ammo, (610, 50))

        #text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        #window.blit(text_lose, (10, 50))

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
            if now_time - last_time < 2:
                reload = font2.render('Wait for reload', 1, (150,0,0))
                window.blit(reload,(win_width/2-200, win_height-100))
            else:
                num_fire = 0
                reload_time = False
        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 60, 60, randint(1, 3))
            monsters.add(monster)

        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        #if sprite.spritecollide(ship, monsters, False) or lost > max_lost:
         #   finish = True # програли, ставимо тло і більше не керуємо спрайтами.
          #  window.blit(lose, (200, 200))

        

            
        if lost > max_lost or life <= 0:
            finish = True
            window.blit(lose, (0,0))
        # if finish:
        #     win = font1.render("Вітаю з перемогою!",1,(0,255,50))
        #     window.blit(win,(win_width/2-200, win_height-100))
        no_time= timer()

        if no_time-real_timer > 100:
                finish = True
                window.blit(win,(0,0))

        display.update()

    clock.tick(FPS)  
    