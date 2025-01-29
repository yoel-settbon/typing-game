import pygame
import random

pygame.init()

# Window and colors parameters
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Slicer")

WHITE, RED, YELLOW, BLACK = (255, 255, 255), (209, 10, 10), (255, 178, 0), (0, 0, 0)

# Images loads
background_image = pygame.image.load("assets/images/backgrounds/game.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Fonts loads
title_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 70)
font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 40)

# Game variables
lives = 3
score = 0
zombies = ["zombie1", "zombie2", "zombie3", "zombie4"]
bonus = ["zombie5", "zombie6", "icecube"]

# Zombies storage
data = {}

def draw_text(text, font, color, x, y):
    """Function to draw the texts"""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    window.blit(text_surf, text_rect)

def menu():
    """Function to draw the menu"""
    window.blit(background_image, (0, 0))
    draw_text("READY FOR ZOMBIE SLICER ?!", title_font, RED, WINDOW_WIDTH // 2, 50)
    draw_text("Play Game", font, RED, WINDOW_WIDTH // 2, 150)
    draw_text("Score", font, RED, WINDOW_WIDTH // 2, 200)
    draw_text("Quit", font, RED, WINDOW_WIDTH // 2, 250)
    pygame.display.update()

    waiting_input = True
    while waiting_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 250 <= mouse_x <= 550:
                    if 130 <= mouse_y <= 170:
                        waiting_input = False
                    elif 180 <= mouse_y <= 220:
                        pass
                    elif 230 <= mouse_y <= 270:
                        pygame.quit()
                        exit()

def generate_random_zombies(zombie):
    """Function to generate zombies"""
    zombie_path = f"assets/images/zombies/{zombie}.png"
    data[zombie] = {
        'img': pygame.image.load(zombie_path),
        'x': random.randint(100, 500),
        'y': 800,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -60),
        'throw': random.random() >= 0.75,
        't': 0,
        'hit': False,
    }
    print(f"Généré : {zombie} -> {data[zombie]}")  # Vérification console

def draw_zombies():
    """Function to draw zombies"""
    for zombie in data.values():
        if zombie['throw']:
            window.blit(zombie['img'], (int(zombie['x']), int(zombie['y'])))

def update_zombies():
    """Function to update zombies position"""
    for zombie in data.values():
        if zombie['throw']:
            zombie['t'] += 0.1
            zombie['x'] += zombie['speed_x']
            zombie['y'] += (zombie['speed_y'] + (0.5 * 9.81 * (zombie['t'] ** 2)))  # Gravité

# Print the menu before the game
menu()

for zombie in zombies:
    generate_random_zombies(zombie)

pygame.display.update()

# Game loop
running = True
while running:
    window.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_zombies()
    draw_zombies()
    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()