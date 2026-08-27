import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# DIMENSIONS
LARGEUR = 1400
HAUTEUR = 800
TAILLE_CASE = 40

# COULEURS
VERT_EVA = (57, 255, 20)
VIOLET_EVA = (110, 45, 160)
BLANC = (255, 255, 255)

# FENETRE
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake EVA")

horloge = pygame.time.Clock()
VITESSE = 15

police = pygame.font.SysFont(None, 35)

# MUSIQUE
pygame.mixer.music.load("musique.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# IMAGES
fond = pygame.image.load("fond.jpg")
fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

img_pomme = pygame.image.load("pomme.png").convert_alpha()
img_pomme = pygame.transform.scale(
    img_pomme,
    (TAILLE_CASE, TAILLE_CASE)
)

img_pomme_doree = pygame.image.load("pomme_doree.png").convert_alpha()
img_pomme_doree = pygame.transform.scale(
    img_pomme_doree,
    (int(TAILLE_CASE * 1.6), int(TAILLE_CASE * 1.6))
)

img_champignon = pygame.image.load("champignon.png").convert_alpha()
img_champignon = pygame.transform.scale(
    img_champignon,
    (int(TAILLE_CASE * 1.6), int(TAILLE_CASE * 1.6))
)


# FONCTIONS

def afficher_score(score):

    texte = police.render(
        f"Score : {score}",
        True,
        BLANC
    )

    fenetre.blit(texte, (10, 10))


def dessiner_serpent(serpent):

    for i, segment in enumerate(serpent):

        couleur = (
            VERT_EVA
            if i == len(serpent) - 1
            else VIOLET_EVA
        )

        pygame.draw.rect(
            fenetre,
            couleur,
            (
                segment[0],
                segment[1],
                TAILLE_CASE,
                TAILLE_CASE
            )
        )


def position_aleatoire():

    return (
        random.randrange(0, LARGEUR, TAILLE_CASE),
        random.randrange(0, HAUTEUR, TAILLE_CASE)
    )


def collision(x, y, objet):

    return pygame.Rect(
        x,
        y,
        TAILLE_CASE,
        TAILLE_CASE
    ).colliderect(
        pygame.Rect(
            objet[0],
            objet[1],
            TAILLE_CASE,
            TAILLE_CASE
        )
    )


# JEU

def jeu():

    x = LARGEUR // 2
    y = HAUTEUR // 2

    dx = TAILLE_CASE
    dy = 0

    serpent = []
    longueur = 1
    score = 0

    nourriture = position_aleatoire()

    pomme_doree = None
    champignon = None

    while True:

        # EVENEMENTS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # ZQSD
                if event.key == pygame.K_q and dx == 0:
                    dx = -TAILLE_CASE
                    dy = 0

                elif event.key == pygame.K_d and dx == 0:
                    dx = TAILLE_CASE
                    dy = 0

                elif event.key == pygame.K_z and dy == 0:
                    dy = -TAILLE_CASE
                    dx = 0

                elif event.key == pygame.K_s and dy == 0:
                    dy = TAILLE_CASE
                    dx = 0

        # DEPLACEMENT
        x += dx
        y += dy

        # COLLISION BORDS
        if (
            x < 0
            or x >= LARGEUR
            or y < 0
            or y >= HAUTEUR
        ):
            pygame.quit()
            sys.exit()

        # TETE
        tete = [x, y]
        serpent.append(tete)

        # LONGUEUR
        if len(serpent) > longueur:
            del serpent[0]

        # COLLISION AVEC SOI-MEME
        for segment in serpent[:-1]:

            if segment == tete:
                pygame.quit()
                sys.exit()

        # POMME NORMALE
        if collision(x, y, nourriture):

            nourriture = position_aleatoire()

            longueur += 1
            score += 1

        # POMME DOREE = +5
        if pomme_doree and collision(x, y, pomme_doree):

            pomme_doree = None
            score += 5

        # CHAMPIGNON = -3
        if champignon and collision(x, y, champignon):

            champignon = None

            

        # SPAWN
        if (
            random.random() < 0.005
            and pomme_doree is None
        ):
            pomme_doree = position_aleatoire()

        if (
            random.random() < 0.005
            and champignon is None
        ):
            champignon = position_aleatoire()

        # AFFICHAGE
        fenetre.blit(fond, (0, 0))

        # POMME
        fenetre.blit(img_pomme, nourriture)

        # POMME DOREE
        if pomme_doree:

            fenetre.blit(
                img_pomme_doree,
                (
                    pomme_doree[0] - 12,
                    pomme_doree[1] - 12
                )
            )

        # CHAMPIGNON
        if champignon:

            fenetre.blit(
                img_champignon,
                (
                    champignon[0] - 12,
                    champignon[1] - 12
                )
            )

        # SERPENT
        dessiner_serpent(serpent)

        # SCORE
        afficher_score(score)

        pygame.display.update()

        # FPS
        horloge.tick(VITESSE)


jeu()