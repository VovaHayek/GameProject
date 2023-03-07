import pygame
import os

#GAME VARIABLES
pygame.init()
WIDTH, HEIGHT = 550, 900
BG = (180, 228, 255)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


CHARACTER_IMAGE = pygame.image.load(os.path.join('images', 'character.png'))
CHARACTER_HEIGHT = 171
CHARACTER_WIDTH = 124
CHARACTER = pygame.transform.scale(CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

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
        if keys_pressed[0]: #LEFT
            self.KITTY.x = mouse_x-(CHARACTER_WIDTH/2)
        if keys_pressed[0]:
            self.KITTY.y = mouse_y-(CHARACTER_HEIGHT/2)

        if keys_pressed[0] and mouse_x <= CHARACTER_WIDTH/2:
            self.KITTY.x = 0
        if keys_pressed[0] and mouse_x >= WIDTH-(CHARACTER_WIDTH/2):
            self.KITTY.x = WIDTH-CHARACTER_WIDTH

        if keys_pressed[0] and mouse_y <= CHARACTER_HEIGHT/2:
            self.KITTY.y = 0
        if keys_pressed[0] and mouse_y >= HEIGHT-(CHARACTER_HEIGHT/2):
            self.KITTY.y = HEIGHT-CHARACTER_HEIGHT
#Activating Player class
player = Player()

class StartGame:
    def __init__(self):
        self.FPS = 240
    def main(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys_pressed = pygame.mouse.get_pressed()
            player.character_movement(keys_pressed)

            self.draw_window()

        pygame.quit()
    
    def draw_window(self):
        WINDOW.fill(BG)
        player.create_player()
        pygame.display.update()

if __name__ == "__main__":
    start = StartGame()
    start.main()