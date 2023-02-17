import pygame
from pygame.locals import *
import sys

WIDTH = 800
HEIGHT = 450

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 14)

# pygame.mixer.music.load('')
# pygame.mixer.music.play(-1)

class Button():
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
    def update(self):
        mousePos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and mousePos[0] >= self.x - self.width / 2 and mousePos[0] <= self.x + self.width / 2 and mousePos[1] >= self.y - self.height / 2 and mousePos[1] <= self.y + self.height / 2:
            return self.name
        surf = pygame.Surface((self.width, self.height))
        surf.fill((255, 255, 255))
        rect = surf.get_rect(center = (self.x, self.y))
        text = font.render(self.name, True, (0, 0, 0))
        textRect = text.get_rect(center = (self.x, self.y + 40))
        screen.blit(surf, rect)
        screen.blit(text, textRect)


fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
buttons = []
buttonNames = ["Library", "Minesweeper", "Tic Tac Toe", "Pong", "Rock Paper Scissors", "Space Invaders", "Snake"]
running = buttonNames[0]
buttons.append(Button(60, 15, 100, 20, buttonNames[0]))
for i in range(3):
    for j in range(2):
        buttons.append(Button(175 + 225 * i, 135 + 180 * j, 150, 120, buttonNames[1 + i * 2 + j]))
while running:
    print(running)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    pygame.display.set_caption(running)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
    if running == buttonNames[0]:
        for i in buttons:
            x = i.update()
            if x:
                running = x
                break
    else:
        if buttons[0].update():
            running = buttonNames[0]
            continue
        
        
    pygame.display.flip()
    fpsClock.tick(fps)


pygame.quit()
sys.exit()