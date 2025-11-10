# Pacman-Q-Learning

Ce projet est une implémentation de l'algorithme d'apprentissage par renforcement **Q-Learning** pour entraîner un agent IA à jouer à une version simplifiée de Pac-Man. L'agent apprend à naviguer dans un labyrinthe, à manger toutes les gommes (pellets) et à éviter un fantôme qui se déplace aléatoirement.

Ce projet est construit en Python à l'aide de la bibliothèque Pygame pour l'environnement de jeu.

<img width="307" height="201" alt="image" src="https://github.com/user-attachments/assets/f7a31b5c-f867-4fd5-80b4-787fb5d4e7bb" />


## Fonctionnalités

* **Agent Q-Learning** : Un agent qui apprend à partir de ses expériences en utilisant une Q-table.
* **Environnement Pygame** : Un environnement Pac-Man simple mais fonctionnel.
* **Entraînement et Test** : Scripts séparés pour entraîner l'agent (`main.py`) et pour tester ses performances (`test_agent.py`).
* **Configuration Facile** : Tous les hyperparamètres (taux d'apprentissage, epsilon, récompenses) sont centralisés dans `config.py`.
* **Persistance** : L'agent peut sauvegarder sa Q-table apprise dans un fichier (`.pkl`) et la recharger pour continuer l'entraînement ou la tester.

---

## Structure du Projet
Pacman-Q-Learning/
├── agent.py           # Définit la classe QLearningAgent (le "cerveau" de l'IA)
├── main.py            # Script principal pour l'entraînement de l'agent
├── test_agent.py      # Script pour tester un agent déjà entraîné (mode exploitation)
├── environment.py     # Définit la classe PacManGame (logique du jeu, récompenses, état)
├── config.py          # Fichier central pour tous les hyperparamètres et réglages
├── maze.txt           # Fichier texte définissant la carte du labyrinthe
├── assets/            # Dossier pour les sprites (pacman.png, ghost.png, etc.)
├── pacman_q_table.pkl # (Généré) Fichier de sauvegarde de la Q-table apprise
└── README.md          # Ce fichier README
