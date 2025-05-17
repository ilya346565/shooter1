from pygame import *
from random import randint
from time import time as timer


img_back = "galaxy.jpg"
img_hero = "new2.jpg"
img_hero2 = "new.jpg" 
img_enemy = "ufo.png"
img_bullet = "Bullet.png"
img_ast = 'asteroid.png'
img_pirate = 'new3.jpg'  

win_width = 700
win_height = 500

display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

mixer.init()
mixer.music.load('space (2).mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('Саня лох слитый))', True, (255, 255, 255))
lose = font1.render('Рома лошара тупая))))', True, (180, 0, 0))
font2 = font.SysFont('Arial', 25)

score = 0
lost = 0
max_lost = 5
goal = 20 
life = 3
life2 = 3  

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction = direction  
    
    def update(self):
        self.rect.y -= self.speed * self.direction
        if self.rect.y < 0 or self.rect.y > win_height:
            self.kill()

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, player_num):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.player_num = player_num  
    
    def update(self):
        keys = key.get_pressed()
        if self.player_num == 1:
            if keys[K_LEFT] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < win_width - 80:
                self.rect.x += self.speed
        else:  
            if keys[K_a] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_d] and self.rect.x < win_width - 80:
                self.rect.x += self.speed
    
    def fire(self):
        if self.player_num == 1:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15, 1)
        else:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.bottom, 15, 20, 15, -1)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Pirate(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction = 1  
        self.move_counter = 0
    
    def update(self):
        self.rect.y += self.speed // 2  
        self.rect.x += self.speed * self.direction
        self.move_counter += 1
        
        if self.move_counter > 50:
            self.direction *= -1
            self.move_counter = 0
        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -100
            self.direction = 1
            self.move_counter = 0
            global lost
            lost += 1


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10, 1)
ship2 = Player(img_hero2, win_width - 85, win_height - 100, 80, 100, 10, 2)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_height - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

pirates = sprite.Group()
for i in range(1, 3):  
    pirate = Pirate(img_pirate, randint(80, win_width - 80), -100, 80, 50, randint(2,4))
    pirates.add(pirate)

bullets = sprite.Group()

finish = False
run = True
rel_time = False
rel_time2 = False
num_fire = 0
num_fire2 = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_f:
                if num_fire2 < 5 and rel_time2 == False:
                    num_fire2 += 1
                    fire_sound.play()
                    ship2.fire()
                if num_fire2 >= 5 and rel_time2 == False:
                    last_time2 = timer()
                    rel_time2 = True

    if not finish:
        window.blit(background,(0,0))

        ship.update()
        ship2.update()
        monsters.update()
        asteroids.update()
        pirates.update()
        bullets.update()

        ship.reset()
        ship2.reset()
        monsters.draw(window)
        asteroids.draw(window)
        pirates.draw(window)
        bullets.draw(window)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Идет перезарядка (Игрок 1)', 1, (145, 6, 120))
                window.blit(reload, (200, 460))
            else:
                num_fire = 0
                rel_time = False
                
        if rel_time2 == True:
            now_time2 = timer()
            if now_time2 - last_time2 < 3:
                reload2 = font2.render('Идет перезарядка (Игрок 2)', 1, (145, 6, 120))
                window.blit(reload2, (200, 430))
            else:
                num_fire2 = 0
                rel_time2 = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        pirate_collides = sprite.groupcollide(pirates, bullets, True, True)
        for pc in pirate_collides:
            score += 2  
            pirate = Pirate(img_pirate, randint(80, win_width - 80), -100, 80, 50, randint(2,4))
            pirates.add(pirate)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or sprite.spritecollide(ship, pirates, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            sprite.spritecollide(ship, pirates, True)
            life -= 1
            
        if sprite.spritecollide(ship2, monsters, False) or sprite.spritecollide(ship2, asteroids, False) or sprite.spritecollide(ship2, pirates, False):
            sprite.spritecollide(ship2, monsters, True)
            sprite.spritecollide(ship2, asteroids, True)
            sprite.spritecollide(ship2, pirates, True)
            life2 -= 1

        if lost >= max_lost or (life == 0 and life2 == 0):
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        
        if life == 3:
            life_color = (7, 224, 7)
        elif life == 2:
            life_color = (245, 226, 24)
        else:
            life_color = (189, 6, 6)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (20, 10))
        
        
    
        if life2 == 3:
            life_color2 = (7, 224, 7)
        elif life2 == 2:
            life_color2 = (245, 226, 24)
        else:
            life_color2 = (189, 6, 6)
        text_life2 = font1.render(str(life2), 1, life_color2)
        window.blit(text_life2, (win_width - 50, 10))
            
        display.update()
    else:
        finish = False
        score = 0
        lost = 0 
        num_fire = 0
        num_fire2 = 0
        life = 3
        life2 = 3

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        for p in pirates:
            p.kill()
            
        time.delay(200)

        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_height - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)
            
        for i in range(1, 3):
            pirate = Pirate(img_pirate, randint(80, win_width - 80), -100, 80, 50, randint(2,4))
            pirates.add(pirate)

    time.delay(40)