import pygame
import random
import time
import os
import sys

#GAME VARIABLES
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 550, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

#Background options
BG = pygame.image.load('images/moving-background.png').convert()
BG_WIDTH = BG.get_width()
BG_HEIGHT = BG.get_height()
BG_Y = 0
BG_TILES = 3
BG_SCROLL = 0

SCORE = 0

#GAME FUNCTIONS CLASS
class GameFunctions():
    def restart(self):
        global SCORE

        all_sprites.empty()
        enemies_sprites.empty()
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


#Sprite lists
all_sprites = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()

#PLAYER CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.player_image = pygame.image.load(os.path.join('images', 'character.png'))
        self.image = pygame.transform.scale(self.player_image, (80, 130))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-100

    def character_movement(self, keys_pressed):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if keys_pressed[0]:
            self.rect.centerx = mouse_x
        if keys_pressed[0]:
            self.rect.centery = mouse_y

        if keys_pressed[0] and mouse_x <= self.rect.width/2:
            self.rect.x = 0
        if keys_pressed[0] and mouse_x >= WIDTH-(self.rect.width/2):
            self.rect.x = WIDTH-self.rect.width

        if keys_pressed[0] and mouse_y <= (WIDTH/2)+self.rect.height:
            self.rect.y = (WIDTH/2)+(self.rect.height/2)
        if keys_pressed[0] and mouse_y >= HEIGHT-(self.rect.height/2):
            self.rect.y = HEIGHT-self.rect.height

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.enemy_image = pygame.image.load(os.path.join('images', 'enemy.png')).convert()
        self.enemy_image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.enemy_image, (133, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(random.randint(0, 100), random.randint(300, 417))
        self.rect.bottom = 0

    def update(self):
        self.rect.y += 2
        if self.rect.y > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(5, 400)

    def add_enemies(self, enemy):
        enemies_sprites.add(enemy)
        all_sprites.add(enemy)

player = Player()
enemies = Enemy()
game_functions = GameFunctions()
class StartGame:
    def __init__(self):
        self.FPS = 120
        self.last_spawn = pygame.time.get_ticks()
    def main(self):
        clock = pygame.time.Clock()
        run = True

        all_sprites.add(player)

        while run:
            clock.tick(self.FPS)
            NOW_TIME = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys_pressed = pygame.mouse.get_pressed()
            player.character_movement(keys_pressed)

            if pygame.sprite.spritecollide(player, enemies_sprites, True, pygame.sprite.collide_mask):
                game_functions.game_over()

            self.draw_window()

        pygame.quit()

    def create_enemies(self):
        global SCORE
        now = pygame.time.get_ticks()
        if len(enemies_sprites) < 5:
            if now - self.last_spawn >= 800:
                enemies.add_enemies(Enemy())
                self.last_spawn = now
        for enemy in enemies_sprites:
            if enemy.rect.y > HEIGHT-1:
                SCORE += 1

    def draw_window(self):
        """Updating game window"""
        game_functions.moving_background()
        game_functions.score_display()
        self.create_enemies()
        all_sprites.update()
        all_sprites.draw(WINDOW)
        pygame.display.update()

if __name__ == "__main__":
    start = StartGame()
    start.main()