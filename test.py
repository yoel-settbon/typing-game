import pygame
import random
import time

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Slicer")
FPS = 30
WHITE = (255, 255, 255)
RED = (209, 10, 10)
YELLOW = (255, 178, 0)
BLACK = (0, 0, 0)

background_image = pygame.image.load("assets/images/backgrounds/game.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()
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
game_font = pygame.font.Font("assets/images/font/Impacted2.0.ttf", 30)

lives = 5
score = 0
zombies = ["zombie1", "zombie2", "zombie3", "zombie4"]
bonus = ["zombie5", "zombie6", "icecube"]

def draw_text(text, font, color, x, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    window.blit(text_surf, text_rect)

def generate_zombies(zombies):
    zombies_path = "images/" + zombies + ".png"
    data[zombies] = {
        'img': pygame.image.load(zombies_path),
        'x' : random.randint(100,500),          #where the zombies should be positioned on x-coordinate
        'y' : 800,
        'speed_x': random.randint(-10,10),      #how fast the zombies should move in x direction. Controls the diagonal movement of zombiess
        'speed_y': random.randint(-80, -60),    #control the speed of zombiess in y-directionn ( UP )
        'throw': False,                         #determines if the generated coordinate of the zombiess is outside the window or not. If outside, then it will be discarded
        't': 0,                                 #manages the
        'hit': False,
    }

    if random.random() >= 0.75:     #Return the next random floating point number in the range [0.0, 1.0) to keep the zombiess inside the window
        data[zombies]['throw'] = True
    else:
        data[zombies]['throw'] = False

# Dictionary to hold the data the random zombies generation
data = {}
for zombies in zombies:
    generate_zombies(zombies)

def hide_cross_lives(x, y):
    window.blit(pygame.image.load("images/red_lives.png"), (x, y))

# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    window.blit(text_surface, text_rect)

# draw players lives
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
        img_rect.x = int(x + 35 * i)    #sets the next cross icon 35pixels awt from the previous one
        img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from top of the screen
        display.blit(img, img_rect)

# show game over display & front display
def show_gameover_screen():
    window.blit(background_image, (0,0))
    draw_text(window, "zombies NINJA!", 90, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
    if not game_over :
        draw_text(window,"Score : " + str(score), 50, WINDOW_WIDTH / 2, WINDOW_HEIGHT /2)

    draw_text(window, "Press a key to begin!", 64, WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Game Loop
first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))

while game_running :
    if game_over :
        if first_round :
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(window, 690, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False

    window.blit(background_image, (0, 0))
    window.blit(score_text, (0, 0))
    draw_lives(window, 690, 5, player_lives, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']          #moving the zombiess in x-coordinates
            value['y'] += value['speed_y']          #moving the zombiess in y-coordinate
            value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
            value['t'] += 1                         #increasing speed_y for next loop

            if value['y'] <= 800:
                window.blit(value['img'], (value['x'], value['y']))    #displaying the zombies inside screen dynamically
            else:
                generate_zombies(key)

            current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)
                    #if the user clicks bombs for three time, GAME OVER message should be displayed and the window should be reset
                    if player_lives < 0 :
                        show_gameover_screen()
                        game_over = True

                    half_zombies_path = "images/explosion.png"
                else:
                    half_zombies_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_zombies_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_zombies(key)

    pygame.display.update()
    clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec
                        

pygame.quit()