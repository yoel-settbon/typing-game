import pygame
import random

pygame.init()

# Définition de la fenêtre
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Slicer")

WHITE, RED = (255, 255, 255), (209, 10, 10)

# Chargement des images
background_image = pygame.image.load("assets/images/backgrounds/game.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Chargement des polices
title_font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 70)
font = pygame.font.Font("assets/images/font/Poker Nightmare.ttf", 40)

# Liste des zombies possibles
zombies = ["zombie1", "zombie2", "zombie3", "zombie4"]
active_zombies = []  # Liste des zombies en vol

DEBUG_MODE = True  # Active l'affichage des coordonnées

# Fonction pour afficher du texte
def draw_text(text, font, color, x, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    window.blit(text_surf, text_rect)

# Fonction pour afficher le menu
def menu():
    window.blit(background_image, (0, 0))
    draw_text("READY FOR ZOMBIE SLICER ?!", title_font, RED, WINDOW_WIDTH // 2, 50)
    draw_text("Play Game", font, RED, WINDOW_WIDTH // 2, 150)
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
                    elif 230 <= mouse_y <= 270:
                        pygame.quit()
                        exit()

# Fonction pour générer un zombie
def generate_random_zombie():
    zombie_name = random.choice(zombies)
    zombie_path = f"assets/images/zombies/{zombie_name}.png"
    
    # Charger l'image du zombie
    zombie_img = pygame.image.load(zombie_path).convert_alpha()
    
    # Définir un facteur d'échelle (par exemple, 0.5 pour réduire la taille de moitié)
    scale_factor = 0.090
    zombie_img = pygame.transform.scale(zombie_img, (int(zombie_img.get_width() * scale_factor), int(zombie_img.get_height() * scale_factor)))
    
    # Créer le zombie avec la taille réduite
    new_zombie = {
        'img': zombie_img,
        'x': random.randint(200, 600),  # Position X aléatoire
        'y': WINDOW_HEIGHT - 100,  # Commence un peu au-dessus du bas de l'écran
        'speed_x': random.randint(-0, 0),  # Déplacement léger sur X
        'speed_y': random.randint(-50, -50),  # Vitesse initiale pour le lancé
        't': 0,  # Temps pour la trajectoire parabolique
        'throw': True,  # Active le mouvement
    }
    
    active_zombies.append(new_zombie)
    print(f"🧟‍♂️ Nouveau zombie généré : {zombie_name} à ({new_zombie['x']}, {new_zombie['y']})")


def update_zombies():
    global active_zombies
    gravity = 0.5  # Gravité qui va faire redescendre les zombies
    MAX_HEIGHT = WINDOW_HEIGHT // 9  # Limite de la hauteur à laquelle les zombies peuvent atteindre

    for zombie in active_zombies:
        if zombie['throw']:  # Si le zombie est en vol
            zombie['t'] += 0.1  # Augmenter le temps pour la trajectoire (ajustez la vitesse du mouvement ici)
            
            # Mouvements paraboliques : y(t) = y_0 + v_0 * t + 0.5 * g * t^2
            zombie['y'] = (WINDOW_HEIGHT - 100) + zombie['speed_y'] * zombie['t'] + 0.5 * gravity * zombie['t'] ** 2
            
            # Si le zombie a atteint la hauteur maximale, il ne doit pas dépasser cette hauteur.
            if zombie['y'] < MAX_HEIGHT:
                zombie['y'] = MAX_HEIGHT  # Limiter la hauteur maximale atteinte

            # Si le zombie descend en dessous de la fenêtre, on le bloque au bas de l'écran
            if zombie['y'] > WINDOW_HEIGHT:
                zombie['y'] = WINDOW_HEIGHT

            # Déplacement horizontal (ajusté par la vitesse en X)
            zombie['x'] += zombie['speed_x']
            
            # Si le zombie sort de l'écran par en bas, on le supprime
            if zombie['y'] >= WINDOW_HEIGHT:
                active_zombies.remove(zombie)



# Fonction pour afficher les zombies
def draw_zombies():
    for zombie in active_zombies:
        window.blit(zombie['img'], (int(zombie['x']), int(zombie['y'])))
        
        # Debug : Dessiner un rectangle rouge autour du zombie
        if DEBUG_MODE:
            pygame.draw.rect(window, RED, (int(zombie['x']), int(zombie['y']), 50, 50), 2)

# Affichage du menu avant le lancement du jeu
menu()

# Timer pour générer un zombie toutes les 2 secondes
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2000)

# Boucle principale du jeu
running = True
while running:
    window.blit(background_image, (0, 0))  # Redessiner le fond

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_EVENT:  # Générer un zombie toutes les 2 secondes
            generate_random_zombie()

    update_zombies()  # Mise à jour des zombies
    draw_zombies()  # Affichage des zombies

    pygame.display.update()  # Rafraîchir l'écran
    pygame.time.delay(30)  # Pause pour limiter la vitesse

pygame.quit()