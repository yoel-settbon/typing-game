import pygame
pygame.init()
screen = pygame.display.set_mode((1400, 750))
running = True
image = pygame.image.load('assets\images/bombs\woman.png').convert()
x = 0
y = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        x -= 1
    if pressed[pygame.K_RIGHT]:
        x += 1
    if pressed[pygame.K_DOWN]:
        y += 1
    if pressed[pygame.K_UP]:
        y -= 1

    screen.fill((10, 100, 100))
    screen.blit(image, (x, y))
    pygame.display.flip()
    clock.tick(600)



pygame.quit()