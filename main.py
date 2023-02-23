import pygame
from pygame.locals import *
import sys
import random
import time
import math

WIDTH = 800
HEIGHT = 450

PONG_WIDTH = 10
PONG_HEIGHT = 30

BALL_WIDTH = 5
BALL_HEIGHT = 5

INVADER_HEIGHT = 26
INVADER_LENGTH = 30

INVADER_GAP = 12

BULLET_LENGTH = 2
BULLET_HEIGHT = 8
DEFENDER_HEIGHT = 15
DEFENDER_LENGTH = 60

SPEED = 0.3

variables = [SPEED]
bullets = []
invaders = []

# LOSE = pygame.mixer.Sound("mixkit-player-losing-or-failing-2042.wav")
# SHOOT = pygame.mixer.Sound("mixkit-video-game-retro-click-237.wav")
# pygame.mixer.music.load('music.wav')
# pygame.mixer.music.play(-1)
# HIT = pygame.mixer.Sound("mixkit-fast-game-explosion-1688.wav")

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 14)

def createBullet(x, y, screen, team):
	if team == 1:
		target = invaders
	if team == 2:
		target = player
	bullets.append(Bullet(x, y, screen, target))

def resetInvaders():
	for i in range(10):
		for j in range(6):
			invaders.append(Invader(10 + i * (INVADER_GAP + INVADER_LENGTH), 0 + j * (INVADER_GAP + INVADER_HEIGHT), screen, variables))


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, screen, target):
		super(Bullet, self).__init__()
		self.x = x
		self.y = y
		self.screen = screen
		self.target = target
		self.speed = 2
		self.surf = pygame.Surface((BULLET_LENGTH, BULLET_HEIGHT))
		self.surf.fill((255, 0, 0))
		if type(self.target) == list:
			self.speed = -2
    
	def update(self):
		if self.y < 0 or self.y > HEIGHT:
			return 1
		else:
			self.y += self.speed
			if type(self.target) == list:
				for i in self.target:
					if self.x > i.x - BULLET_LENGTH and self.x < i.x + INVADER_LENGTH and self.y + BULLET_HEIGHT > i.y and self.y < i.y + INVADER_HEIGHT:
						# pygame.mixer.Sound.play(HIT)
						return i
			else:
				if self.x > self.target.x - BULLET_LENGTH and self.x < self.target.x + DEFENDER_LENGTH and self.y + BULLET_HEIGHT > self.target.y and self.y < self.target.y + DEFENDER_HEIGHT:
					# pygame.mixer.Sound.play(HIT)
					self.target.lives -= 1
					return 1
			self.screen.blit(self.surf, (self.x, self.y))

class Character(pygame.sprite.Sprite):
	def __init__(self, x, y, screen, lives):
		super(Character, self).__init__()
		self.x = x
		self.y = y
		self.screen = screen
		self.lives = lives

class Invader(Character):
	def __init__(self, x, y, screen, variables):
		super().__init__(x, y, screen, 1)
		self.team = 2
		self.img = pygame.image.load("invader.jpg")
		self.img = pygame.transform.rotozoom(self.img, 0, 0.175)
		# self.surf = pygame.Surface((INVADER_LENGTH, INVADER_HEIGHT))
		# self.surf.fill((255, 255, 255))
		self.variables = variables
		self.prev = 1
    
	def update(self, level):
		if self.prev != self.variables[0]:
			self.y = self.y + INVADER_HEIGHT + INVADER_GAP
		self.x = self.x + self.variables[0]
		if self.x <= 0 or self.x >= WIDTH - INVADER_LENGTH:
			self.variables[0] *= -1
			self.y = self.y + INVADER_HEIGHT + INVADER_GAP
		self.prev = self.variables[0]
		self.screen.blit(self.img, (self.x, self.y))
		# self.screen.blit(self.surf, (self.x, self.y))
		if self.y > 400:
			return 1

		if random.randint(1, 10000) <= level:
			createBullet(self.x + INVADER_LENGTH / 2, self.y + INVADER_HEIGHT, self.screen, self.team)

class Defender(Character):
	def __init__(self, x, y, screen):
		super().__init__(x, y, screen, 3)
		self.team = 1
		self.surf = pygame.Surface((DEFENDER_LENGTH, DEFENDER_HEIGHT))
		self.surf.fill((255, 255, 255))
		self.time = -1
	def update(self, pressed_keys):
		if pressed_keys[K_LEFT]:
			self.x = self.x - 5
			if self.x < 0:
				self.x = 0
		if pressed_keys[K_RIGHT]:
			self.x = self.x + 5
			if self.x > WIDTH - DEFENDER_LENGTH:
				self.x = WIDTH - DEFENDER_LENGTH
		if pressed_keys[K_SPACE] and time.time() - self.time > 0.40:
			# pygame.mixer.Sound.play(SHOOT)
			createBullet(self.x + DEFENDER_LENGTH / 2, self.y + DEFENDER_HEIGHT - BULLET_HEIGHT, self.screen, self.team)
			self.time = time.time()
		self.screen.blit(self.surf, (self.x, self.y))

