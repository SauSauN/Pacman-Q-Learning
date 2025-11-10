# environment.py

import pygame
import os
import random
import config

class PacManGame:
    def __init__(self, maze_file):
        pygame.init()
        pygame.display.set_caption("Pac-Man Q-Learning")
        
        self.tile_size = config.TILE_SIZE
        self._load_maze(maze_file)
        
        # Dimensions de l'écran
        self.screen_width = self.width * self.tile_size
        self.screen_height = self.height * self.tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.assets = self._load_assets()
        
        self.actions = ['up', 'down', 'left', 'right']
        self.action_map = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        
        # S'assurer que reset() est appelé pour initialiser les positions
        self.reset() 

    def _load_maze(self, maze_file):
        """Charge le labyrinthe depuis un fichier texte."""
        self.maze = []
        self.all_pellets = set()
        with open(maze_file, 'r') as f:
            for y, line in enumerate(f):
                row = []
                for x, char in enumerate(line.strip()):
                    row.append(char)
                    if char == 'P':
                        self.start_pos = (x, y)
                    elif char == 'G':
                        self.ghost_start_pos = (x, y)
                    elif char == '.':
                        self.all_pellets.add((x, y))
                self.maze.append(row)
        self.width = len(self.maze[0])
        self.height = len(self.maze)

    def _load_assets(self):
        """Charge les images ou crée des surfaces de couleur en fallback."""
        assets = {}
        assets_path = "assets"
        
        def load_or_fallback(filename, color):
            path = os.path.join(assets_path, filename)
            try:
                img = pygame.image.load(path)
                return pygame.transform.scale(img, (self.tile_size, self.tile_size))
            except pygame.error:
                print(f"Avertissement: Impossible de charger {path}. Utilisation d'un carré {color}.")
                surface = pygame.Surface((self.tile_size, self.tile_size))
                surface.fill(color)
                return surface

        assets['wall'] = load_or_fallback('wall.png', (0, 0, 139))     # Bleu foncé
        assets['pacman'] = load_or_fallback('pacman.png', (255, 255, 0)) # Jaune
        assets['ghost'] = load_or_fallback('ghost.png', (255, 0, 0))   # Rouge
        assets['pellet'] = load_or_fallback('pellet.png', (255, 255, 255)) # Blanc
        
        # Créer une surface pour les gommes (plus petite)
        assets['pellet_draw'] = pygame.Surface((self.tile_size // 4, self.tile_size // 4))
        assets['pellet_draw'].fill((255, 255, 255)) # Blanc
        
        return assets

    def reset(self):
        """Réinitialise le jeu pour un nouvel épisode."""
        self.pacman_pos = self.start_pos
        self.ghost_pos = self.ghost_start_pos
        self.pellets = self.all_pellets.copy()
        self.score = 0
        return self._get_state()

    def _get_state(self):
        """
        Définit l'état. C'est crucial.
        Un état simple est (position_pacman, position_fantome).
        Pour un labyrinthe de 10x10, cela fait (100 * 100) = 10 000 états, ce qui est gérable.
        """
        # On utilise des tuples pour qu'ils soient "hashables" (utilisables comme clés de dict)
        return (self.pacman_pos, self.ghost_pos)

    def step(self, action):
        """Fait avancer le jeu d'une étape."""
        
        # 1. Mouvement de Pac-Man
        dx, dy = self.action_map[action]
        next_pac_pos = (self.pacman_pos[0] + dx, self.pacman_pos[1] + dy)
        
        # Vérification des murs pour Pac-Man
        if self.maze[next_pac_pos[1]][next_pac_pos[0]] != '#':
            self.pacman_pos = next_pac_pos
        
        # 2. Mouvement du Fantôme (Logique simple : aléatoire)
        ghost_action = random.choice(self.actions)
        dgx, dgy = self.action_map[ghost_action]
        next_ghost_pos = (self.ghost_pos[0] + dgx, self.ghost_pos[1] + dgy)
        
        # Vérification des murs pour le Fantôme
        if self.maze[next_ghost_pos[1]][next_ghost_pos[0]] != '#':
            self.ghost_pos = next_ghost_pos

        # 3. Calcul des récompenses et de l'état 'done'
        done = False
        reward = config.REWARD_MOVE # Pénalité de base pour bouger

        if self.pacman_pos == self.ghost_pos:
            reward = config.REWARD_GHOST
            done = True
        elif self.pacman_pos in self.pellets:
            reward = config.REWARD_PELLET
            self.pellets.remove(self.pacman_pos)
            self.score += 10
            if not self.pellets: # Si c'était la dernière gomme
                reward = config.REWARD_WIN
                done = True
        
        next_state = self._get_state()
        return next_state, reward, done

    def render(self):
        """Affiche l'état actuel du jeu."""
        self.screen.fill((0, 0, 0)) # Fond noir
        
        for y, row in enumerate(self.maze):
            for x, tile in enumerate(row):
                pos_rect = (x * self.tile_size, y * self.tile_size)
                if tile == '#':
                    self.screen.blit(self.assets['wall'], pos_rect)
        
        # Dessiner les gommes
        pellet_offset = self.tile_size // 2 - self.tile_size // 8
        for (px, py) in self.pellets:
            pos_rect = (px * self.tile_size + pellet_offset, py * self.tile_size + pellet_offset)
            self.screen.blit(self.assets['pellet_draw'], pos_rect)
            
        # Dessiner Pac-Man
        pac_rect = (self.pacman_pos[0] * self.tile_size, self.pacman_pos[1] * self.tile_size)
        self.screen.blit(self.assets['pacman'], pac_rect)

        # Dessiner le Fantôme
        ghost_rect = (self.ghost_pos[0] * self.tile_size, self.ghost_pos[1] * self.tile_size)
        self.screen.blit(self.assets['ghost'], ghost_rect)
        
        pygame.display.flip()

    def close(self):
        """Ferme Pygame."""
        pygame.quit()