import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialisation du jeu
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = RIGHT

food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

score = 0
font = pygame.font.Font(None, 36)

# Fonction pour dessiner un rectangle sur la grille
def draw_rect(pos, color):
    rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, color, rect)

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != DOWN:
                snake_direction = UP
            elif event.key == pygame.K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                snake_direction = RIGHT

    # Déplacement du serpent
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    snake.insert(0, new_head)

    # Vérification de la collision avec la nourriture
    if snake[0] == food:
        score += 1
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    else:
        snake.pop()

    # Vérification des collisions
    if (snake[0][0] < 0 or snake[0][0] >= GRID_WIDTH or
        snake[0][1] < 0 or snake[0][1] >= GRID_HEIGHT or
        snake[0] in snake[1:]):
        running = False

    # Dessin
    screen.fill(BLACK)
    for segment in snake:
        draw_rect(segment, GREEN)
    draw_rect(food, RED)

    # Affichage du score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(10)  # Contrôle la vitesse du jeu

# Affichage du score final
game_over_text = font.render(f"Game Over! Score final: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()

# Attente avant de fermer
pygame.time.wait(3000)

pygame.quit()