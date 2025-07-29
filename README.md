# Asteroid Game

Un clone du jeu classique Asteroids développé en Python avec Pygame.

## Description

Ce jeu reprend les mécaniques du célèbre Asteroids où le joueur contrôle un vaisseau spatial et doit détruire des astéroïdes qui se divisent en morceaux plus petits quand ils sont touchés.

## Fonctionnalités

- **Contrôle du vaisseau** : Déplacement, rotation et tir
- **Astéroïdes dynamiques** : 3 tailles différentes qui se divisent lors de l'impact
- **Génération continue** : Les astéroïdes apparaissent depuis les bords de l'écran
- **Détection de collision** : Entre le joueur/astéroïdes et projectiles/astéroïdes
- **Game Over** : Fin de partie lors d'une collision avec le vaisseau

## Contrôles

- **↑** : Avancer
- **↓** : Reculer
- **←** : Tourner à gauche
- **→** : Tourner à droite
- **Espace** : Tirer

## Installation

### Prérequis

- Python 3.12 ou supérieur
- uv (gestionnaire de paquets Python)

### Installation des dépendances

```bash
uv sync
```

ou avec pip :

```bash
pip install pygame==2.6.1
```

## Lancement du jeu

```bash
python main.py
```

## Structure du projet

```
asteroid_py/
├── main.py           # Boucle principale du jeu
├── player.py         # Classe du vaisseau joueur
├── asteroid.py       # Classe des astéroïdes
├── shot.py           # Classe des projectiles
├── asteroidfield.py  # Générateur d'astéroïdes
├── circleshape.py    # Classe de base pour les objets circulaires
├── constants.py      # Configuration et constantes du jeu
├── pyproject.toml    # Configuration du projet
└── README.md         # Ce fichier
```

## Architecture

Le jeu utilise une architecture orientée objet basée sur les sprites de Pygame :

- **CircleShape** : Classe de base abstraite pour tous les objets du jeu (hérite de pygame.sprite.Sprite)
- **Player** : Le vaisseau spatial contrôlé par le joueur
- **Asteroid** : Les astéroïdes qui se déplacent et se divisent
- **Shot** : Les projectiles tirés par le joueur
- **AsteroidField** : Gestionnaire de génération d'astéroïdes

## Configuration

Les paramètres du jeu sont définis dans `constants.py` :

- Taille de l'écran : 1280x720
- Rayon du joueur : 20 pixels
- Vitesse de déplacement : 200 pixels/seconde
- Vitesse de rotation : 300 degrés/seconde
- Cooldown de tir : 0.3 secondes
- Taux de spawn des astéroïdes : 0.8 secondes

## Améliorations possibles

- Ajouter un système de score
- Implémenter plusieurs vies
- Ajouter un wrap-around pour le vaisseau (réapparition de l'autre côté)
- Nettoyer les projectiles hors écran
- Ajouter des effets sonores
- Créer des niveaux avec difficulté progressive
- Améliorer les graphismes et effets visuels
- Ajouter un menu principal et écran de game over