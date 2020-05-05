import pygame
from random import randint
from random import random
from random import shuffle



class Player(object):
    player_ship = pygame.image.load('ship.png')
    player_ship_dead = pygame.image.load('boom.png')
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.health = 3

    def draw(self, win):
        win.blit(self.player_ship, (self.x, self.y))

    def dead(self, win):
        win.blit(self.player_ship_dead, (self.x, self.y-10))

class Enemy(object):
    enemy = pygame.image.load('enemy.png')
    enemy_red = pygame.image.load('enemy_red.png')
    enemy_dead = pygame.image.load('boom.png')
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.widht = 50
        self.height = 42

        self.is_dead = False
        self.dead_time = 0

        self.is_red = False

    def draw(self, win):
        win.blit(self.enemy, (self.x, self.y))

    def draw_red(self, win):
        win.blit(self.enemy_red, (self.x, self.y))

    def dead(self, bullet_x, bullet_y):
        if (self.x < bullet_x < (self.x + self.widht)) and (self.y < bullet_y < (self.y + self.height)) and self.is_dead == False:
            self.is_dead = True
            return True
        else:
            return False

    def dead_red(self, bullet_x, bullet_y):
        if (self.x < bullet_x < (self.x + self.widht)) and (self.y < bullet_y < (self.y + self.height)) and self.is_dead == False:
            if self.is_red == False:
                self.is_dead = True
            self.is_red = False
            return True
        else:
            return False

class Projectile(object):
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Interface(object):
    heart = pygame.image.load('heart.png')
    def __init__(self, widht_win):
        self.widht_win = widht_win

    def draw_hearts(self, win, healths):
        for i in range(0, healths + 1):
            win.blit(self.heart, (widht_win - 40*i, 10))


def new_game():
    global level
    global bullets
    bullets = []

    global enemies_bullets
    enemies_bullets = []

    global dead_enemy
    dead_enemy = set()

    global lose
    global score
    global len_dead_enemy

    global player
    global velocity_enemies_bullets
    len_dead_enemy = 0

    if lose == True:
        score = 0
        velocity_enemies_bullets = 5
        level = 1
        player.health = 3
    elif score == 0:
        level = 1
    else:
        level = int(level) + 1
        if player.health == 7:
            player.health = 7
        else:
            player.health += 1
        velocity_enemies_bullets += level

    #спуан мобов
    global count_enemies

    count_enemies = 48 # 10; 19; 29; 38...
    x_enemy = 30
    y_enemy = 50
    global enemies
    enemies = []
    for enemy in range(count_enemies):
        if (x_enemy == 600):
            x_enemy = 30
            y_enemy += 50
        elif (x_enemy == 630):
            x_enemy = 60
            y_enemy += 50
        enemies.append(Enemy(x_enemy, y_enemy))
        x_enemy += 60

    #спаун красных мобов
    enemies_list = list(range(count_enemies))
    if level > 1:
        shuffle(enemies_list)
        for i in range(0, level):
            enemies[enemies_list[i]].is_red = True
    else:
        red_enemy_is = randint(0, count_enemies - 1)
        enemies[red_enemy_is].is_red = True



pygame.init()

widht_win = 640
height_win = 480
win = pygame.display.set_mode((widht_win, height_win))
pygame.display.set_caption("Space Invaders")

score = 0
space = 0

font_main = pygame.font.Font('digital-7.ttf', 72)
font_point = pygame.font.Font('digital-7.ttf', 20)
font_instruction = pygame.font.Font('digital-7 (italic).ttf', 24)
font_total_points = pygame.font.Font('digital-7 (italic).ttf', 34)
you_win = font_main.render("YOU WIN", 1, (0, 255, 0))
you_lose = font_main.render("YOU LOSE", 1, (255, 0, 0))
your_points = font_point.render(str(score), 1, (255, 255, 255))
instruction_st = font_instruction.render("Press UP to START the game", 2, (255, 255, 255))
instruction_con = font_instruction.render("Press UP to CONTINUE the game", 1, (255, 255, 255))
instruction_con_life = font_instruction.render("You GET plus one LIFE", 1, (255, 255, 255))
instruction_res = font_instruction.render("Press UP to RESTART the game", 1, (255, 255, 255))
instruction_control = font_instruction.render("Control: fire - SPACE, move - left/right", 1, (255, 255, 255))


first_game = True
start = False
lose = False

k = 0
l = 0

player = Player((widht_win / 2 - 25), (height_win - 100), 10)
inter = Interface(widht_win)

velocity_enemies_bullets = 5
level = 0
new_game()

