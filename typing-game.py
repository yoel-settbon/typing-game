import pygame, sys
import os
import random

player_lives = 5
score = 0
zombies = ['zombie1', 'zombie2', 'zombie3', 'zombie4', 'zombie-bonus', 'zombie-jet-pack', 'ice-cube', 'man', 'woman']

WIDTH = 800
HEIGHT = 500
FPS = 5

pygame.init()
pygame.display.set_caption('Zombie Slicer')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (209, 10, 10)
YELLOW = (255, 178, 0)
BLACK = (0, 0, 0)

background = pygame.image.load('assets/images/backgrounds/game.jpg')
font = pygame.font.Font(os.path.join(os.getcwd(), 'assets/images/font/Poker Nightmare.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
lives_icon = pygame.image.load('assets/images/life/lives.png')

def generate_random_zombies(zombie):
    zombies_path = "assets/images/zombies" + zombie + ".png"
    data[zombie] = {
        'img': pygame.image.load(zombies_path),
        'x' : random.randint(100,500),
        'y' : 800,
        'speed_x': random.randint(-10,10),
        'speed_y': random.randint(-80, -60),
        'throw': False,
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[zombie]['throw'] = True
    else:
        data[zombie]['throw'] = False

data = {}
for zombie in zombies:
    generate_random_zombies(zombie)

def hide_human(x, y):