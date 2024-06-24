import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu du Pendu")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Police
font = pygame.font.Font(None, 36)

# Liste de mots
words = ["PYTHON", "PROGRAMMATION", "ORDINATEUR", "ALGORITHME", "VARIABLE", "FONCTION"]


# Fonction pour choisir un mot aléatoire
def choose_word():
    return random.choice(words)


# Fonction pour dessiner le pendu
def draw_hangman(errors):
    # Base
    pygame.draw.line(screen, WHITE, (100, 400), (300, 400), 4)
    # Poteau vertical
    pygame.draw.line(screen, WHITE, (150, 400), (150, 100), 4)
    # Poutre horizontale
    pygame.draw.line(screen, WHITE, (150, 100), (250, 100), 4)
    # Corde
    pygame.draw.line(screen, WHITE, (250, 100), (250, 150), 4)

    if errors > 0:
        # Tête
        pygame.draw.circle(screen, WHITE, (250, 175), 25, 4)
    if errors > 1:
        # Corps
        pygame.draw.line(screen, WHITE, (250, 200), (250, 300), 4)
    if errors > 2:
        # Bras gauche
        pygame.draw.line(screen, WHITE, (250, 225), (200, 250), 4)
    if errors > 3:
        # Bras droit
        pygame.draw.line(screen, WHITE, (250, 225), (300, 250), 4)
    if errors > 4:
        # Jambe gauche
        pygame.draw.line(screen, WHITE, (250, 300), (200, 350), 4)
    if errors > 5:
        # Jambe droite
        pygame.draw.line(screen, WHITE, (250, 300), (300, 350), 4)


# Initialisation du jeu
word = choose_word()
word_display = ["_" for _ in word]
guessed_letters = set()
errors = 0
max_errors = 6

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                letter = chr(event.key).upper()
                if letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter in word:
                        for i, char in enumerate(word):
                            if char == letter:
                                word_display[i] = letter
                    else:
                        errors += 1

    # Vérification de fin de jeu
    if "_" not in word_display or errors >= max_errors:
        running = False

    # Dessin
    screen.fill(BLACK)
    draw_hangman(errors)

    # Affichage du mot
    word_text = font.render(" ".join(word_display), True, WHITE)
    screen.blit(word_text, (400, 200))

    # Affichage des lettres devinées
    guessed_text = font.render("Lettres devinées: " + ", ".join(sorted(guessed_letters)), True, WHITE)
    screen.blit(guessed_text, (400, 300))

    # Affichage des erreurs
    errors_text = font.render(f"Erreurs: {errors}/{max_errors}", True, WHITE)
    screen.blit(errors_text, (400, 400))

    pygame.display.flip()
    clock.tick(60)

# Affichage du résultat final
result_text = font.render("Gagné!" if "_" not in word_display else f"Perdu! Le mot était: {word}", True, WHITE)
screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 500))
pygame.display.flip()

# Attente avant de fermer
pygame.time.wait(3000)

pygame.quit()