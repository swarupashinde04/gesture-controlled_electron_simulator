import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Electron Simulation")

x = random.randint(100,700)
y = random.randint(100,500)

vx = 3
vy = 3

clock = pygame.time.Clock()

running = True
while running:

    screen.fill((0,0,0))

    x += vx
    y += vy

    if x <= 0 or x >= 800:
        vx *= -1
    if y <= 0 or y >= 600:
        vy *= -1

    pygame.draw.circle(screen, (0,255,255), (x,y), 8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
