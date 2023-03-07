import pygame
import random
import time
import os

#GAME VARIABLES
pygame.init()
WIDTH, HEIGHT = 550, 900
BG = (180, 228, 255)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
START_TIME = pygame.time.get_ticks()

#Character options
CHARACTER_IMAGE = pygame.image.load(os.path.join('images', 'character.png'))
CHARACTER_HEIGHT = 171
CHARACTER_WIDTH = 124
CHARACTER = pygame.transform.scale(CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

#Enemy options
ENEMY_LIST = []
ENEMY_IMAGE = pygame.image.load(os.path.join('images', 'enemy.png'))
ENEMY_WIDTH = 133
ENEMY_HEIGHT = 60
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

class Player:
    def __init__(self):
        self.Y_POS = 630
        self.X_POS = 213
        self.KITTY = pygame.Rect(self.X_POS, self.Y_POS, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    def create_player(self):
        """Spawns character when game's started, and updates position of character when cursor moved"""
        WINDOW.blit(CHARACTER, (self.KITTY.x, self.KITTY.y))

    def character_movement(self, keys_pressed):
        """Character's movement functionality"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if keys_pressed[0]:
            self.KITTY.x = mouse_x-(CHARACTER_WIDTH/2)
        if keys_pressed[0]:
            self.KITTY.y = mouse_y-(CHARACTER_HEIGHT/2)

        if keys_pressed[0] and mouse_x <= CHARACTER_WIDTH/2:
            self.KITTY.x = 0
        if keys_pressed[0] and mouse_x >= WIDTH-(CHARACTER_WIDTH/2):
            self.KITTY.x = WIDTH-CHARACTER_WIDTH

        if keys_pressed[0] and mouse_y <= (WIDTH/2)+CHARACTER_HEIGHT:
            self.KITTY.y = (WIDTH/2)+(CHARACTER_HEIGHT/2)
        if keys_pressed[0] and mouse_y >= HEIGHT-(CHARACTER_HEIGHT/2):
            self.KITTY.y = HEIGHT-CHARACTER_HEIGHT
#Activating Player class
player = Player()

class Enemy:
    def __init__(self):
        self.X_POS = random.randint(0, 500)
        self.Y_POS = -ENEMY_HEIGHT
        self.SPEED_TIME = pygame.time.get_ticks()
        self.ENEMY_SPEED = 3

    def create_enemy(self):
        if len(ENEMY_LIST) < 10:
            BIRD = pygame.Rect(random.randint(0, 400), self.Y_POS, ENEMY_WIDTH, ENEMY_HEIGHT)
            ENEMY_LIST.append(BIRD)
    
    def spawn_enemies(self):
        for index, enemy in enumerate(ENEMY_LIST):
            WINDOW.blit(ENEMY, (enemy.x, enemy.y))
            self.slide_down(enemy, index)

    def slide_down(self, enemy, enemy_id):
        if pygame.time.get_ticks() >= self.SPEED_TIME:
            self.SPEED_TIME = pygame.time.get_ticks()
            enemy.y += self.ENEMY_SPEED
            if enemy.y > 200 and enemy.y < 203:
                self.create_enemy()
            if enemy.y > 900:
                ENEMY_LIST.pop(enemy_id)
            
#Activating Enemy class
enemies = Enemy()


class StartGame:
    def __init__(self):
        self.FPS = 120
    def main(self):
        clock = pygame.time.Clock()
        run = True
        enemies.create_enemy()
        while run:
            clock.tick(self.FPS)
            NOW_TIME = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys_pressed = pygame.mouse.get_pressed()
            player.character_movement(keys_pressed)


            self.draw_window()

        pygame.quit()
    
    def draw_window(self):
        """Updating game window"""
        WINDOW.fill(BG)
        player.create_player()
        enemies.spawn_enemies()
        pygame.display.update()

if __name__ == "__main__":
    start = StartGame()
    start.main()