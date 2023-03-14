import pygame
import random
import time
import os

#GAME VARIABLES
pygame.init()
WIDTH, HEIGHT = 550, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#Background options
BG = pygame.image.load('images/moving-background.png').convert()
BG_WIDTH = BG.get_width()
BG_HEIGHT = BG.get_height()
BG_Y = 0
BG_TILES = 3
BG_SCROLL = 0

START_TIME = pygame.time.get_ticks()
SCORE = 0

#Character options
CHARACTER_IMAGE = pygame.image.load(os.path.join('images', 'character.png'))
CHARACTER_HEIGHT = 130
CHARACTER_WIDTH = 80
CHARACTER = pygame.transform.scale(CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

#Enemy options
ENEMY_LIST = []
ENEMY_IMAGE = pygame.image.load(os.path.join('images', 'enemy.png'))
ENEMY_WIDTH = 133
ENEMY_HEIGHT = 60
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

#GAME FUNCTIONS CLASS
class GameFunctions():
    def restart(self):
        global SCORE

        ENEMY_LIST.clear()
        player.KITTY.x = player.X_POS
        player.KITTY.y = player.Y_POS
        SCORE = 0
        start.main()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    def moving_background(self):
        global BG_SCROLL
        for i in range(1, BG_TILES+1):
            WINDOW.blit(BG, (-(BG_WIDTH/2), -(i*BG_HEIGHT-HEIGHT)+BG_SCROLL))
        BG_SCROLL += 1
        if BG_SCROLL > BG_HEIGHT:
            BG_SCROLL = 0

    def score_display(self):
        global SCORE

        GAME_OVER_TEXT = pygame.font.SysFont("comicsansms",35)
        TEXT_SURF, TEXT_RECT = self.text_objects(str(SCORE), GAME_OVER_TEXT)
        TEXT_RECT.center = (35, 35)
        WINDOW.blit(TEXT_SURF, TEXT_RECT)

    def game_over(self):
        GAME_OVER_TEXT = pygame.font.SysFont("comicsansms",115)
        TEXT_SURF, TEXT_RECT = self.text_objects("Paused", GAME_OVER_TEXT)
        TEXT_RECT.center = ((WIDTH/2), (HEIGHT/4))
        WINDOW.blit(TEXT_SURF, TEXT_RECT)

        while True:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.button("Play Again",150,450,100,50,(214, 19, 85),(249, 74, 41),self.restart)

            pygame.display.update()

    def button(self, msg, x, y, width, height, i_color, a_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(WINDOW, a_color, (x, y, width, height))
            if click[0] == True and action != None:
                action()
        else:
            pygame.draw.rect(WINDOW, i_color, (x, y, width, height))
        SMALL_TEXT = pygame.font.SysFont("comicsansms",20)
        TEXT_SURF, TEXT_RECT = self.text_objects(msg, SMALL_TEXT)
        TEXT_RECT.center = ((x+(width/2)), (y+(height/2)))
        WINDOW.blit(TEXT_SURF, TEXT_RECT)
game_functions = GameFunctions()


#PLAYER CLASS
class Player():
    def __init__(self):
        #super(Player, self).__init__()
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
player = Player()

class Enemy(object):
    def __init__(self):
        self.X_POS = random.randint(0, 500)
        self.Y_POS = -ENEMY_HEIGHT
        self.SPEED_TIME = pygame.time.get_ticks()
        self.ENEMY_SPEED = 2

    def create_enemy(self):
        if len(ENEMY_LIST) < 10:
            BIRD = pygame.Rect(random.randint(0, 400), self.Y_POS, ENEMY_WIDTH, ENEMY_HEIGHT)
            ENEMY_LIST.append(BIRD)
    
    def spawn_enemies(self):
        for index, enemy in enumerate(ENEMY_LIST):
            WINDOW.blit(ENEMY, (enemy.x, enemy.y))
            if player.KITTY.colliderect(enemy):
                game_functions.game_over()
            self.slide_down(enemy, index)
        for index, enemy in enumerate(ENEMY_LIST):
            return enemy


    def slide_down(self, enemy, enemy_id):
        global SCORE

        if pygame.time.get_ticks() > self.SPEED_TIME:
            self.SPEED_TIME >= pygame.time.get_ticks()
            enemy.y += self.ENEMY_SPEED
            if enemy.y > 200 and enemy.y < 203:
                self.create_enemy()
            if enemy.y > 900:
                SCORE += 1
                ENEMY_LIST.pop(enemy_id)
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
        game_functions.moving_background()
        game_functions.score_display()
        player.create_player()
        enemies.spawn_enemies()
        pygame.display.update()

if __name__ == "__main__":
    start = StartGame()
    start.main()