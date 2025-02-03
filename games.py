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

zombie_sounds = [
    pygame.mixer.Sound("assets/audio/zombie1.wav"),
    pygame.mixer.Sound("assets/audio/zombie2.wav"),
    pygame.mixer.Sound("assets/audio/zombie3.wav"),
]

tittle_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 70)
font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 40)
game_font = pygame.font.Font("assets/images/font/Impacted2.0.ttf", 30)
display_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 25)

zombies = ["zombie1", "zombie2", "zombie3", "zombie4", "zombie5", "zombie6"]

MAX_ZOMBIES = 3

def game_over_music():
    """function to play game over music"""
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/audio/game-over-music.wav')
    pygame.mixer.music.play()

def menu_music():
    """function to play the menu music"""
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/audio/menu-music.wav')
    pygame.mixer.music.play(-1)

def scores_music():
    """function to play scores music"""
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/audio/scores_theme.wav')
    pygame.mixer.music.play(-1)

def game_music():
    """function to play the game music"""
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/audio/game-theme.wav')
    pygame.mixer.music.play(-1)

def load_scores():
    """function to load the scores"""
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_scores(score):
    """function to save the scores"""
    scores = load_scores()
    scores.append({"score": score}) 
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4) 

def show_scores():
    """function to print the scores"""
    scores = load_scores()
    print("\n Meilleurs scores :")
    for i, entry in enumerate(scores[:10], 1):
        print(f"{i}. {entry['nom']} - {entry['score']}")

def draw_text(text, font, color, x, y):
    """function to draw the texts in the game"""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    window.blit(text_surf, text_rect)

def game_over(score):
    """function to switch to game over menu"""
    game_over_music()
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
    """function to run the game"""
    game_music()
    lives = 5
    score = 0
    combo_count = 0
    combo_multiplier = 1
    window.blit(background_image, (0, 0))
    draw_text("Press ECHAP to go back to the MENU", display_font, YELLOW, WINDOW_WIDTH // 2, 15)
    draw_text(f"Score: {score}", game_font, RED, WINDOW_WIDTH // 1.1, 20)
    draw_text(f"Lives: {lives}", game_font, RED, WINDOW_WIDTH // 13.5, 20)
    draw_text(f"Combo: {combo_count}x", game_font, YELLOW, WINDOW_WIDTH // 2, 50)

    zombie_list = []
    eliminated_zombies = 0

    def spawn_zombie(number_of_zombies=1):
        """function to randomly spawn zombies"""
        if len(zombie_list) < MAX_ZOMBIES:
            for _ in range(number_of_zombies):
                random.choice(zombie_sounds).play()
                zombie_image = random.choice(zombies_images)
                zombie_x = random.randint(150, WINDOW_WIDTH - 150)
                
                zombie_max_y = random.randint(0, WINDOW_HEIGHT // 2)
                zombie_y = random.randint(WINDOW_HEIGHT + 50, WINDOW_HEIGHT + 70)
                speed_up = random.uniform(0.1, 0.18)
                speed_down = random.uniform(0.2, 0.24)
                letter = chr(random.randint(65, 90))
                
                zombie_list.append({
                    "image": zombie_image, 
                    "x": zombie_x, 
                    "y": zombie_y, 
                    "max_y": zombie_max_y, 
                    "letter": letter, 
                    "speed_up": speed_up,
                    "speed_down": speed_down, 
                    "direction": "up"
                })

        for sound in zombie_sounds:
            sound.set_volume(0.1)

    def draw_zombies():
        """function to draw zombies"""
        for zombie in zombie_list:
            window.blit(zombie["image"], (zombie["x"], zombie["y"]))
            draw_text(zombie["letter"], game_font, RED, zombie["x"] + 20, zombie["y"] - 10)

    spawn_zombie(random.randint(1, 2))
    
    waiting_input = True
    while waiting_input:
        window.blit(background_image, (0, 0))
        draw_text("Press ECHAP to go back to the MENU", display_font, YELLOW, WINDOW_WIDTH // 2, 15)
        draw_text(f"Score: {score}", game_font, RED, WINDOW_WIDTH // 1.1, 20)
        draw_text(f"Lives: {lives}", game_font, RED, WINDOW_WIDTH // 13.5, 20)
        draw_text(f"Combo: {combo_count}x", game_font, YELLOW, WINDOW_WIDTH // 2, 50)
        draw_zombies()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                else:
                    key_pressed = chr(event.key).upper()
                    zombie_found = False
                    for zombie in zombie_list:
                        if zombie["letter"] == key_pressed:
                            zombie_list.remove(zombie)
                            score += 1
                            eliminated_zombies += 1 
                            combo_count += 1
                            if combo_count > 1:
                                combo_multiplier = combo_count
                            spawn_zombie(random.randint(1, 2)) 
                            zombie_found = True
                            break

                    if not zombie_found:
                        lives -= 1
                        combo_count = 0
                        combo_multiplier = 1
                        if lives == 0:
                            game_over(score)

        if eliminated_zombies == 3:
            score += 5
            eliminated_zombies = 0
        elif eliminated_zombies == 4:
            score += 8
            eliminated_zombies = 0

        for zombie in zombie_list[:]:
            if zombie["direction"] == "up":
                zombie["y"] -= zombie["speed_up"]
                if zombie["y"] < zombie["max_y"]: 
                    zombie["direction"] = "down"
            elif zombie["direction"] == "down":
                zombie["y"] += zombie["speed_down"]
                if zombie["y"] > WINDOW_HEIGHT + 50:
                    zombie_list.remove(zombie)
                    lives -= 1
                    combo_count = 0
                    combo_multiplier = 1
                    if lives == 0:
                        game_over(score)
                    spawn_zombie(random.randint(1, 2))  
                    break

def history():
    """function to run the scores menu"""
    scores_music()
    window.blit(background_image, (0, 0))
    draw_text("SCORE HISTORY", tittle_font, RED, WINDOW_WIDTH // 4, 50)

    scores = load_scores()
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    y_offset = 100
    for i, entry in enumerate(scores[:10]): 
        draw_text(f"{i+1}. Score: {entry['score']}", game_font, RED, WINDOW_WIDTH // 8, y_offset)
        y_offset += 30

    draw_text("Press 'D' to delete history", game_font, YELLOW, WINDOW_WIDTH // 1.3, 50)
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
    """function to print the menu"""
    menu_music()
    window.blit(background_image, (0, 0))
    draw_text("READY FOR ZOMBIE SLICER ?!", tittle_font, RED, WINDOW_WIDTH // 2.4, 50)
    draw_text("Play Game", font, RED, WINDOW_WIDTH // 10, 150)
    draw_text("Score", font, RED, WINDOW_WIDTH // 16, 200)
    draw_text("Quit", font, RED, WINDOW_WIDTH // 18, 250)

    pygame.display.update()

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