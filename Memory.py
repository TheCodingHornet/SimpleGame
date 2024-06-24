import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Memory')

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Paramètres du jeu
CARD_SIZE = 100
CARD_MARGIN = 10
GRID_SIZE = 4
TOTAL_CARDS = GRID_SIZE * GRID_SIZE

# Création des cartes
symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2
random.shuffle(symbols)

cards = []
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        x = j * (CARD_SIZE + CARD_MARGIN) + CARD_MARGIN
        y = i * (CARD_SIZE + CARD_MARGIN) + CARD_MARGIN
        card = {'rect': pygame.Rect(x, y, CARD_SIZE, CARD_SIZE),
                'symbol': symbols[i * GRID_SIZE + j],
                'revealed': False}
        cards.append(card)

# Variables de jeu
revealed_cards = []
matched_cards = []
attempts = 0

font = pygame.font.Font(None, 36)

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for card in cards:
                if card['rect'].collidepoint(pos) and card not in revealed_cards and card not in matched_cards:
                    revealed_cards.append(card)
                    card['revealed'] = True
                    if len(revealed_cards) == 2:
                        attempts += 1
                        if revealed_cards[0]['symbol'] == revealed_cards[1]['symbol']:
                            matched_cards.extend(revealed_cards)
                        else:
                            pygame.time.wait(500)
                            for c in revealed_cards:
                                c['revealed'] = False
                        revealed_cards = []

    # Dessin
    screen.fill(WHITE)

    for card in cards:
        if card['revealed'] or card in matched_cards:
            pygame.draw.rect(screen, GRAY, card['rect'])
            text = font.render(card['symbol'], True, BLACK)
            text_rect = text.get_rect(center=card['rect'].center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, BLACK, card['rect'])

    attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
    screen.blit(attempts_text, (10, HEIGHT - 40))

    if len(matched_cards) == TOTAL_CARDS:
        win_text = font.render("You Win!", True, BLACK)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()