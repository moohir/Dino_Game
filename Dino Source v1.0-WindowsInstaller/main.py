__author__ = "Mihir"

import os
import pickle
import random
import sys

import pygame

pygame.init()

scr_size = (width,height) = (600,150)
FPS = 60
left_speed = 8

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

#Sounds

def read_data(name):
    # If the code is frozen, use this path:
    CurrentPath = os.getenv('APPDATA')
    file = open(os.path.join(CurrentPath, name), 'rb')
    load = pickle.load(file)
    return load

def write_data(name, data):
    # If the code is frozen, use this path:
    CurrentPath = os.getenv('APPDATA')
    file = open(os.path.join(CurrentPath, name), 'wb')
    pickle.dump(data, file)
    file.close()

def get_sound(name):
    # If the code is frozen, use this path:
    if getattr(sys, 'frozen', False):
        CurrentPath = sys._MEIPASS
    # If it's not use the path we're on now
    else:
        CurrentPath = os.path.dirname(__file__)

    # Look for the 'sprites' folder on the path I just gave you:
    spriteFolderPath = os.path.join(CurrentPath, 'assets')
    # From the folder you just opened, load the image file 'some_image.png
    return pygame.mixer.Sound(os.path.join(spriteFolderPath, name))

def get_image(name):
    # If the code is frozen, use this path:
    if getattr(sys, 'frozen', False):
        CurrentPath = sys._MEIPASS
    # If it's not use the path we're on now
    else:
        CurrentPath = os.path.dirname(__file__)

    # Look for the 'sprites' folder on the path I just gave you:
    spriteFolderPath = os.path.join(CurrentPath, 'assets')
    # From the folder you just opened, load the image file 'some_image.png'
    return pygame.image.load(os.path.join(spriteFolderPath, name)).convert_alpha()
    
try:
    hs = read_data("DinoGame\high_score.data")
except:
    write_data("DinoGame\high_score.data", 0)
    hs = 0


str_hs = str(hs)
temp = "0" * (5-len(str_hs))
temp += str_hs
str_hs = temp


hs_img = get_image("hi.png")
hs_img = pygame.transform.scale(hs_img, (19, 10))
g_o = get_image("game_over.png")
replay = get_image("replay_button.png")
g_o = pygame.transform.scale(g_o, (200, 12))
replay = pygame.transform.scale(replay, (36, 30))
g_o_rect = g_o.get_rect()
replay_rect = replay.get_rect()
g_o_rect.center = (300, 50)
replay_rect.center = (300, 85)

jump_sound = get_sound('jump.wav')
die_sound = get_sound('die.wav')
checkPoint_sound = get_sound('checkPoint.wav')

#sprites
class dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.img1 = get_image('dino_1.png')
        self.WIDTH, self.HEIGHT = 44, 48
        self.img1 = pygame.transform.scale(self.img1, (self.WIDTH, self.HEIGHT))

        self.img2 = get_image('dino_2.png')
        self.WIDTH, self.HEIGHT = 44, 48
        self.img2 = pygame.transform.scale(self.img2, (self.WIDTH, self.HEIGHT))

        self.img_jump = get_image('dino_jump.png')
        self.WIDTH, self.HEIGHT = 44, 48
        self.img_jump = pygame.transform.scale(self.img_jump, (self.WIDTH, self.HEIGHT))

        self.img_death = get_image('dino_death.png')
        self.WIDTH, self.HEIGHT = 44, 48
        self.img_death = pygame.transform.scale(self.img_death, (self.WIDTH, self.HEIGHT))

        self.image = self.img1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.img_death)
        self.rect.bottom = 140
        self.rect.left = 50
        self.t = 0
        self.vel = 13
        self.press = False

    def update(self):
        if hit == False:
            pressed = pygame.key.get_pressed()
            if self.rect.bottom == 140:
                self.press = False

            if pressed[pygame.K_SPACE] and self.press == False:
                self.vel = -13
                self.press = True
                jump_sound.play()

            if pressed[pygame.K_UP] and self.press == False:
                self.vel = -13
                self.press = True
                jump_sound.play()

            if self.rect.bottom + self.vel < 140:
                self.rect.bottom += self.vel
                self.vel += 1

            else:
                self.rect.bottom = 140

            if self.vel == 13:
                self.t +=1
                if self.t == 4:
                    tempx = self.rect.x
                    tempy = self.rect.y
                    if self.image == self.img1:
                        self.image = self.img2
                    else:
                        self.image = self.img1
                    self.rect = self.image.get_rect()
                    self.rect.x, self.rect.y = tempx, tempy
                    self.t = 0
            else:
                self.image = self.img_jump

        else:
            tempx = self.rect.bottom
            tempy = self.rect.right
            self.image  = self.img_death
            self.rect = self.image.get_rect()
            self.rect.bottom, self.rect.right = tempx, tempy

        self.mask = pygame.mask.from_surface(self.img_death)

