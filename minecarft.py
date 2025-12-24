import pygame
import random
import math
import sys
from collections import defaultdict

# Implémentation simple du bruit de Perlin
class PerlinNoise:
    def __init__(self, seed=0):
        random.seed(seed)
        self.permutation = list(range(256))
        random.shuffle(self.permutation)
        self.permutation *= 2
    
    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(self, t, a, b):
        return a + t * (b - a)
    
    def grad(self, hash_val, x):
        return x if hash_val & 1 else -x
    
    def noise1d(self, x):
        xi = int(x) & 255
        xf = x - int(x)
        
        u = self.fade(xf)
        
        a = self.permutation[xi]
        b = self.permutation[xi + 1]
        
        return self.lerp(u, self.grad(a, xf), self.grad(b, xf - 1))
    
    def pnoise1(self, x, octaves=1, persistence=0.5, lacunarity=2.0):
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0
        
        for _ in range(octaves):
            total += self.noise1d(x * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity
        
        return total / max_value
    
    def pnoise2(self, x, y, octaves=1, persistence=0.5, lacunarity=2.0):
        # Simplification pour le bruit 2D
        return self.pnoise1(x + y * 57.0, octaves, persistence, lacunarity)

# Instance globale
noise = PerlinNoise(12345)

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1200, 700
FPS = 60

# Couleurs
SKY_BLUE = (135, 206, 250)
NIGHT_SKY = (20, 20, 40)
SUNSET_SKY = (255, 140, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Taille des blocs
BLOCK_SIZE = 32
CHUNK_WIDTH = 16
CHUNK_HEIGHT = 256

# Textures des blocs (couleurs)
BLOCK_COLORS = {
    'air': None,
    'grass': (95, 159, 53),
    'dirt': (139, 90, 43),
    'stone': (128, 128, 128),
    'bedrock': (84, 84, 84),
    'sand': (238, 214, 175),
    'water': (64, 164, 223),
    'wood': (101, 67, 33),
    'leaves': (34, 139, 34),
    'coal_ore': (64, 64, 64),
    'iron_ore': (205, 127, 50),
    'gold_ore': (255, 215, 0),
    'diamond_ore': (0, 191, 255),
    'planks': (160, 100, 40),
    'crafting_table': (139, 69, 19),
    'furnace': (96, 96, 96),
    'torch': (255, 200, 50),
    'glass': (173, 216, 230),
    'cobblestone': (100, 100, 100),
    'brick': (150, 80, 70),
    'obsidian': (40, 0, 80),
    'lava': (255, 100, 0),
    'snow': (255, 255, 255),
    'ice': (180, 220, 255),
    'cactus': (100, 150, 50),
}

# Propriétés des blocs
BLOCK_PROPERTIES = {
    'air': {'solid': False, 'hardness': 0, 'tool': None, 'light': 0, 'transparent': True},
    'grass': {'solid': True, 'hardness': 3, 'tool': 'shovel', 'light': 0, 'transparent': False},
    'dirt': {'solid': True, 'hardness': 3, 'tool': 'shovel', 'light': 0, 'transparent': False},
    'stone': {'solid': True, 'hardness': 30, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'bedrock': {'solid': True, 'hardness': 999999, 'tool': None, 'light': 0, 'transparent': False},
    'sand': {'solid': True, 'hardness': 3, 'tool': 'shovel', 'light': 0, 'transparent': False},
    'water': {'solid': False, 'hardness': 0, 'tool': None, 'light': 0, 'transparent': True},
    'wood': {'solid': True, 'hardness': 15, 'tool': 'axe', 'light': 0, 'transparent': False},
    'leaves': {'solid': True, 'hardness': 1, 'tool': None, 'light': 0, 'transparent': True},
    'coal_ore': {'solid': True, 'hardness': 30, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'iron_ore': {'solid': True, 'hardness': 40, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'gold_ore': {'solid': True, 'hardness': 40, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'diamond_ore': {'solid': True, 'hardness': 50, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'planks': {'solid': True, 'hardness': 15, 'tool': 'axe', 'light': 0, 'transparent': False},
    'crafting_table': {'solid': True, 'hardness': 15, 'tool': 'axe', 'light': 0, 'transparent': False},
    'furnace': {'solid': True, 'hardness': 30, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'torch': {'solid': False, 'hardness': 0, 'tool': None, 'light': 14, 'transparent': True},
    'glass': {'solid': True, 'hardness': 2, 'tool': None, 'light': 0, 'transparent': True},
    'cobblestone': {'solid': True, 'hardness': 30, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'brick': {'solid': True, 'hardness': 30, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'obsidian': {'solid': True, 'hardness': 200, 'tool': 'pickaxe', 'light': 0, 'transparent': False},
    'lava': {'solid': False, 'hardness': 0, 'tool': None, 'light': 15, 'transparent': True},
    'snow': {'solid': True, 'hardness': 1, 'tool': 'shovel', 'light': 0, 'transparent': False},
    'ice': {'solid': True, 'hardness': 3, 'tool': 'pickaxe', 'light': 0, 'transparent': True},
    'cactus': {'solid': True, 'hardness': 2, 'tool': None, 'light': 0, 'transparent': False},
}

# Recettes de craft
CRAFTING_RECIPES = {
    'planks': {'wood': 1, 'output': 4},
    'crafting_table': {'planks': 4, 'output': 1},
    'stick': {'planks': 2, 'output': 4},
    'wooden_pickaxe': {'planks': 3, 'stick': 2, 'output': 1},
    'wooden_axe': {'planks': 3, 'stick': 2, 'output': 1},
    'wooden_shovel': {'planks': 1, 'stick': 2, 'output': 1},
    'wooden_sword': {'planks': 2, 'stick': 1, 'output': 1},
    'stone_pickaxe': {'cobblestone': 3, 'stick': 2, 'output': 1},
    'stone_axe': {'cobblestone': 3, 'stick': 2, 'output': 1},
    'stone_shovel': {'cobblestone': 1, 'stick': 2, 'output': 1},
    'stone_sword': {'cobblestone': 2, 'stick': 1, 'output': 1},
    'iron_pickaxe': {'iron_ingot': 3, 'stick': 2, 'output': 1},
    'iron_axe': {'iron_ingot': 3, 'stick': 2, 'output': 1},
    'iron_shovel': {'iron_ingot': 1, 'stick': 2, 'output': 1},
    'iron_sword': {'iron_ingot': 2, 'stick': 1, 'output': 1},
    'diamond_pickaxe': {'diamond': 3, 'stick': 2, 'output': 1},
    'diamond_axe': {'diamond': 3, 'stick': 2, 'output': 1},
    'diamond_shovel': {'diamond': 1, 'stick': 2, 'output': 1},
    'diamond_sword': {'diamond': 2, 'stick': 1, 'output': 1},
    'torch': {'coal': 1, 'stick': 1, 'output': 4},
    'furnace': {'cobblestone': 8, 'output': 1},
    'glass': {'sand': 1, 'output': 1},  # Nécessite four
    'brick': {'clay': 4, 'output': 1},
}

# Recettes de fusion
SMELTING_RECIPES = {
    'iron_ore': 'iron_ingot',
    'gold_ore': 'gold_ingot',
    'sand': 'glass',
    'cobblestone': 'stone',
}

class Chunk:
    def __init__(self, x):
        self.x = x
        self.blocks = {}
        self.generate()
    
    def generate(self):
        """Génération procédurale avec bruit de Perlin"""
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        
        for local_x in range(CHUNK_WIDTH):
            world_x = self.x * CHUNK_WIDTH + local_x
            
            # Hauteur de base avec bruit de Perlin
            noise_val = noise.pnoise1(world_x / scale, 
                                       octaves=octaves,
                                       persistence=persistence,
                                       lacunarity=lacunarity)
            
            base_height = int(noise_val * 30 + 80)
            
            # Déterminer le biome
            biome_noise = noise.pnoise1(world_x / 200.0, octaves=2)
            temp_noise = noise.pnoise1(world_x / 150.0, octaves=2)
            
            if biome_noise > 0.4:
                biome = 'desert'
            elif biome_noise < -0.3 and temp_noise < 0:
                biome = 'snow'
            elif biome_noise < -0.2:
                biome = 'forest'
            else:
                biome = 'plains'
            
            # Variation de hauteur selon le biome
            if biome == 'desert':
                base_height -= 5
            elif biome == 'snow':
                base_height += 10
            
            # Génération des couches
            for y in range(CHUNK_HEIGHT):
                if y == 0:
                    block_type = 'bedrock'
                elif y < base_height - 40:
                    # Minerais profonds
                    rand = random.random()
                    if y < 16 and rand < 0.001:
                        block_type = 'diamond_ore'
                    elif y < 32 and rand < 0.008:
                        block_type = 'gold_ore'
                    elif y < 64 and rand < 0.015:
                        block_type = 'iron_ore'
                    elif rand < 0.02:
                        block_type = 'coal_ore'
                    else:
                        block_type = 'stone'
                elif y < base_height - 4:
                    block_type = 'stone'
                elif y < base_height - 1:
                    block_type = 'dirt'
                elif y == base_height - 1:
                    if biome == 'desert':
                        block_type = 'sand'
                    elif biome == 'snow':
                        block_type = 'snow'
                    else:
                        block_type = 'grass'
                elif y < base_height + 1 and biome == 'snow':
                    block_type = 'snow'
                else:
                    block_type = 'air'
                
                if block_type != 'air':
                    self.blocks[(local_x, y)] = block_type
            
            # Assurer qu'il y a du sol solide autour du spawn (x=0)
            if abs(world_x) < 5:
                for y in range(60, 75):
                    if (local_x, y) not in self.blocks:
                        if y < 70:
                            self.blocks[(local_x, y)] = 'dirt'
                        elif y == 70:
                            self.blocks[(local_x, y)] = 'grass'
            
            # Grottes
            for y in range(5, base_height - 5):
                cave_noise1 = noise.pnoise2(world_x / 50.0, y / 50.0, octaves=2)
                cave_noise2 = noise.pnoise2(world_x / 30.0, y / 30.0, octaves=2)
                
                if abs(cave_noise1) < 0.1 and abs(cave_noise2) < 0.1:
                    if (local_x, y) in self.blocks:
                        del self.blocks[(local_x, y)]
                    
                    # Lave au fond
                    if y < 12 and random.random() < 0.3:
                        self.blocks[(local_x, y)] = 'lava'
            
            # Eau de surface
            water_level = 70
            if base_height < water_level:
                for y in range(base_height, water_level):
                    if (local_x, y) not in self.blocks:
                        self.blocks[(local_x, y)] = 'water'
            
            # Végétation
            if biome == 'forest' and random.random() < 0.15:
                self.generate_tree(local_x, base_height)
            elif biome == 'plains' and random.random() < 0.05:
                self.generate_tree(local_x, base_height)
            elif biome == 'desert' and random.random() < 0.08:
                self.generate_cactus(local_x, base_height)
    
    def generate_tree(self, x, base_y):
        """Génère un arbre"""
        height = random.randint(4, 7)
        
        # Tronc
        for y in range(base_y, base_y + height):
            self.blocks[(x, y)] = 'wood'
        
        # Feuilles
        crown_y = base_y + height
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if abs(dx) + abs(dy) < 4 and random.random() < 0.8:
                    leaf_y = crown_y + dy
                    if 0 <= x + dx < CHUNK_WIDTH and leaf_y < CHUNK_HEIGHT:
                        if (x + dx, leaf_y) not in self.blocks or self.blocks[(x + dx, leaf_y)] == 'air':
                            self.blocks[(x + dx, leaf_y)] = 'leaves'
    
    def generate_cactus(self, x, base_y):
        """Génère un cactus"""
        height = random.randint(2, 4)
        for y in range(base_y, base_y + height):
            self.blocks[(x, y)] = 'cactus'
    
    def get_block(self, x, y):
        return self.blocks.get((x, y), 'air')
    
    def set_block(self, x, y, block_type):
        if block_type == 'air':
            if (x, y) in self.blocks:
                del self.blocks[(x, y)]
        else:
            self.blocks[(x, y)] = block_type

class World:
    def __init__(self):
        self.chunks = {}
        self.spawn_point = (0, 100)
        
        # Pré-générer les chunks autour du spawn
        print("Pré-génération des chunks initiaux...")
        for chunk_x in range(-2, 3):
            self.get_chunk(chunk_x)
        print(f"{len(self.chunks)} chunks générés")
    
    def get_chunk(self, chunk_x):
        if chunk_x not in self.chunks:
            self.chunks[chunk_x] = Chunk(chunk_x)
        return self.chunks[chunk_x]
    
    def get_block(self, x, y):
        if y < 0 or y >= CHUNK_HEIGHT:
            return 'air'
        
        chunk_x = x // CHUNK_WIDTH
        local_x = x % CHUNK_WIDTH
        
        chunk = self.get_chunk(chunk_x)
        return chunk.get_block(local_x, y)
    
    def set_block(self, x, y, block_type):
        if y < 0 or y >= CHUNK_HEIGHT:
            return
        
        chunk_x = x // CHUNK_WIDTH
        local_x = x % CHUNK_WIDTH
        
        chunk = self.get_chunk(chunk_x)
        chunk.set_block(local_x, y, block_type)
    
    def find_spawn_point(self):
        """Trouve un point de spawn valide"""
        # Chercher un point de spawn sûr autour de x=0
        for x in range(-10, 11):
            for y in range(CHUNK_HEIGHT - 1, 20, -1):
                block_below = self.get_block(x, y)
                block_at = self.get_block(x, y + 1)
                block_above = self.get_block(x, y + 2)
                
                # Vérifier qu'il y a un sol solide et de l'espace au-dessus
                if (BLOCK_PROPERTIES[block_below]['solid'] and 
                    block_at == 'air' and 
                    block_above == 'air'):
                    self.spawn_point = (x * BLOCK_SIZE, y * BLOCK_SIZE)
                    print(f"Point de spawn trouvé: x={x}, y={y}")
                    return
        
        # Si aucun point trouvé, utiliser une position par défaut en hauteur
        self.spawn_point = (0, 60 * BLOCK_SIZE)
        print(f"Point de spawn par défaut: {self.spawn_point}")

class Particle:
    def __init__(self, x, y, color, vel_x=None, vel_y=None):
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = vel_x if vel_x is not None else random.uniform(-2, 2)
        self.vel_y = vel_y if vel_y is not None else random.uniform(-4, -1)
        self.lifetime = random.randint(20, 40)
        self.age = 0
        self.size = random.randint(2, 4)
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.2
        self.age += 1
        return self.age < self.lifetime
    
    def draw(self, screen, camera_x, camera_y):
        alpha = int(255 * (1 - self.age / self.lifetime))
        if alpha > 0:
            screen_x = int(self.x - camera_x)
            screen_y = int(self.y - camera_y)
            if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
                pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.size)

class Item:
    def __init__(self, item_type, count=1):
        self.type = item_type
        self.count = count
        self.max_stack = 64
    
    def add(self, amount):
        self.count = min(self.count + amount, self.max_stack)
    
    def remove(self, amount):
        self.count -= amount
        if self.count <= 0:
            return True
        return False

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 48
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.health = 20
        self.max_health = 20
        self.hunger = 20
        self.max_hunger = 20
        self.experience = 0
        self.level = 0
        
        # Inventaire
        self.inventory = defaultdict(int)
        self.inventory['wood'] = 10
        self.inventory['dirt'] = 10
        
        self.hotbar = ['dirt', 'stone', 'wood', 'planks', 'torch', 'crafting_table', 'furnace', 'cobblestone', 'glass']
        self.selected_slot = 0
        
        # Outils équipés
        self.tools = {
            'pickaxe': None,
            'axe': None,
            'shovel': None,
            'sword': None,
        }
        self.equipped_tool = None
        
        # États
        self.mining_block = None
        self.mining_progress = 0
        self.facing_right = True
        self.in_water = False
        self.game_mode = 'survival'  # 'survival' ou 'creative'
    
    def get_mining_speed(self, block_type):
        """Calcule la vitesse de minage selon l'outil équipé"""
        props = BLOCK_PROPERTIES[block_type]
        base_hardness = props['hardness']
        
        if base_hardness == 0:
            return 999
        
        # Vérifier si on a le bon outil
        required_tool = props['tool']
        if required_tool and self.equipped_tool:
            tool_type, tool_material = self.equipped_tool.split('_')
            
            if tool_type == required_tool:
                # Multiplicateurs selon le matériau
                multipliers = {
                    'wooden': 1.5,
                    'stone': 3.0,
                    'iron': 6.0,
                    'diamond': 12.0,
                }
                multiplier = multipliers.get(tool_material, 1.0)
                return (60 / base_hardness) * multiplier
        
        return 60 / base_hardness
    
    def update(self, world, keys, dt):
        # Mouvement horizontal
        self.vel_x = 0
        speed = 5 if not self.in_water else 2
        
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self.vel_x = -speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = speed
            self.facing_right = True
        
        # Sprint
        if keys[pygame.K_LSHIFT] and not self.in_water:
            self.vel_x *= 1.8
        
        self.x += self.vel_x
        
        # Collision horizontale
        self.check_collision_x(world)
        
        # Gravité
        gravity = 0.5 if not self.in_water else 0.1
        self.vel_y += gravity
        
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Saut
        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and (self.on_ground or self.in_water):
            self.vel_y = -12 if not self.in_water else -4
        
        self.y += self.vel_y
        self.on_ground = False
        
        # Collision verticale
        self.check_collision_y(world)
        
        # Sécurité: téléporter le joueur s'il tombe trop bas
        if self.y > CHUNK_HEIGHT * BLOCK_SIZE:
            print("Joueur tombé dans le vide, respawn...")
            world.find_spawn_point()
            self.x, self.y = world.spawn_point
            self.vel_y = 0
            self.health = self.max_health
        
        # Vérifier si dans l'eau
        self.check_water(world)
        
        # Dégâts environnementaux
        self.check_environmental_damage(world)
        
        # Faim
        if self.game_mode == 'survival':
            self.hunger -= 0.001
            if self.hunger < 0:
                self.hunger = 0
                self.health -= 0.01
            
            if self.health < 0:
                self.health = 0
    
    def check_collision_x(self, world):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        min_x = int((self.x - 5) // BLOCK_SIZE)
        max_x = int((self.x + self.width + 5) // BLOCK_SIZE)
        min_y = int(self.y // BLOCK_SIZE)
        max_y = int((self.y + self.height) // BLOCK_SIZE)
        
        for bx in range(min_x, max_x + 1):
            for by in range(min_y, max_y + 1):
                block = world.get_block(bx, by)
                if BLOCK_PROPERTIES[block]['solid']:
                    block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    if player_rect.colliderect(block_rect):
                        if self.vel_x > 0:
                            self.x = block_rect.left - self.width
                        elif self.vel_x < 0:
                            self.x = block_rect.right
                        player_rect.x = self.x
    
    def check_collision_y(self, world):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        min_x = int(self.x // BLOCK_SIZE)
        max_x = int((self.x + self.width) // BLOCK_SIZE)
        min_y = int((self.y - 5) // BLOCK_SIZE)
        max_y = int((self.y + self.height + 5) // BLOCK_SIZE)
        
        for bx in range(min_x, max_x + 1):
            for by in range(min_y, max_y + 1):
                block = world.get_block(bx, by)
                if BLOCK_PROPERTIES[block]['solid']:
                    block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    if player_rect.colliderect(block_rect):
                        if self.vel_y > 0:
                            self.y = block_rect.top - self.height
                            self.vel_y = 0
                            self.on_ground = True
                        elif self.vel_y < 0:
                            self.y = block_rect.bottom
                            self.vel_y = 0
                        player_rect.y = self.y
    
    def check_water(self, world):
        center_x = int((self.x + self.width // 2) // BLOCK_SIZE)
        center_y = int((self.y + self.height // 2) // BLOCK_SIZE)
        
        block = world.get_block(center_x, center_y)
        self.in_water = (block == 'water')
    
    def check_environmental_damage(self, world):
        if self.game_mode == 'creative':
            return
        
        feet_x = int((self.x + self.width // 2) // BLOCK_SIZE)
        feet_y = int((self.y + self.height) // BLOCK_SIZE)
        
        block = world.get_block(feet_x, feet_y)
        
        if block == 'lava':
            self.health -= 0.2
        elif block == 'cactus':
            self.health -= 0.05
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Corps
        body_color = (70, 130, 220)
        pygame.draw.rect(screen, body_color, (screen_x, screen_y + 16, self.width, 32))
        
        # Tête
        head_color = (255, 220, 180)
        pygame.draw.rect(screen, head_color, (screen_x + 4, screen_y, 16, 16))
        
        # Yeux
        eye_offset = 4 if self.facing_right else -4
        pygame.draw.rect(screen, WHITE, (screen_x + 8 + eye_offset, screen_y + 5, 3, 3))
        pygame.draw.rect(screen, WHITE, (screen_x + 13 + eye_offset, screen_y + 5, 3, 3))
        pygame.draw.circle(screen, (0, 100, 200), (screen_x + 9 + eye_offset, screen_y + 6), 1)
        pygame.draw.circle(screen, (0, 100, 200), (screen_x + 14 + eye_offset, screen_y + 6), 1)
        
        # Jambes
        pygame.draw.rect(screen, (50, 50, 150), (screen_x + 4, screen_y + 36, 7, 12))
        pygame.draw.rect(screen, (50, 50, 150), (screen_x + 13, screen_y + 36, 7, 12))
        
        # Bras
        arm_color = (255, 220, 180)
        if self.facing_right:
            pygame.draw.rect(screen, arm_color, (screen_x + self.width - 4, screen_y + 16, 4, 16))
        else:
            pygame.draw.rect(screen, arm_color, (screen_x, screen_y + 16, 4, 16))

class Mob:
    def __init__(self, x, y, mob_type):
        self.x = x
        self.y = y
        self.type = mob_type
        self.width = 24
        self.height = 32
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.health = 10
        self.max_health = 10
        self.damage = 1
        self.speed = 2
        self.ai_timer = 0
        self.facing_right = True
        
        if mob_type == 'zombie':
            self.color = (0, 120, 0)
            self.health = 20
            self.damage = 2
        elif mob_type == 'skeleton':
            self.color = (200, 200, 200)
            self.health = 15
            self.damage = 2
        elif mob_type == 'creeper':
            self.color = (50, 200, 50)
            self.health = 20
            self.damage = 10
            self.speed = 2.5
        elif mob_type == 'spider':
            self.color = (100, 50, 0)
            self.health = 16
            self.damage = 2
            self.speed = 3
    
    def update(self, world, player, dt):
        self.ai_timer += 1
        
        # IA: suivre le joueur
        distance_to_player = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        
        if distance_to_player < 400:
            if player.x > self.x:
                self.vel_x = self.speed
                self.facing_right = True
            else:
                self.vel_x = -self.speed
                self.facing_right = False
        else:
            self.vel_x *= 0.9
        
        self.x += self.vel_x
        self.check_collision_x(world)
        
        # Gravité
        self.vel_y += 0.5
        if self.vel_y > 15:
            self.vel_y = 15
        
        # Saut automatique
        if self.on_ground and abs(self.vel_x) > 0.5 and self.ai_timer % 30 == 0:
            self.vel_y = -10
        
        self.y += self.vel_y
        self.on_ground = False
        self.check_collision_y(world)
        
        # Attaquer le joueur
        if distance_to_player < 50:
            player.health -= self.damage * 0.01
        
        return self.health > 0
    
    def check_collision_x(self, world):
        mob_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        min_x = int((self.x - 5) // BLOCK_SIZE)
        max_x = int((self.x + self.width + 5) // BLOCK_SIZE)
        min_y = int(self.y // BLOCK_SIZE)
        max_y = int((self.y + self.height) // BLOCK_SIZE)
        
        for bx in range(min_x, max_x + 1):
            for by in range(min_y, max_y + 1):
                block = world.get_block(bx, by)
                if BLOCK_PROPERTIES[block]['solid']:
                    block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    if mob_rect.colliderect(block_rect):
                        if self.vel_x > 0:
                            self.x = block_rect.left - self.width
                        elif self.vel_x < 0:
                            self.x = block_rect.right
                        mob_rect.x = self.x
    
    def check_collision_y(self, world):
        mob_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        min_x = int(self.x // BLOCK_SIZE)
        max_x = int((self.x + self.width) // BLOCK_SIZE)
        min_y = int((self.y - 5) // BLOCK_SIZE)
        max_y = int((self.y + self.height + 5) // BLOCK_SIZE)
        
        for bx in range(min_x, max_x + 1):
            for by in range(min_y, max_y + 1):
                block = world.get_block(bx, by)
                if BLOCK_PROPERTIES[block]['solid']:
                    block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    if mob_rect.colliderect(block_rect):
                        if self.vel_y > 0:
                            self.y = block_rect.top - self.height
                            self.vel_y = 0
                            self.on_ground = True
                        elif self.vel_y < 0:
                            self.y = block_rect.bottom
                            self.vel_y = 0
                        mob_rect.y = self.y
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Corps
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width, self.height))
        
        # Détails selon le type
        if self.type == 'zombie':
            # Yeux rouges
            pygame.draw.circle(screen, (255, 0, 0), (screen_x + 8, screen_y + 8), 3)
            pygame.draw.circle(screen, (255, 0, 0), (screen_x + 16, screen_y + 8), 3)
        elif self.type == 'creeper':
            # Visage de creeper
            pygame.draw.rect(screen, (0, 0, 0), (screen_x + 6, screen_y + 6, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), (screen_x + 14, screen_y + 6, 4, 4))
            pygame.draw.rect(screen, (0, 0, 0), (screen_x + 10, screen_y + 14, 4, 6))
        
        # Barre de vie
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y - 8, self.width, 4))
        pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y - 8, int(self.width * health_ratio), 4))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minecraft Python - Version Complète")
        self.clock = pygame.time.Clock()
        
        # Monde
        print("Génération du monde...")
        self.world = World()
        
        print("Recherche d'un point de spawn...")
        self.world.find_spawn_point()
        
        # Joueur
        spawn_x, spawn_y = self.world.spawn_point
        self.player = Player(spawn_x, spawn_y)
        print(f"Joueur spawné à: ({spawn_x}, {spawn_y})")
        
        # Caméra
        self.camera_x = 0
        self.camera_y = 0
        
        # Particules
        self.particles = []
        
        # Mobs
        self.mobs = []
        self.mob_spawn_timer = 0
        
        # Temps
        self.time = 6000  # Commence le matin
        self.day_length = 24000
        
        # UI
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        
        # Menus
        self.show_inventory = False
        self.show_crafting = False
        self.show_debug = False
        
        # Stats
        self.fps = 60
    
    def get_time_phase(self):
        """Retourne la phase du jour (0-1, où 0=midi, 0.5=minuit)"""
        normalized = (self.time % self.day_length) / self.day_length
        return abs(math.cos(normalized * 2 * math.pi))
    
    def get_sky_color(self):
        phase = self.get_time_phase()
        
        if phase < 0.3:  # Jour
            return SKY_BLUE
        elif phase < 0.5:  # Coucher de soleil
            t = (phase - 0.3) / 0.2
            return tuple(int(SKY_BLUE[i] * (1-t) + SUNSET_SKY[i] * t) for i in range(3))
        elif phase < 0.7:  # Nuit
            t = (phase - 0.5) / 0.2
            return tuple(int(SUNSET_SKY[i] * (1-t) + NIGHT_SKY[i] * t) for i in range(3))
        else:  # Lever de soleil
            t = (phase - 0.7) / 0.3
            return tuple(int(NIGHT_SKY[i] * (1-t) + SKY_BLUE[i] * t) for i in range(3))
    
    def spawn_mob(self):
        if len(self.mobs) >= 15:
            return
        
        # Spawn à distance du joueur
        spawn_x = self.player.x + random.choice([-600, 600])
        spawn_y = self.player.y - 200
        
        mob_type = random.choice(['zombie', 'skeleton', 'creeper', 'spider'])
        self.mobs.append(Mob(spawn_x, spawn_y, mob_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # Touches de hotbar
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    self.player.selected_slot = int(event.unicode) - 1
                
                # Menus
                elif event.key == pygame.K_e:
                    self.show_inventory = not self.show_inventory
                    self.show_crafting = False
                elif event.key == pygame.K_c:
                    self.show_crafting = not self.show_crafting
                    self.show_inventory = False
                elif event.key == pygame.K_F3:
                    self.show_debug = not self.show_debug
                elif event.key == pygame.K_g:
                    self.player.game_mode = 'creative' if self.player.game_mode == 'survival' else 'survival'
                
                elif event.key == pygame.K_ESCAPE:
                    self.show_inventory = False
                    self.show_crafting = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.show_inventory and not self.show_crafting:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_x = int((mouse_x + self.camera_x) // BLOCK_SIZE)
                    world_y = int((mouse_y + self.camera_y) // BLOCK_SIZE)
                    
                    # Clic gauche: miner
                    if event.button == 1:
                        distance = math.sqrt(
                            ((world_x * BLOCK_SIZE - self.player.x) ** 2) +
                            ((world_y * BLOCK_SIZE - self.player.y) ** 2)
                        )
                        
                        if distance < 200:  # Portée de minage
                            self.player.mining_block = (world_x, world_y)
                            self.player.mining_progress = 0
                    
                    # Clic droit: placer
                    elif event.button == 3:
                        distance = math.sqrt(
                            ((world_x * BLOCK_SIZE - self.player.x) ** 2) +
                            ((world_y * BLOCK_SIZE - self.player.y) ** 2)
                        )
                        
                        if distance < 200:
                            selected_block = self.player.hotbar[self.player.selected_slot]
                            if self.player.inventory[selected_block] > 0:
                                current_block = self.world.get_block(world_x, world_y)
                                if current_block == 'air':
                                    self.world.set_block(world_x, world_y, selected_block)
                                    self.player.inventory[selected_block] -= 1
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.player.mining_block = None
                    self.player.mining_progress = 0
        
        return True
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        # Mettre à jour le joueur
        self.player.update(self.world, keys, dt)
        
        # Minage
        if self.player.mining_block and pygame.mouse.get_pressed()[0]:
            bx, by = self.player.mining_block
            block_type = self.world.get_block(bx, by)
            
            if block_type != 'air':
                mining_speed = self.player.get_mining_speed(block_type)
                self.player.mining_progress += mining_speed
                
                # Créer des particules pendant le minage
                if random.random() < 0.2:
                    px = bx * BLOCK_SIZE + random.randint(0, BLOCK_SIZE)
                    py = by * BLOCK_SIZE + random.randint(0, BLOCK_SIZE)
                    color = BLOCK_COLORS.get(block_type, WHITE)
                    self.particles.append(Particle(px, py, color))
                
                # Bloc miné
                if self.player.mining_progress >= 60:
                    # Donner le bloc au joueur
                    drop = block_type
                    if block_type == 'grass':
                        drop = 'dirt'
                    elif block_type == 'stone':
                        drop = 'cobblestone'
                    elif '_ore' in block_type:
                        drop = block_type
                    
                    self.player.inventory[drop] += 1
                    
                    # Particules de destruction
                    for _ in range(15):
                        px = bx * BLOCK_SIZE + random.randint(0, BLOCK_SIZE)
                        py = by * BLOCK_SIZE + random.randint(0, BLOCK_SIZE)
                        color = BLOCK_COLORS.get(block_type, WHITE)
                        self.particles.append(Particle(px, py, color))
                    
                    # Détruire le bloc
                    self.world.set_block(bx, by, 'air')
                    self.player.mining_block = None
                    self.player.mining_progress = 0
        
        # Mettre à jour les particules
        self.particles = [p for p in self.particles if p.update()]
        
        # Mettre à jour les mobs
        self.mobs = [mob for mob in self.mobs if mob.update(self.world, self.player, dt)]
        
        # Spawn de mobs
        phase = self.get_time_phase()
        if phase > 0.5:  # Nuit
            self.mob_spawn_timer += 1
            if self.mob_spawn_timer > 180:
                self.spawn_mob()
                self.mob_spawn_timer = 0
        
        # Temps
        self.time = (self.time + 1) % self.day_length
        
        # Caméra
        self.camera_x = self.player.x + self.player.width // 2 - WIDTH // 2
        self.camera_y = self.player.y + self.player.height // 2 - HEIGHT // 2
    
    def draw_block(self, screen, block_type, x, y):
        """Dessine un bloc à l'écran"""
        color = BLOCK_COLORS.get(block_type)
        if not color:
            return
        
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, color, rect)
        
        # Bordure 3D
        if BLOCK_PROPERTIES[block_type]['solid']:
            border_color = tuple(max(0, c - 30) for c in color)
            pygame.draw.rect(screen, border_color, rect, 1)
        
        # Effets spéciaux
        if block_type == 'grass':
            # Herbe sur le dessus
            grass_color = tuple(max(0, c - 40) for c in color)
            for i in range(4):
                gx = x + 4 + i * 8
                pygame.draw.line(screen, grass_color, (gx, y), (gx, y + 4), 1)
        
        elif block_type in ['water', 'lava']:
            # Animation fluide
            offset = (pygame.time.get_ticks() // 100 % 8)
            wave_color = tuple(min(255, c + 20) for c in color)
            for i in range(4):
                wy = y + i * 8 + offset
                pygame.draw.line(screen, wave_color, (x, wy), (x + BLOCK_SIZE, wy), 2)
        
        elif block_type == 'torch':
            # Flamme
            flame_colors = [(255, 255, 0), (255, 200, 50), (255, 150, 0)]
            for i, fc in enumerate(flame_colors):
                pygame.draw.circle(screen, fc, (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2 - i * 2), 4 - i)
    
    def draw_world(self, screen):
        # Calculer les blocs visibles
        min_x = int(self.camera_x // BLOCK_SIZE) - 1
        max_x = int((self.camera_x + WIDTH) // BLOCK_SIZE) + 1
        min_y = int(self.camera_y // BLOCK_SIZE) - 1
        max_y = int((self.camera_y + HEIGHT) // BLOCK_SIZE) + 1
        
        # Dessiner les blocs
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                block_type = self.world.get_block(x, y)
                
                if block_type != 'air':
                    screen_x = x * BLOCK_SIZE - int(self.camera_x)
                    screen_y = y * BLOCK_SIZE - int(self.camera_y)
                    self.draw_block(screen, block_type, screen_x, screen_y)
                    
                    # Afficher progression de minage
                    if self.player.mining_block == (x, y):
                        progress = self.player.mining_progress / 60
                        crack_surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                        crack_surf.set_alpha(int(150 * progress))
                        crack_surf.fill(WHITE)
                        screen.blit(crack_surf, (screen_x, screen_y))
    
    def draw_hud(self, screen):
        # Barre de vie
        heart_width = 20
        for i in range(10):
            x = 10 + i * (heart_width + 2)
            y = 10
            
            if i < self.player.health / 2:
                pygame.draw.circle(screen, (255, 0, 0), (x + heart_width // 2, y + heart_width // 2), heart_width // 2)
            else:
                pygame.draw.circle(screen, (100, 0, 0), (x + heart_width // 2, y + heart_width // 2), heart_width // 2, 2)
        
        # Barre de faim
        for i in range(10):
            x = 10 + i * (heart_width + 2)
            y = 40
            
            if i < self.player.hunger / 2:
                pygame.draw.rect(screen, (200, 150, 100), (x, y, heart_width, heart_width))
            else:
                pygame.draw.rect(screen, (100, 75, 50), (x, y, heart_width, heart_width), 2)
        
        # Hotbar
        hotbar_y = HEIGHT - 60
        slot_size = 50
        total_width = len(self.player.hotbar) * (slot_size + 5)
        start_x = (WIDTH - total_width) // 2
        
        for i, item_type in enumerate(self.player.hotbar):
            x = start_x + i * (slot_size + 5)
            
            # Fond
            if i == self.player.selected_slot:
                pygame.draw.rect(screen, (200, 200, 200), (x, hotbar_y, slot_size, slot_size))
            else:
                pygame.draw.rect(screen, (100, 100, 100), (x, hotbar_y, slot_size, slot_size))
            
            pygame.draw.rect(screen, WHITE, (x, hotbar_y, slot_size, slot_size), 2)
            
            # Item
            color = BLOCK_COLORS.get(item_type)
            if color:
                pygame.draw.rect(screen, color, (x + 10, hotbar_y + 10, 30, 30))
            
            # Quantité
            count = self.player.inventory.get(item_type, 0)
            if count > 0:
                count_text = self.font.render(str(count), True, WHITE)
                screen.blit(count_text, (x + 5, hotbar_y + 35))
            
            # Numéro
            num_text = self.font.render(str(i + 1), True, WHITE)
            screen.blit(num_text, (x + 5, hotbar_y - 20))
        
        # Infos
        phase = self.get_time_phase()
        time_str = "🌙 Nuit" if phase > 0.5 else "☀️ Jour"
        time_text = self.font.render(time_str, True, WHITE)
        screen.blit(time_text, (WIDTH - 100, 10))
        
        mode_text = self.font.render(f"Mode: {self.player.game_mode}", True, WHITE)
        screen.blit(mode_text, (WIDTH - 200, 40))
    
    def draw_debug(self, screen):
        if not self.show_debug:
            return
        
        debug_info = [
            f"FPS: {int(self.fps)}",
            f"Pos: ({int(self.player.x)}, {int(self.player.y)})",
            f"Block: ({int(self.player.x // BLOCK_SIZE)}, {int(self.player.y // BLOCK_SIZE)})",
            f"Chunks loaded: {len(self.world.chunks)}",
            f"Mobs: {len(self.mobs)}",
            f"Particles: {len(self.particles)}",
            f"On ground: {self.player.on_ground}",
            f"In water: {self.player.in_water}",
        ]
        
        y = 100
        for info in debug_info:
            text = self.font.render(info, True, WHITE)
            shadow = self.font.render(info, True, BLACK)
            screen.blit(shadow, (11, y + 1))
            screen.blit(text, (10, y))
            y += 25
    
    def draw_inventory(self, screen):
        if not self.show_inventory:
            return
        
        # Fond semi-transparent
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))
        
        # Titre
        title = self.title_font.render("INVENTAIRE", True, (255, 255, 100))
        screen.blit(title, (WIDTH // 2 - 150, 50))
        
        # Items
        y = 150
        for item_type, count in sorted(self.player.inventory.items()):
            if count > 0:
                # Icône du bloc
                color = BLOCK_COLORS.get(item_type, WHITE)
                pygame.draw.rect(screen, color, (WIDTH // 2 - 200, y, 30, 30))
                
                # Nom et quantité
                text = self.big_font.render(f"{item_type}: {count}", True, WHITE)
                screen.blit(text, (WIDTH // 2 - 150, y))
                
                y += 40
        
        # Instructions
        close_text = self.font.render("Appuyez sur E pour fermer", True, WHITE)
        screen.blit(close_text, (WIDTH // 2 - 150, HEIGHT - 50))
    
    def draw_crafting(self, screen):
        if not self.show_crafting:
            return
        
        # Fond
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))
        
        # Titre
        title = self.title_font.render("CRAFTING", True, (100, 255, 100))
        screen.blit(title, (WIDTH // 2 - 120, 50))
        
        # Recettes
        y = 120
        for item, recipe in CRAFTING_RECIPES.items():
            # Vérifier si on peut craft
            can_craft = True
            recipe_text = f"{item} -> "
            
            for mat, qty in recipe.items():
                if mat != 'output':
                    if self.player.inventory.get(mat, 0) < qty:
                        can_craft = False
                    recipe_text += f"{mat}x{qty} "
            
            output_qty = recipe.get('output', 1)
            recipe_text += f" = {output_qty}"
            
            # Afficher
            color = (100, 255, 100) if can_craft else (255, 100, 100)
            text = self.font.render(recipe_text, True, color)
            screen.blit(text, (100, y))
            
            # Bouton craft
            if can_craft:
                button_rect = pygame.Rect(WIDTH - 200, y - 5, 100, 30)
                pygame.draw.rect(screen, (50, 150, 50), button_rect)
                pygame.draw.rect(screen, WHITE, button_rect, 2)
                
                button_text = self.font.render("Craft", True, WHITE)
                screen.blit(button_text, (button_rect.x + 25, button_rect.y + 5))
                
                # Gérer le clic
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        # Consommer les ressources
                        for mat, qty in recipe.items():
                            if mat != 'output':
                                self.player.inventory[mat] -= qty
                        
                        # Donner l'item
                        self.player.inventory[item] += output_qty
                        pygame.time.wait(200)  # Éviter les clics multiples
            
            y += 35
            if y > HEIGHT - 100:
                break
        
        # Instructions
        close_text = self.font.render("Appuyez sur C pour fermer | G: Changer de mode", True, WHITE)
        screen.blit(close_text, (WIDTH // 2 - 250, HEIGHT - 40))
    
    def draw(self):
        # Ciel
        self.screen.fill(self.get_sky_color())
        
        # Monde
        self.draw_world(self.screen)
        
        # Particules
        for particle in self.particles:
            particle.draw(self.screen, self.camera_x, self.camera_y)
        
        # Mobs
        for mob in self.mobs:
            mob.draw(self.screen, self.camera_x, self.camera_y)
        
        # Joueur
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        
        # HUD
        self.draw_hud(self.screen)
        
        # Debug
        self.draw_debug(self.screen)
        
        # Menus
        self.draw_inventory(self.screen)
        self.draw_crafting(self.screen)
        
        # Game Over
        if self.player.health <= 0:
            game_over_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
            screen_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(game_over_text, screen_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.fps = self.clock.get_fps()
            
            running = self.handle_events()
            
            if self.player.health > 0:
                self.update(dt)
            
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("🎮 Minecraft Python - Version Complète")
    print("=" * 50)
    print("CONTRÔLES:")
    print("  Q/D ou ←/→ : Se déplacer")
    print("  ESPACE : Sauter")
    print("  SHIFT : Sprint")
    print("  1-9 : Sélectionner hotbar")
    print("  E : Inventaire")
    print("  C : Crafting")
    print("  G : Changer de mode (Survival/Creative)")
    print("  F3 : Debug info")
    print("  Clic gauche : Miner")
    print("  Clic droit : Placer")
    print("  ÉCHAP : Quitter les menus")
    print("=" * 50)
    print("Chargement du monde...")
    
    game = Game()
    game.run()