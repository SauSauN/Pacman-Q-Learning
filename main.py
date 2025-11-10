# main.py

import pygame
import sys
import config  # Importer notre fichier de configuration
from environment import PacManGame
from agent import QLearningAgent

def main():
    # Initialisation de l'environnement et de l'agent
    env = PacManGame(config.MAZE_FILE)
    actions = env.actions
    
    agent = QLearningAgent(
        actions=actions,
        alpha=config.ALPHA,
        gamma=config.GAMMA,
        epsilon=config.EPSILON_START,
        epsilon_end=config.EPSILON_END,
        epsilon_decay=config.EPSILON_DECAY
    )
    
    # Charger une Q-table existante si elle existe
    agent.load_q_table(config.Q_TABLE_FILE)
    
    clock = pygame.time.Clock()
    
    print("--- Démarrage de l'entraînement ---")

    for episode in range(config.NUM_EPISODES):
        state = env.reset()
        done = False
        total_reward = 0
        
        # Pour compter les étapes (steps) dans un épisode
        step_count = 0 # <-- NOUVEAU
        
        while not done:
            # Gérer les événements Pygame (pour fermer la fenêtre)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\nArrêt de l'entraînement (par l'utilisateur).") # Ajout de \n
                    agent.save_q_table(config.Q_TABLE_FILE)
                    env.close()
                    sys.exit()

            # 1. L'agent choisit une action
            action = agent.choose_action(state)
            
            # 2. L'environnement exécute l'action
            next_state, reward, done = env.step(action)
            
            # 3. L'agent apprend de cette transition
            agent.learn(state, action, reward, next_state)
            
            # 4. Mettre à jour l'état
            state = next_state
            total_reward += reward
            step_count += 1
            
            # 5. Afficher le jeu
            env.render()
            
            # 6. Contrôler la vitesse
            clock.tick(config.SPEED)
            
            # --- AFFICHAGE CONTINU ---
            # Le 'end="\r"' fait en sorte que la ligne suivante
            # s'écrive par-dessus celle-ci.
            print(f"Épisode: {episode + 1}/{config.NUM_EPISODES} | Score: {total_reward: 5d} | Étapes: {step_count: 3d} | Epsilon: {agent.epsilon:.4f}  ", end="\r") # <-- NOUVEAU

        # Fin de l'épisode
        
        # --- NOUVEAU ---
        # On imprime une ligne vide pour "valider" la ligne précédente
        # et passer à la suivante pour le résumé.
        print() 
        
        agent.update_epsilon() # Réduire l'exploration
        
        if (episode + 1) % 100 == 0:
            # Ligne modifiée pour être un "Résumé" clair
            print(f"--- Résumé Épisode {episode + 1} --- Score final: {total_reward}, Epsilon actuel: {agent.epsilon:.4f} ---") # <-- MODIFIÉ
            # Sauvegarder périodiquement
            agent.save_q_table(config.Q_TABLE_FILE)

    print("--- Entraînement terminé ---")
    agent.save_q_table(config.Q_TABLE_FILE)
    env.close()

if __name__ == "__main__":
    main()