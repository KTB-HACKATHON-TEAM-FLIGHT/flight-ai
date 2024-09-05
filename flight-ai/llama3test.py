import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
SHIP_SIZE = 50
ALIEN_SIZE = 30
BULLET_SIZE = 10

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the player ship
ship = pygame.Rect(WIDTH / 2, HEIGHT - SHIP_SIZE - 10, SHIP_SIZE, SHIP_SIZE)

# Set up the aliens
aliens = [
    pygame.Rect(10 + i * (ALIEN_SIZE + 10), 10, ALIEN_SIZE, ALIEN_SIZE)
    for i in range(10)
]

# Set up the bullets
bullets = []

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the ship
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.x -= 5
    if keys[pygame.K_RIGHT]:
        ship.x += 5

    # Fire bullets
    if keys[pygame.K_SPACE]:
        bullets.append(pygame.Rect(ship.centerx, ship.top, BULLET_SIZE, BULLET_SIZE))

    # Move the bullets
    for bullet in bullets:
        bullet.y -= 5
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move the aliens
    for alien in aliens:
        alien.y += 1
        if alien.y > HEIGHT:
            aliens.remove(alien)

    # Check for collisions
    for alien in aliens:
        for bullet in bullets:
            if alien.colliderect(bullet):
                aliens.remove(alien)
                bullets.remove(bullet)

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, ship)
    for alien in aliens:
        pygame.draw.rect(screen, WHITE, alien)
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // 60)