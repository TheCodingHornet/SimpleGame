import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casse-briques")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paramètres du jeu
paddle_width = 100
paddle_height = 10
ball_radius = 10
brick_width = 10
brick_height = 4

# Création de la raquette
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 50, paddle_width, paddle_height)

# Création de la balle
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = -5

# Création des briques
bricks = []
for i in range(8):
    for j in range(47):
        brick = pygame.Rect(j * (brick_width + 5) + 50, i * (brick_height + 5) + 50, brick_width, brick_height)
        bricks.append(brick)

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement de la raquette
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 7
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 7

    # Déplacement de la balle
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collision avec les murs
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= HEIGHT:
        running = False  # Fin du jeu si la balle touche le bas

    # Collision avec la raquette
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1
        # Ajustement de l'angle en fonction de l'endroit où la balle touche la raquette
        middle_y = paddle.y + paddle.height / 2
        difference_in_y = middle_y - ball.y
        reduction_factor = (paddle.height / 2) / 5
        ball_speed_x = difference_in_y / reduction_factor

    # Collision avec les briques
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            break

    # Dessin des éléments
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()