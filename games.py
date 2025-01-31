import pygame
import random
import json
import os

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Slicer")

WHITE = (255, 255, 255)
RED = (209, 10, 10)
YELLOW = (255, 178, 0)
BLACK = (0, 0, 0)

SCORES_FILE = "scores.json"

background_image = pygame.image.load("assets/images/backgrounds/game.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

zombies_images = [
    pygame.image.load("assets/images/zombies/zombie1.png"),
    pygame.image.load("assets/images/zombies/zombie2.png"),
    pygame.image.load("assets/images/zombies/zombie3.png"),
    pygame.image.load("assets/images/zombies/zombie4.png"),
    pygame.image.load("assets/images/zombies/zombie-bonus.png"),
    pygame.image.load("assets/images/zombies/zombie-jet-pack.png")
]

tittle_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 70)
font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 40)
game_font = pygame.font.Font("assets/images/font/Impacted2.0.ttf", 30)
display_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 25)

FPS = 20
zombies = ["zombie1", "zombie2", "zombie3", "zombie4", "zombie5", "zombie6"]
bonus = ["icecube"]

def menu_music():
    pygame.mixer.music.stop
    pygame.mixer.music.load('assets/audio/menu-theme.wav')
    pygame.mixer.music.play(-1)

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_scores(score):
    scores = load_scores()
    scores.append({"score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4)

def show_scores():
    scores = load_scores()
    print("\n Meilleurs scores :")
    for i, entry in enumerate(scores[:10], 1):
        print(f"{i}. {entry['nom']} - {entry['score']}")


def draw_text(text, font, color, x, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    window.blit(text_surf, text_rect)

def game_over(score):
    save_scores(score)

    window.fill(BLACK)
    draw_text("GAME OVER...LOSER", tittle_font, RED, WINDOW_WIDTH // 2, 150)
    draw_text("Press ENTER to retry", game_font, YELLOW, WINDOW_WIDTH // 2, 250)
    draw_text("Press ECHAP to go back to MENU", game_font, YELLOW, WINDOW_WIDTH // 2, 300)
    draw_text("Press SPACE to see the SCORE", game_font, YELLOW, WINDOW_WIDTH // 2, 350)
    pygame.display.update()
    
    waiting_input = True
    while waiting_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_game()
                elif event.key == pygame.K_ESCAPE:
                    menu()
                elif event.key == pygame.K_SPACE:
                    history()


def play_game():
    lives = 5
    score = 0
    window.blit(background_image, (0, 0))
    draw_text("Press ECHAP to go back to the MENU", display_font, YELLOW, WINDOW_WIDTH // 2, 15)
    draw_text(f"Score: {score}", game_font, RED, WINDOW_WIDTH // 1.1, 20)
    draw_text(f"Lives: {lives}", game_font, RED, WINDOW_WIDTH // 13.5, 20)
    
    zombie_list = []

    def spawn_zombie():
        zombie_image = random.choice(zombies_images)
        zombie_x = random.randint(150, WINDOW_WIDTH - 150)
        zombie_y = random.randint(WINDOW_HEIGHT + 50, WINDOW_HEIGHT + 70)
        speed_up = random.uniform(0.1, 0.18)
        speed_down = random.uniform(0.19, 0.27)
        letter = chr(random.randint(65, 90))
        zombie_list.append({
            "image": zombie_image, 
            "x": zombie_x, 
            "y": zombie_y, 
            "letter": letter, 
            "speed_up": speed_up,
            "speed_down": speed_down, 
            "direction": "up"
        })

    def draw_zombies():
        for zombie in zombie_list:
            window.blit(zombie["image"], (zombie["x"], zombie["y"]))
            draw_text(zombie["letter"], game_font, RED, zombie["x"] + 20, zombie["y"] - 10)

    spawn_zombie()
    waiting_input = True
    while waiting_input:
        window.blit(background_image, (0, 0))
        draw_text("Press ECHAP to go back to the MENU", display_font, YELLOW, WINDOW_WIDTH // 2, 15)
        draw_text(f"Score: {score}", game_font, RED, WINDOW_WIDTH // 1.1, 20)
        draw_text(f"Lives: {lives}", game_font, RED, WINDOW_WIDTH // 13.5, 20)
        draw_zombies()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                else:
                    key_pressed = chr(event.key).upper()
                    for zombie in zombie_list:
                        if zombie["letter"] == key_pressed:
                            zombie_list.remove(zombie)
                            score += 1
                            spawn_zombie()
                            break
                    else:
                        lives -= 1
                        if lives == 0:
                            game_over(score)

        for zombie in zombie_list[:]:
            if zombie["direction"] == "up":
                zombie["y"] -= zombie["speed_up"] 
                if zombie["y"] < WINDOW_HEIGHT // 4:
                    zombie["direction"] = "down"  
            elif zombie["direction"] == "down":
                zombie["y"] += zombie["speed_down"]
                if zombie["y"] > WINDOW_HEIGHT + 50:
                    zombie_list.remove(zombie)
                    lives -= 1
                    if lives == 0:
                        game_over()
                    spawn_zombie()
                    break

    try:
        with open("scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    scores.append({"score": score})

    with open("scores.json", "w") as file:
        json.dump(scores, file)
    
    pygame.display.update()

def history():
    window.blit(background_image, (0, 0))
    draw_text("SCORE HISTORY", tittle_font, RED, WINDOW_WIDTH // 2, 50)

    scores = load_scores()
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    y_offset = 120
    for i, entry in enumerate(scores[:10]):
        draw_text(f"{i+1}. Score: {entry['score']}", game_font, RED, WINDOW_WIDTH // 2, y_offset)
        y_offset += 40

    draw_text("Press 'D' to delete history", game_font, YELLOW, WINDOW_WIDTH // 2, 450)
    draw_text("Press ECHAP to go back to the MENU", display_font, YELLOW, WINDOW_WIDTH // 2, 470)

    pygame.display.update()

    waiting_input = True
    while waiting_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                elif event.key == pygame.K_d:
                    with open(SCORES_FILE, "w") as file:
                        json.dump([], file)
                    history()


def menu():
    window.blit(background_image, (0, 0))
    draw_text("READY FOR ZOMBIE SLICER ?!", tittle_font, RED, WINDOW_WIDTH // 2.4, 50)
    draw_text("Play Game", font, RED, WINDOW_WIDTH // 10, 150)
    draw_text("Score", font, RED, WINDOW_WIDTH // 16, 200)
    draw_text("Quit", font, RED, WINDOW_WIDTH // 18, 250)

    pygame.display.update()
    menu_music()

    waiting_input = True

    while waiting_input:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 10 <= mouse_x <= 150:
                    if 130 <= mouse_y <= 170:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif 180 <= mouse_y <= 220:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    elif 230 <= mouse_y <= 270:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else: 
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