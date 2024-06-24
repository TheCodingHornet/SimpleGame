import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paramètres du jeu
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
BALL_SPEED = 5
PADDLE_SPEED = 7

# Création des raquettes
player = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Création de la balle
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_dx = BALL_SPEED * random.choice((1, -1))
ball_dy = BALL_SPEED * random.choice((1, -1))

# Scores
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Fonction pour réinitialiser la balle
def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_dx = BALL_SPEED * random.choice((1, -1))
    ball_dy = BALL_SPEED * random.choice((1, -1))

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Déplacement du joueur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED

    # IA simple pour l'adversaire
    if opponent.centery < ball.centery and opponent.bottom < HEIGHT:
        opponent.y += PADDLE_SPEED
    elif opponent.centery > ball.centery and opponent.top > 0:
        opponent.y -= PADDLE_SPEED

    # Déplacement de la balle
    ball.x += ball_dx
    ball.y += ball_dy

    # Collision avec les bords supérieur et inférieur
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    # Collision avec les raquettes
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_dx *= -1

    # Marquage des points
    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
    elif ball.right >= WIDTH:
        player_score += 1
        reset_ball()

    # Dessin des éléments
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Affichage des scores
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH//4, 20))
    screen.blit(opponent_text, (3*WIDTH//4, 20))

    # Mise à jour de l'affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()