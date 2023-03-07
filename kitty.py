import pygame
import os

#GAME VARIABLES
WIDTH, HEIGHT = 550, 900
BG = (180, 228, 255)
FPS = 120
VELOCITY = 3
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CHARACTER_IMAGE = pygame.image.load(os.path.join('images', 'hayek.png'))
CHARACTER_HEIGHT = 171
CHARACTER_WIDTH = 124
CHARACTER = pygame.transform.scale(CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

def character_movement(keys_pressed, kitty):
    if keys_pressed[pygame.K_LEFT] and kitty.x - VELOCITY > 0: #LEFT
        kitty.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and kitty.x + VELOCITY + CHARACTER_WIDTH < WIDTH: #RIGHT
        kitty.x += VELOCITY
    if keys_pressed[pygame.K_UP] and kitty.y - VELOCITY > 0: #UP
        kitty.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and kitty.y + VELOCITY + CHARACTER_HEIGHT-(CHARACTER_HEIGHT/3) < HEIGHT: #DOWN
        kitty.y += VELOCITY

def draw_window(kitty):
    WINDOW.fill(BG)
    WINDOW.blit(CHARACTER, (kitty.x, kitty.y))
    pygame.display.update()

def main():
    kitty = pygame.Rect(213, 630, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        character_movement(keys_pressed, kitty)

        draw_window(kitty)

    pygame.quit()

if __name__ == "__main__":
    main()