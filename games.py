import pygame
import random
import math

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Slicer")

WHITE = (255, 255, 255)
RED = (209, 10, 10)
YELLOW = (255, 178, 0)
BLACK = (0, 0, 0)

background_image = pygame.image.load("assets/images/backgrounds/game.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

zombies_images = [
    pygame.image.load("assets/images/zombies/zombie1.png"),
    pygame.image.load("assets/images/zombies/zombie2.png"),
    pygame.image.load("assets/images/zombies/zombie3.png"),
    pygame.image.load("assets/images/zombies/zombie4.png")
]
zombies_width = 50
zombies_height = 50

tittle_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 70)
font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 40)
lives = 3
score = 0
zombies = ["zombie1", "zombie2", "zombie3", "zombie4"]
bonus = ["zombie5", "zombie6", "icecube"]

def draw_text(text, font, color, x, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    window.blit(text_surf, text_rect) 

def menu():
    window.blit(background_image, (0, 0))
    draw_text("READY FOR ZOMBIE SLICER ?!",tittle_font, RED, WINDOW_WIDTH // 2.5, 50)
    draw_text("Play Game", font, RED, WINDOW_WIDTH // 10, 150)
    draw_text("Score", font, RED, WINDOW_WIDTH // 16, 200)
    draw_text("Quit", font, RED, WINDOW_WIDTH // 18, 250)

    pygame.display.update()

    waiting_input = True

    while waiting_input :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500:
                    if 130 <= mouse_y <= 170:
                
                        waiting_input = False
                    elif 180 <= mouse_y <= 220:
                        
                        pass
                    elif 230 <= mouse_y <= 270:
                        
                        pygame.quit()
                        exit()
menu()


