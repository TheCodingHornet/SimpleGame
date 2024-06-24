import pygame
import random

# Initialisation
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Formes des pièces
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Couleurs des pièces
SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

# Configuration de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")


# Fonction pour créer une nouvelle pièce
def new_piece():
    shape = random.choice(SHAPES)
    color = SHAPE_COLORS[SHAPES.index(shape)]
    return {
        'shape': shape,
        'color': color,
        'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
        'y': 0
    }


# Fonction pour dessiner la grille
def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))


# Fonction pour vérifier la collision
def check_collision(shape, grid, x, y):
    for y_offset, row in enumerate(shape):
        for x_offset, cell in enumerate(row):
            if cell:
                if (y + y_offset >= GRID_HEIGHT or
                        x + x_offset < 0 or
                        x + x_offset >= GRID_WIDTH or
                        grid[y + y_offset][x + x_offset]):
                    return True
    return False


# Fonction pour effacer les lignes complètes
def clear_lines(grid):
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for line in full_lines:
        del grid[line]
        grid.insert(0, [None] * GRID_WIDTH)
    return len(full_lines)


# Initialisation du jeu
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_piece = new_piece()
next_piece = new_piece()
score = 0
level = 1
lines_cleared = 0

clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5  # Secondes

running = True
while running:
    fall_time += clock.get_rawtime()
    clock.tick()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_piece['shape'], grid, current_piece['x'] - 1, current_piece['y']):
                    current_piece['x'] -= 1
            if event.key == pygame.K_RIGHT:
                if not check_collision(current_piece['shape'], grid, current_piece['x'] + 1, current_piece['y']):
                    current_piece['x'] += 1
            if event.key == pygame.K_DOWN:
                if not check_collision(current_piece['shape'], grid, current_piece['x'], current_piece['y'] + 1):
                    current_piece['y'] += 1
            if event.key == pygame.K_UP:
                rotated = list(zip(*current_piece['shape'][::-1]))
                if not check_collision(rotated, grid, current_piece['x'], current_piece['y']):
                    current_piece['shape'] = rotated

    # Chute automatique de la pièce
    if fall_time / 1000 > fall_speed:
        fall_time = 0
        if not check_collision(current_piece['shape'], grid, current_piece['x'], current_piece['y'] + 1):
            current_piece['y'] += 1
        else:
            # Fixer la pièce sur la grille
            for y_offset, row in enumerate(current_piece['shape']):
                for x_offset, cell in enumerate(row):
                    if cell:
                        grid[current_piece['y'] + y_offset][current_piece['x'] + x_offset] = current_piece['color']

            # Effacer les lignes complètes
            lines = clear_lines(grid)
            score += lines ** 2 * 100
            lines_cleared += lines
            level = lines_cleared // 10 + 1
            fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)

            # Nouvelle pièce
            current_piece = next_piece
            next_piece = new_piece()

            # Vérifier game over
            if check_collision(current_piece['shape'], grid, current_piece['x'], current_piece['y']):
                running = False

    # Dessin
    screen.fill(BLACK)
    draw_grid(grid)

    # Dessiner la pièce courante
    for y_offset, row in enumerate(current_piece['shape']):
        for x_offset, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_piece['color'],
                                 ((current_piece['x'] + x_offset) * GRID_SIZE,
                                  (current_piece['y'] + y_offset) * GRID_SIZE,
                                  GRID_SIZE - 1, GRID_SIZE - 1))

    # Dessiner la barre latérale
    pygame.draw.rect(screen, WHITE, (GRID_WIDTH * GRID_SIZE, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))

    # Afficher le score et le niveau
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (GRID_WIDTH * GRID_SIZE + 10, 10))
    screen.blit(level_text, (GRID_WIDTH * GRID_SIZE + 10, 50))

    # Afficher la prochaine pièce
    next_piece_text = font.render("Next:", True, BLACK)
    screen.blit(next_piece_text, (GRID_WIDTH * GRID_SIZE + 10, 100))
    for y_offset, row in enumerate(next_piece['shape']):
        for x_offset, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, next_piece['color'],
                                 (GRID_WIDTH * GRID_SIZE + 50 + x_offset * GRID_SIZE,
                                  150 + y_offset * GRID_SIZE,
                                  GRID_SIZE - 1, GRID_SIZE - 1))

    pygame.display.flip()

pygame.quit()