class ground():
    def __init__(self):
        self.img1 = get_image('ground.png')
        self.img2 = get_image('ground.png')

        self.rect1 = self.img1.get_rect()
        self.rect2 = self.img2.get_rect()

        self.rect1.bottom = 150
        self.rect1.left = 0

        self.rect2.bottom = 150
        self.rect2.left = int(self.rect1.right -5)



    def draw(self):
        screen.blit(self.img1, self.rect1)
        screen.blit(self.img2, self.rect2)

    def update(self):
        if hit == False:
            if self.rect1.right <= 0:
                self.rect1.left = int(self.rect2.right -5)

            if self.rect2.right <= 0:
                self.rect2.left = int(self.rect1.right -5)

            self.rect1.right -= left_speed
            self.rect2.right -= left_speed

class cactus(pygame.sprite.Sprite):
    def __init__(self, type, number):
        pygame.sprite.Sprite.__init__(self)
        self.one_small = get_image('cactus-1s.png')
        self.two_small = get_image('cactus-2s.png')
        self.three_small = get_image('cactus-3s.png')
        self.one_big = get_image('cactus-1b.png')
        self.two_big = get_image('cactus-2b.png')
        self.three_big = get_image('cactus-3b.png')
        self.four_big = get_image('cactus-4b.png')

        self.img_list = ["o_s", "t_s", "th_s", "o_b", "o_b", "t_b", "th_b", "f_b"]

        self.number = number

        if type == "o_s":
            self.one_small = pygame.transform.scale(self.one_small, (17, 35))
            self.image = self.one_small

        elif type == "t_s":
            self.two_small = pygame.transform.scale(self.two_small, (40, 40))
            self.image = self.two_small

        elif type == "th_s":
            self.three_small = pygame.transform.scale(self.three_small, (58, 43))
            self.image = self.three_small

        elif type == "o_b":
            self.one_big = pygame.transform.scale(self.one_big, (24, 53))
            self.image = self.one_big

        elif type == "t_b":
            self.two_big = pygame.transform.scale(self.two_big, (53, 55))
            self.image = self.two_big

        elif type == "th_b":
            self.three_big = pygame.transform.scale(self.three_big, (51, 53))
            self.image = self.three_big

        elif type == "f_b":
            self.four_big = pygame.transform.scale(self.four_big, (75, 53))
            self.image = self.four_big

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (600, 145)

    def change_img(self, type, temp):
        if type == "o_s":
            self.one_small = pygame.transform.scale(self.one_small, (17, 35))
            self.image = self.one_small

        elif type == "t_s":
            self.two_small = pygame.transform.scale(self.two_small, (40, 40))
            self.image = self.two_small

        elif type == "th_s":
            self.three_small = pygame.transform.scale(self.three_small, (58, 43))
            self.image = self.three_small

        elif type == "o_b":
            self.one_big = pygame.transform.scale(self.one_big, (24, 53))
            self.image = self.one_big

        elif type == "t_b":
            self.two_big = pygame.transform.scale(self.two_big, (53, 55))
            self.image = self.two_big

        elif type == "th_b":
            self.three_big = pygame.transform.scale(self.three_big, (51, 53))
            self.image = self.three_big

        elif type == "f_b":
            self.four_big = pygame.transform.scale(self.four_big, (75, 53))
            self.image = self.four_big

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = temp

    def update(self):
        if hit == False:
            if self.rect.right <= 0:
                self.rect.left = 1200 + random.randint(-200, 200)

                if self.number == 1 and self.rect.left - enemy_2.rect.left < 400:
                    self.rect.left = enemy_2.rect.left + 600

                if self.number == 1 and self.rect.left - enemy_2.rect.left > 600:
                    self.rect.left = enemy_2.rect.left + 600

                self.change_img(self.img_list[random.randint(0, 7)], self.rect.bottomleft)


            self.rect.left -= left_speed
            self.mask = pygame.mask.from_surface(self.image)