class SuperInvader(Invader):
	def __init__(self, screen):
		super().__init__(-50,0, screen, [3])
	def update(self, level):
		if self.prev != self.variables[0]:
			self.y = self.y + INVADER_HEIGHT + INVADER_GAP
		self.x = self.x + self.variables[0]
		self.prev = self.variables[0]
		self.screen.blit(self.img, (self.x, self.y))
		if self.x > 900:
			return 1000
		if self.y > 800:
			return 1

class PongPlayer():
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.surf = pygame.Surface((PONG_WIDTH, PONG_HEIGHT))
        self.surf.fill((255, 255, 255))
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.y = self.y - 5
            if self.y < 0:
            	self.y = 0
        if pressed_keys[K_DOWN]:
            self.y = self.y + 5
            if self.y > HEIGHT - PONG_HEIGHT:
                self.y = HEIGHT - PONG_HEIGHT
        self.screen.blit(self.surf, (self.x, self.y))

class PongBall():
    def __init__(self, x, y, screen):
        self.x = WIDTH // 2
        self.y = y
        self.screen = screen
        self.surf = pygame.Surface((PONG_WIDTH, PONG_HEIGHT))
        self.surf.fill((255, 255, 255))
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.y = self.y - 5
            if self.y < 0:
            	self.y = 0
        if pressed_keys[K_DOWN]:
            self.y = self.y + 5
            if self.y > HEIGHT - PONG_HEIGHT:
                self.y = HEIGHT - PONG_HEIGHT
        self.screen.blit(self.surf, (self.x, self.y))

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
        if self.name == buttonNames[0]:
            text = font.render("<---" + self.name, True, (0, 0, 0))
            textRect = text.get_rect(center = (self.x, self.y))
        else:
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
score = 0
player = Defender(30, 400, screen)
gameOver = False

p1 = PongPlayer(760, 220, screen)
p2 = PongPlayer(40, 220, screen)


prerunning = running
while running:
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    pygame.display.set_caption(running)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
    if running == buttonNames[0]:
        for i in buttons[1:]:
            x = i.update()
            if x:
                running = x
                break
    else:
        if buttons[0].update():
            running = buttonNames[0]
            continue
        if running == buttonNames[3]:
            p1.update(pygame.key.get_pressed())
            p2.update(pygame.key.get_pressed())
        if running == buttonNames[5]:
            if gameOver:
                if pygame.key.get_pressed()[K_r]:
                    gameOver = False
                    score = 0
                    newHighScore = False
                    invaders = []
                    bullets = []
                    player = Defender(30, 400, screen)
                    continue

                gameOverText = font.render(f'Game Over', True, (255, 0, 0))
                gameOverTextRect = gameOverText.get_rect()
                gameOverTextRect.center = (WIDTH // 2, HEIGHT // 2 - 80)
                screen.blit(gameOverText, gameOverTextRect)

                playAgainText = font.render(f'Press R to restart', True, (255, 0, 0))
                playAgainTextRect = playAgainText.get_rect()
                playAgainTextRect.center = (WIDTH // 2, HEIGHT // 2 - 40)
                screen.blit(playAgainText, playAgainTextRect)

                scoreText = font.render(f'Score: {score}', True, (0, 0, 255))
                scoreTextRect = scoreText.get_rect()
                scoreTextRect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(scoreText, scoreTextRect)
                pygame.display.flip()
                fpsClock.tick(fps)
                continue
            if len(invaders) == 0:
                resetInvaders()
            if random.randint(1, 2000) == 1:
                invaders.append(SuperInvader(screen))
            pressed_keys = pygame.key.get_pressed()
            level = min([score // 100 + 1])
            for i in invaders:
                x = i.update(level)
                if x == 1:
                    lives = 0
                    gameOver = True
                    # pygame.mixer.Sound.play(LOSE)
                    continue
                elif x == 1000:
                    invaders.remove(i)
            
            for i in bullets:
                x = i.update()
                if x:
                    bullets.remove(i)
                if type(x) == Invader:
                    invaders.remove(x)
                    score += 10
                elif type(x) == SuperInvader:
                    invaders.remove(x)
                    score += 100
            scoreText = font.render(f'Score: {score}', True, (0, 0, 255))
            livesText = font.render(f'Lives: {player.lives}', True, (0, 0, 255))
            scoreTextRect = scoreText.get_rect()
            livesTextRect = livesText.get_rect()
            scoreTextRect.midleft = (130, 15)
            livesTextRect.midright = (780, 15)
            screen.blit(scoreText, scoreTextRect)
            screen.blit(livesText, livesTextRect)
            if player.lives == 0:
                gameOver = True
                # pygame.mixer.Sound.play(LOSE)
            player.update(pressed_keys)

        
    prerunning = running
    pygame.display.flip()
    fpsClock.tick(fps)


pygame.quit()
sys.exit()