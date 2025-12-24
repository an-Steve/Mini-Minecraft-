# 🎮 Minecraft Python - Version Complète

Un clone complet de Minecraft développé en Python avec Pygame, incluant génération procédurale de monde, système de craft, mobs hostiles, et bien plus !

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📸 Aperçu

Un jeu d'aventure et de survie en 2D inspiré de Minecraft avec :
- Génération de monde infinie et procédurale
- Système de craft complet
- Mobs hostiles avec IA
- Cycle jour/nuit
- Multiples biomes
- Plus de 20 types de blocs différents

## ✨ Fonctionnalités

### 🌍 Génération de Monde
- **Génération procédurale** utilisant le bruit de Perlin
- **4 biomes** : Plaines, Forêt, Désert, Neige
- **Grottes souterraines** avec lave
- **Minerais** répartis par profondeur :
  - Charbon (y < 128)
  - Fer (y < 64)
  - Or (y < 32)
  - Diamant (y < 16)
- Lacs, arbres, cactus
- Bedrock indestructible au fond du monde

### ⛏️ Système de Minage
- Vitesse de minage variable selon l'outil
- Outils en 4 matériaux : **Bois → Pierre → Fer → Diamant**
- Progression visuelle avec fissures
- Particules lors de la destruction
- Portée de minage réaliste

### 🔨 Craft & Objets
Plus de **30 recettes de craft** incluant :
- **Outils** : Pioches, haches, pelles, épées
- **Blocs** : Planches, verre, briques, cobblestone
- **Objets utiles** : Torches, fours, tables de craft
- Menu de craft interactif

### 🧟 Mobs & Combat
- **4 types de mobs** : Zombies, Squelettes, Creepers, Araignées
- IA qui traque et attaque le joueur
- Spawn automatique la nuit
- Système de vie pour les mobs
- Dégâts au contact

### 🌓 Environnement Dynamique
- **Cycle jour/nuit** avec transitions réalistes
- Changements de couleur du ciel
- Plus de mobs la nuit
- Effets d'éclairage

### 💖 Système de Survie
- **20 points de vie** ❤️
- **20 points de faim** 🍖
- Dégâts environnementaux (lave, cactus)
- Physique de l'eau (ralentissement, nage)
- Game Over et respawn

### 🎮 Modes de Jeu
- **Mode Survie** : Vie limitée, faim, dégâts
- **Mode Créatif** : Invincibilité (touche G)

## 🎯 Contrôles

### Déplacement
| Touche | Action |
|--------|--------|
| `Q` ou `←` | Se déplacer à gauche |
| `D` ou `→` | Se déplacer à droite |
| `ESPACE` | Sauter |
| `SHIFT` | Sprint |

### Actions
| Touche | Action |
|--------|--------|
| `Clic gauche` | Miner (maintenir) |
| `Clic droit` | Placer un bloc |
| `1-9` | Sélectionner slot de hotbar |
| `E` | Ouvrir l'inventaire |
| `C` | Ouvrir le menu de craft |

### Système
| Touche | Action |
|--------|--------|
| `G` | Changer de mode (Survival/Creative) |
| `F3` | Afficher les informations de debug |
| `ÉCHAP` | Fermer les menus |

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- Pygame 2.0 ou supérieur

### Installation rapide

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/minecraft-python.git
cd minecraft-python
```

2. **Installer Pygame**
```bash
pip install pygame
```

3. **Lancer le jeu**
```bash
python minecraft_complete.py
```

### Installation avec environnement virtuel (recommandé)

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur Linux/Mac :
source venv/bin/activate

# Installer les dépendances
pip install pygame

# Lancer le jeu
python minecraft_complete.py
```

## 🎨 Types de Blocs

Le jeu contient plus de **20 types de blocs** :

| Bloc | Description | Obtention |
|------|-------------|-----------|
| 🟩 Herbe | Bloc de surface | Miner avec pelle |
| 🟫 Terre | Sous l'herbe | Miner avec pelle |
| ⬜ Pierre | Roche commune | Miner avec pioche |
| ⬛ Bedrock | Indestructible | - |
| 🟨 Sable | Dans les déserts | Miner avec pelle |
| 💧 Eau | Liquide | - |
| 🟫 Bois | Troncs d'arbres | Miner avec hache |
| 🟢 Feuilles | Couronnes d'arbres | Miner |
| ⚫ Charbon | Minerai commun | Miner avec pioche |
| 🔶 Fer | Minerai moyen | Miner avec pioche en pierre+ |
| 🟡 Or | Minerai rare | Miner avec pioche en fer+ |
| 💎 Diamant | Minerai très rare | Miner avec pioche en fer+ |
| 🟧 Planches | Bois transformé | Craft : 1 bois → 4 planches |
| 🔥 Torche | Source de lumière | Craft : 1 charbon + 1 bâton |
| 🔥 Lave | Liquide dangereux | Grottes profondes |
| ❄️ Neige | Biome neigeux | Miner avec pelle |
| 🧊 Glace | Eau gelée | Miner avec pioche |
| 🌵 Cactus | Désert (dangereux) | Miner |

