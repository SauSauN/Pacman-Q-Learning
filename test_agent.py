import pygame
import sys
import pickle
import config
from environment import PacManGame
from agent import QLearningAgent

def test_agent():
    # Charger l'environnement
    env = PacManGame(config.MAZE_FILE)
    actions = env.actions

    # Charger l'agent et sa Q-table apprise
    agent = QLearningAgent(
        actions=actions,
        alpha=config.ALPHA,
        gamma=config.GAMMA,
        epsilon=0.0,  # Aucune exploration, 100% exploitation
        epsilon_end=0.0,
        epsilon_decay=1.0
    )

    print(f"Chargement de la Q-table depuis : {config.Q_TABLE_FILE}")
    agent.load_q_table(config.Q_TABLE_FILE)

    clock = pygame.time.Clock()

    print("--- DÉMARRAGE DU TEST ---")

    for episode in range(5):  # Nombre d’épisodes de test
        state = env.reset()
        done = False
        total_reward = 0
        step_count = 0

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("\nFermeture du test.")
                    env.close()
                    sys.exit()

            # exploitation pure
            agent.epsilon = 0.0
            action = agent.choose_action(state)

            next_state, reward, done = env.step(action)
            state = next_state
            total_reward += reward
            step_count += 1

            env.render()
            clock.tick(config.SPEED)


        print(f"✅ Épisode {episode + 1} terminé - Récompense totale : {total_reward} | Étapes : {step_count}")

    env.close()
    print("--- TEST TERMINÉ ---")

if __name__ == "__main__":
    test_agent()
