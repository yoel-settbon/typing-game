import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Ninja")

# Charger une image de fruit
fruit_image = pygame.image.load("assets/images/zombies/zombie1.png")  # Remplace par ton image de fruit
fruit_image = pygame.transform.scale(fruit_image, (80, 80))  # Redimensionner l'image
fruit_rect = fruit_image.get_rect()

# Variables de fruits
fruits = []

# Fonction pour créer un fruit
def create_fruit():
    x = random.randint(5, screen_width - 100)
    y = screen_height + 50  # Commence en bas de l'écran
    speed = random.randint(5, 10)
    angle = random.uniform(-math.pi/4, math.pi/4)  # L'angle de lancement des fruits
    fruits.append({'rect': fruit_rect.copy(), 'x': x, 'y': y, 'speed': speed, 'angle': angle})

# Boucle de jeu
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((255, 255, 255))  # Fond blanc

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacer les fruits
    for fruit in fruits:
        fruit['x'] += fruit['speed'] * math.cos(fruit['angle'])
        fruit['y'] -= fruit['speed'] * math.sin(fruit['angle'])

        # Afficher le fruit
        screen.blit(fruit_image, (fruit['x'], fruit['y']))

        # Supprimer les fruits hors de l'écran
        if fruit['y'] < 0 or fruit['x'] < 0 or fruit['x'] > screen_width:
            fruits.remove(fruit)

    # Ajouter un fruit à intervalle aléatoire
    if random.randint(1, 100) > 98:  # Chance d'ajouter un fruit
        create_fruit()

    # Actualiser l'écran
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
