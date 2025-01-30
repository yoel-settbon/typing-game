import pygame
import random
import json

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

tittle_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 70)
font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 40)
game_font = pygame.font.Font("assets/images/font/Impacted2.0.ttf", 30)
display_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 25)

lives = 5
score = 0
zombies = ["zombie1", "zombie2", "zombie3", "zombie4"]
bonus = ["zombie5", "zombie6", "icecube"]

def draw_text(text, font, color, x, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    window.blit(text_surf, text_rect)

def play_game():
    global lives, score
    window.blit(background_image, (0, 0))
    draw_text("Press ECHAP to go back to the MENU", display_font, RED, WINDOW_WIDTH // 2, 15)
    draw_text(f"Score: {score}", game_font, YELLOW, WINDOW_WIDTH // 1.1, 20)
    draw_text(f"Lives: {lives}", game_font, YELLOW, WINDOW_WIDTH // 11, 20)
    
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                
def history():
        window.blit(background_image, (0, 0))
        draw_text("SCORE HISTORY", tittle_font, RED, WINDOW_WIDTH // 4, 50)

        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                with open("scores.json", "w") as file:
                    json.dump([], file)
                scores = []
        for entry in scores:
            draw_text(f"Score: {entry['score']}", game_font, RED, WINDOW_WIDTH // 6, 100)

        draw_text("Press 'D' to delete history", game_font, YELLOW, WINDOW_WIDTH // 1.3, 40)
        draw_text("Press ECHAP to go back to the MENU", game_font, YELLOW, WINDOW_WIDTH // 2, 470)

        pygame.display.update()

        waiting_input = True
        while waiting_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu()

def menu():
    window.blit(background_image, (0, 0))
    draw_text("READY FOR ZOMBIE SLICER ?!",tittle_font, RED, WINDOW_WIDTH // 2.4, 50)
    draw_text("Play Game", font, RED, WINDOW_WIDTH // 10, 150)
    draw_text("Score", font, RED, WINDOW_WIDTH // 16, 200)
    draw_text("Quit", font, RED, WINDOW_WIDTH // 18, 250)

    pygame.display.update()

    waiting_input = True

    while waiting_input :
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 10 <= mouse_x <= 150 :
                    if 130 <= mouse_y <= 170 :
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif 180 <= mouse_y <= 220 :
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif 230 <= mouse_y <= 270 :
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else : 
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 0 <= mouse_x <= 200:
                    if 130 <= mouse_y <= 170:
                        play_game()
                    elif 180 <= mouse_y <= 220:
                        history()
                    elif 230 <= mouse_y <= 270:
                        
                        pygame.quit()
                        exit()
menu()