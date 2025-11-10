# agent.py

import random
import pickle
import os
from collections import defaultdict

class QLearningAgent:
    def __init__(self, actions, alpha, gamma, epsilon, epsilon_end, epsilon_decay):
        self.actions = actions
        self.alpha = alpha     # Taux d'apprentissage
        self.gamma = gamma     # Facteur d'escompte
        self.epsilon = epsilon
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        
        # La Q-table. On utilise defaultdict pour que les 
        # états non visités aient une valeur Q de 0 par défaut.
        self.q_table = defaultdict(lambda: 0.0)

    def get_q_value(self, state, action):
        """Récupère la valeur Q pour un état et une action."""
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        """
        Choisit une action en utilisant la stratégie epsilon-greedy.
        - 'Exploration' : Choisit une action aléatoire (probabilité epsilon)
        - 'Exploitation': Choisit la meilleure action connue (probabilité 1-epsilon)
        """
        if random.uniform(0, 1) < self.epsilon:
            # --- Exploration ---
            return random.choice(self.actions)
        else:
            # --- Exploitation ---
            q_values = [] 
            for a in self.actions:
                q = self.get_q_value(state, a) 
                q_values.append(q)

            max_q = max(q_values)
            
            # S'il y a plusieurs actions avec la même valeur max,
            # en choisir une au hasard parmi elles.
            best_actions = []  
            for a, q in zip(self.actions, q_values):
                if q == max_q:
                    best_actions.append(a)
            return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        """
        Met à jour la Q-table en utilisant la formule de Bellman.
        Q(s, a) <- Q(s, a) + alpha * [r + gamma * max(Q(s', a')) - Q(s, a)]
        """
        # Récupérer l'ancienne valeur Q
        old_q = self.get_q_value(state, action)
        
        # Trouver la meilleure valeur Q pour l'état suivant
        max_future_q = float('-inf') 

        # On parcourt chaque action possible
        for a in self.actions:
            q = self.get_q_value(next_state, a)
            
            if q > max_future_q:
                max_future_q = q
        
        # Calculer la nouvelle valeur Q (l'objectif de la mise à jour)
        target = reward + self.gamma * max_future_q
        
        # Mettre à jour la Q-table
        new_q = old_q + self.alpha * (target - old_q)
        self.q_table[(state, action)] = new_q

    def update_epsilon(self):
        """Réduit l'epsilon pour moins explorer avec le temps."""
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

    def save_q_table(self, filename):
        """Sauvegarde la Q-table dans un fichier."""
        # On convertit le defaultdict en dict normal pour le pickle
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
        print(f"Q-table sauvegardée dans {filename}")

    def load_q_table(self, filename):
        """Charge la Q-table depuis un fichier."""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.q_table = defaultdict(lambda: 0.0, pickle.load(f))
            print(f"Q-table chargée depuis {filename}")
        else:
            print(f"Fichier Q-table {filename} non trouvé. Démarrage avec une table vide.")