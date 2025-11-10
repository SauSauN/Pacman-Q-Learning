# config.py

# --- Paramètres Pygame (Affichage) ---
TILE_SIZE = 28  # Taille de chaque case en pixels
SPEED = 100      # Vitesse du jeu (FPS). Mettez > 60 pour un entraînement rapide.

# --- Paramètres du Labyrinthe ---
MAZE_FILE = "maze.txt"

# --- Paramètres Q-Learning (Cerveau) ---
ALPHA = 0.1             # Taux d'apprentissage (Learning Rate)
GAMMA = 0.99            # Facteur d'escompte (Discount Factor)
EPSILON_START = 1.0     # Taux d'exploration initial (100% aléatoire)
EPSILON_END = 0.01      # Taux d'exploration final (1% aléatoire)
EPSILON_DECAY = 0.9995  # Vitesse de réduction de l'exploration

NUM_EPISODES = 3000    # Nombre total de parties à jouer

# --- Définition des Récompenses ---
REWARD_MOVE = -1        # Pénalité pour chaque déplacement (pour être efficace)
REWARD_PELLET = 10      # Récompense pour avoir mangé une gomme
REWARD_GHOST = -300     # Grosse pénalité si attrapé
REWARD_WIN = 500        # Grosse récompense si toutes les gommes sont mangées

# --- Fichier de Sauvegarde ---
Q_TABLE_FILE = "pacman_q_table.pkl"