class number(pygame.sprite.Sprite):
    def __init__(self, place, num, is_hs = False):
        pygame.sprite.Sprite.__init__(self)

        self.place = place
        self.hs = is_hs

        self.img0 = get_image('0.png')
        self.img1 = get_image('1.png')
        self.img2 = get_image('2.png')
        self.img3 = get_image('3.png')
        self.img4 = get_image('4.png')
        self.img5 = get_image('5.png')
        self.img6 = get_image('6.png')
        self.img7 = get_image('7.png')
        self.img8 = get_image('8.png')
        self.img9 = get_image('9.png')

        if num == 0:    self.image = self.img0
        if num == 1:    self.image = self.img1
        if num == 2:    self.image = self.img2
        if num == 3:    self.image = self.img3
        if num == 4:    self.image = self.img4
        if num == 5:    self.image = self.img5
        if num == 6:    self.image = self.img6
        if num == 7:    self.image = self.img7
        if num == 8:    self.image = self.img8
        if num == 9:    self.image = self.img9

        if is_hs == False:
            if place == 1: cords = (592 - place * 12, 20)
            if place == 2: cords = (592 - place * 12, 20)
            if place == 3: cords = (592 - place * 12, 20)
            if place == 4: cords = (592 - place * 12, 20)
            if place == 5: cords = (592 - place * 12, 20)

        else:
            if place == 1: cords = (40 + place * 12, 20)
            if place == 2: cords = (40 + place * 12, 20)
            if place == 3: cords = (40 + place * 12, 20)
            if place == 4: cords = (40 + place * 12, 20)
            if place == 5: cords = (40 + place * 12, 20)

        self.image = pygame.transform.scale(self.image, (9, 10))
        self.rect = self.image.get_rect()
        self.rect.bottomright = cords
        self.cords = cords

    def update(self):
        if self.hs == False:
            value = self.place
            value = 5 - value
            num = int(str_score[value])

            if num == 0:    self.image = self.img0
            if num == 1:    self.image = self.img1
            if num == 2:    self.image = self.img2
            if num == 3:    self.image = self.img3
            if num == 4:    self.image = self.img4
            if num == 5:    self.image = self.img5
            if num == 6:    self.image = self.img6
            if num == 7:    self.image = self.img7
            if num == 8:    self.image = self.img8

            self.image = pygame.transform.scale(self.image, (9, 10))
            self.rect = self.image.get_rect()
            self.rect.bottomright = self.cords

    def updatehs(self):
        str_hs = str(hs)
        temp = "0" * (5-len(str_hs))
        temp += str_hs
        str_hs = temp
        num = int(str_hs[self.place - 1])

        if num == 0:    self.image = self.img0
        if num == 1:    self.image = self.img1
        if num == 2:    self.image = self.img2
        if num == 3:    self.image = self.img3
        if num == 4:    self.image = self.img4
        if num == 5:    self.image = self.img5
        if num == 6:    self.image = self.img6
        if num == 7:    self.image = self.img7
        if num == 8:    self.image = self.img8

        self.image = pygame.transform.scale(self.image, (9, 10))
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.cords


all_sprites = pygame.sprite.Group()
dino = dino()
ground = ground()
enemy_1 = cactus("o_b", 1)
enemy_2 = cactus("f_b", 2)
enemy_2.rect.left = 1200

#score
one = number(1, 0)
two = number(2, 0)
three = number(3, 0)
four = number(4, 0)
five = number(5, 0)

hone = number(1, int(str_hs[0]), is_hs = True)
htwo = number(2, int(str_hs[1]), is_hs = True)
hthree = number(3, int(str_hs[2]), is_hs = True)
hfour = number(4, int(str_hs[3]), is_hs = True)
hfive = number(5, int(str_hs[4]), is_hs = True)


all_sprites.add(enemy_1)
all_sprites.add(enemy_2)
all_sprites.add(one)
all_sprites.add(two)
all_sprites.add(three)
all_sprites.add(four)
all_sprites.add(five)

all_sprites.add(hone)
all_sprites.add(htwo)
all_sprites.add(hthree)
all_sprites.add(hfour)
all_sprites.add(hfive)

all_sprites.add(dino)

running = True
hit = False
d_sound = 0
score = 000000
str_score = "00000"
score_check = 0
restart = 0
kpress = False

while running:
    screen.fill(WHITE)
    # keep loop running at the right speed
    clock.tick(60)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    ground.update()
    if pygame.sprite.collide_mask(dino, enemy_1) != None or pygame.sprite.collide_mask(dino, enemy_2) != None:
        hit = True

        if d_sound == 0:
            pygame.mixer.music.stop()
            die_sound.play()
            write_data("DinoGame\high_score.data", hs)
            d_sound = 1




    all_sprites.draw(screen)
    ground.draw()
    screen.blit(hs_img, (10 ,10))

    if hit == False and score_check ==  6:
        if str_score[4] == "0" and str_score[3] == "0" and str_score != "00000":
            pygame.mixer.music.stop()
            checkPoint_sound.play()
            left_speed += 1
        score += 1
        str_score = str(score)
        temp = "0" * (5-len(str_score))
        temp += str_score
        str_score = temp
        score_check = 0

    if score >= hs:
        hs = score

    ## DEBUG:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_d]:
        pygame.draw.rect(screen, (255, 0, 0), dino.rect, 2)
        pygame.draw.rect(screen, (255, 0, 0), enemy_1.rect, 2)
        pygame.display.set_caption("Fps: " + str(clock.get_fps()))
        hit_check = False
    else:
        pygame.display.set_caption("Dino Game")

    if hit == True:
        hone.updatehs()
        htwo.updatehs()
        hthree.updatehs()
        hfour.updatehs()
        hfive.updatehs()

        screen.blit(g_o, g_o_rect)
        screen.blit(replay, replay_rect)
        restart += 1
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] or pressed[pygame.K_UP]: kpress = True
        if restart >= 50 and kpress == True:
            dino.image = dino.img1
            enemy_1.rect.bottomleft = (1000, 145)
            enemy_2.rect.bottomleft = (1600, 145)
            hit = False
            d_sound = 0
            score = 000000
            str_score = "00000"
            score_check = 0
            restart = 0
            kpress = False
            left_speed = 8



    score_check += 1
    pygame.display.flip()
    pygame.display.update()