## 🔧 Recettes de Craft Principales

### Outils de base
```
Planches (x4) = 1 Bois
Bâton (x4) = 2 Planches
Table de craft = 4 Planches

Pioche en bois = 3 Planches + 2 Bâtons
Hache en bois = 3 Planches + 2 Bâtons
Pelle en bois = 1 Planche + 2 Bâtons
Épée en bois = 2 Planches + 1 Bâton
```

### Outils avancés
```
Pioche en pierre = 3 Cobblestone + 2 Bâtons
Pioche en fer = 3 Lingots de fer + 2 Bâtons
Pioche en diamant = 3 Diamants + 2 Bâtons
```

### Objets utiles
```
Torche (x4) = 1 Charbon + 1 Bâton
Four = 8 Cobblestone
Verre = 1 Sable (dans un four)
```

## 🏗️ Architecture du Code

```
minecraft_complete.py
│
├── PerlinNoise          # Génération de bruit procédural
├── Chunk                # Gestion des chunks de terrain (16x256)
├── World                # Monde infini avec génération procédurale
├── Particle             # Système de particules
├── Item                 # Gestion des items dans l'inventaire
├── Player               # Joueur avec physique et inventaire
├── Mob                  # Entités hostiles avec IA
└── Game                 # Boucle principale et rendu
```

## 🎓 Concepts Techniques

### Génération Procédurale
- Utilisation du **bruit de Perlin** pour créer un terrain naturel
- Génération par chunks (16 blocs de largeur)
- Multiples octaves pour différents niveaux de détail
- Biomes basés sur des valeurs de bruit

### Physique
- Gravité réaliste (0.5 unités/frame)
- Détection de collision AABB (Axis-Aligned Bounding Box)
- Friction et résistance de l'eau
- Saut avec impulsion négative

### Optimisation
- Rendu uniquement des blocs visibles à l'écran
- Génération lazy des chunks (seulement quand nécessaire)
- Culling des particules hors écran
- Limitation du nombre de mobs actifs

## 🐛 Débogage

Appuyez sur `F3` pour afficher les informations de debug :
- FPS (images par seconde)
- Position du joueur (x, y)
- Position en blocs
- Nombre de chunks chargés
- Nombre de mobs actifs
- Nombre de particules
- État (sur le sol, dans l'eau)

## 🚀 Améliorations Futures

- [ ] Système de sauvegarde du monde
- [ ] Plus de biomes (jungle, marais, montagne)
- [ ] Animaux passifs (vaches, cochons, moutons)
- [ ] Système d'agriculture (blé, carottes)
- [ ] Plus de recettes de craft
- [ ] Boss et donjons
- [ ] Multijoueur local
- [ ] Sons et musique
- [ ] Interface graphique améliorée
- [ ] Support des textures personnalisées

## 📝 Changelog

### Version 1.0 (Actuelle)
- ✅ Génération de monde procédurale
- ✅ 4 biomes différents
- ✅ Plus de 20 types de blocs
- ✅ Système de craft complet
- ✅ 4 types de mobs hostiles
- ✅ Cycle jour/nuit
- ✅ Modes Survival et Creative
- ✅ Physique et collisions
- ✅ Système de particules
- ✅ Interface utilisateur complète

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Créé avec ❤️ en Python et Pygame

## 🙏 Remerciements

- Inspiré par le jeu original **Minecraft** de Mojang Studios
- Moteur de jeu : **Pygame**
- Génération procédurale : Algorithme de **bruit de Perlin**

## 📞 Support

Si vous rencontrez des problèmes ou avez des questions :
- Ouvrez une **Issue** sur GitHub
- Consultez la section **Débogage** ci-dessus
- Vérifiez que vous avez la bonne version de Python et Pygame

---

⭐ **N'oubliez pas de mettre une étoile si vous aimez ce projet !** ⭐

**Bon jeu ! 🎮**