run = True
while run:
    pygame.time.delay(33)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y > 0 and bullet.y < height_win:
            bullet.y -= bullet.velocity
            for enemy in enemies:
                if enemy.is_red:
                    if enemy.dead_red(bullet.x, bullet.y):
                        bullets.pop(bullets.index(bullet))
                elif enemy.dead(bullet.x, bullet.y):
                    bullets.pop(bullets.index(bullet))
        else:
            bullets.pop(bullets.index(bullet))

    for en_bullet in enemies_bullets:
        if en_bullet.y > 0 and en_bullet.y < height_win:
            en_bullet.y += en_bullet.velocity
        else:
            enemies_bullets.pop(enemies_bullets.index(en_bullet))

    if len(enemies_bullets) < 3 and start == True:
        number_enemy = randint(0, count_enemies - 1)
        while enemies[number_enemy].is_dead and len(dead_enemy) < count_enemies:
            number_enemy = randint(0, count_enemies - 1)
        enemies_bullets.append(Projectile(int(enemies[number_enemy].x + 25), int(enemies[number_enemy].y + 30), 5, (200,0,0), velocity_enemies_bullets))

    keys = pygame.key.get_pressed()
    if first_game == False and lose == False:
        if keys[pygame.K_SPACE] and lose == False:
            if space > 999:
                bullets.append(Projectile(int(player.x+25), int(player.y), 6, (0,0,255), 20))
            space = 1
        space += 333

        if keys[pygame.K_LEFT] and player.x > 5 and lose == False:
            player.x -= player.velocity
        if keys[pygame.K_RIGHT] and player.x < widht_win - 50 - 5 and lose == False:
            player.x += player.velocity


    win.fill((0,0,0))
    for i in range(100):
        win.fill(pygame.Color('white'), (random() * widht_win, random() * height_win, 1, 1))

    k = k + 1
    l = l + ((k % 4) % 3) % 2
    for enemy in enemies:
        if enemy.is_dead:
            if enemy.dead_time < 1000:
                win.blit(enemy.enemy_dead, (enemy.x, enemy.y))
                enemy.dead_time += 66
            dead_enemy.add(enemy)
            if len_dead_enemy < len(dead_enemy):
                score += 100
            len_dead_enemy = len(dead_enemy)
        else:
            if k % 4 == 1:
                if (0 <= enemies.index(enemy) <= 9) or (18 < enemies.index(enemy) <= 28) or (37 < enemies.index(enemy) <= 47):
                    if l % 8 > 3:
                        enemy.x += 10
                    elif l % 8 <= 3:
                        enemy.x -= 10
                if (9 < enemies.index(enemy) <= 18) or (28 < enemies.index(enemy) <= 37):
                    if l % 8 > 3:
                        enemy.x -= 10
                    elif l % 8 <= 3:
                        enemy.x += 10
            if enemy.is_red == True:
                enemy.draw_red(win)
            else:
                enemy.draw(win)

    for bullet in bullets:
        bullet.draw(win)
    for en_bullet in enemies_bullets:
        en_bullet.draw(win)

    your_points = font_point.render(str(score), 1, (255, 255, 255))
    win.blit(your_points, (10, 10))
    your_level = font_point.render("Level: " + str(level), 1, (255, 255, 255))
    win.blit(your_level, (widht_win/2 - 25, 10))
    inter.draw_hearts(win, player.health)

    player.draw(win)
    for en_bullet in enemies_bullets:
        if (player.x < en_bullet.x < player.x + 50) and (player.y < en_bullet.y < player.y + 50):
            player.health -= 1
            if player.health == 0:
                lose = True
            else:
                enemies_bullets.pop(enemies_bullets.index(en_bullet))

    if len(dead_enemy) == count_enemies:
        win.blit(you_win, (220, 200))
        win.blit(instruction_con, (180, 280))
        win.blit(instruction_con_life, (215, 310))
        start = False
        if keys[pygame.K_UP]:
            new_game()

    elif lose:
        win.blit(you_lose, (200, 200))
        win.blit(instruction_res, (180, 280))
        total_points = font_total_points.render("SCORE: " + str(score), 1, (255, 255, 255))
        win.blit(total_points, (245, 320))
        player.dead(win)
        start = False
        if keys[pygame.K_UP]:
            new_game()
            win.blit(your_points, (10, 10))
            lose = False
    if first_game == True:
        win.blit(instruction_st, (190, 310))
        win.blit(instruction_control, (140, 340))
    if keys[pygame.K_UP]:
        first_game = False
        start = True
    pygame.display.update()

pygame.quit()
