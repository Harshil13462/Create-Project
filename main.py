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

TTTLENGTH = 100

INVADER_GAP_HORIZONTAL = 30
INVADER_GAP = 12

BULLET_LENGTH = 2
BULLET_HEIGHT = 8
DEFENDER_HEIGHT = 15
DEFENDER_LENGTH = 60

SPEED = 0.3

variables = [SPEED]
bullets = []
invaders = []

pygame.init()

pygame.mixer.music.load('music.wav')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

font = pygame.font.Font('freesansbold.ttf', 14)

def createBullet(x, y, screen, team):
	if team == 1:
		target = invaders
	if team == 2:
		target = player
	bullets.append(Bullet(x, y, screen, target))

def resetInvaders():
	for i in range(8):
		for j in range(5):
			invaders.append(Invader(10 + i * (INVADER_GAP_HORIZONTAL + INVADER_LENGTH), 0 + j * (INVADER_GAP + INVADER_HEIGHT), screen, variables))


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
						return i
			else:
				if self.x > self.target.x - BULLET_LENGTH and self.x < self.target.x + DEFENDER_LENGTH and self.y + BULLET_HEIGHT > self.target.y and self.y < self.target.y + DEFENDER_HEIGHT:
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
    def __init__(self, x, y, screen, player):
        self.player = player
        self.x = x
        self.y = y
        self.screen = screen
        self.surf = pygame.Surface((PONG_WIDTH, PONG_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.lives = 3
    def update(self, pressed_keys):
        if self.player == 1:
            if pressed_keys[K_w]:
                self.y = self.y - 5
            if pressed_keys[K_s]:
                self.y = self.y + 5
        else:
            if pressed_keys[K_UP]:
                self.y = self.y - 5
            if pressed_keys[K_DOWN]:
                self.y = self.y + 5
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - PONG_HEIGHT:
            self.y = HEIGHT - PONG_HEIGHT
        self.screen.blit(self.surf, (self.x, self.y))

class PongBall():
    def __init__(self, screen):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.xSpeed = (random.random() + 0.5) * (1 if random.random() < 0.5 else -1)
        self.ySpeed = random.random() - 0.5 * 2
        self.screen = screen
        self.surf = pygame.Surface((BALL_WIDTH, BALL_HEIGHT))
        self.surf.fill((255, 255, 255))
    def update(self, p1, p2):
        self.x = self.x + self.xSpeed
        self.y = self.y + self.ySpeed
        if self.y < 0:
            self.y = 0
            self.ySpeed = -1 * self.ySpeed
        if self.y > HEIGHT - BALL_HEIGHT:
            self.y = HEIGHT - BALL_HEIGHT
            self.ySpeed = -1 * self.ySpeed
        if self.x <= p1.x + PONG_WIDTH and self.x >= p1.x and self.y >= p1.y and self.y <= p1.y + PONG_HEIGHT:
            self.xSpeed = -1 * self.xSpeed
            if abs(self.xSpeed) < 10:
                self.xSpeed *= 1.2
                self.ySpeed *= 1.2
        if self.x <= p2.x + PONG_WIDTH and self.x + BALL_WIDTH >= p2.x and self.y >= p2.y and self.y <= p2.y + PONG_HEIGHT:
            self.xSpeed = -1 * self.xSpeed
            if abs(self.xSpeed) < 10:
                self.xSpeed *= 1.2
                self.ySpeed *= 1.2
        if self.x < 0:
            return 1
        if self.x > WIDTH:
            return 2
        self.screen.blit(self.surf, (self.x, self.y))

class C4Board():
    def __init__(self, screen):
        self.screen = screen
        self.places = [[0 for i in range(6)] for i in range(7)]
        self.time = -1
        self.turn = 1
    
    def update(self):
        for i in range(7):
            for j in range(3):
                if self.places[i][j] != 0 and self.places[i][j] == self.places[i][j + 1] and self.places[i][j] == self.places[i][j + 2] and self.places[i][j] == self.places[i][j + 3]:
                    return self.places[i][j]
        for i in range(6):
            for j in range(4):
                if self.places[j][i] != 0 and self.places[j][i] == self.places[j + 1][i] and self.places[j][i] == self.places[j + 2][i] and self.places[j][i] == self.places[j + 3][i]:
                    return self.places[j][i]
        for i in range(4):
            for j in range(3):
                if self.places[i][j] != 0 and self.places[i][j] == self.places[i + 1][j + 1] and self.places[i][j] == self.places[i + 2][j + 2] and self.places[i][j] == self.places[i + 3][j + 3]:
                    return self.places[i][j]
                if self.places[6 - i][j] != 0 and self.places[6 - i][j] == self.places[5 - i][j + 1] and self.places[6 - i][j] == self.places[4 - i][j + 2] and self.places[6 - i][j] == self.places[3 - i][j + 3]:
                    return self.places[6 - i][j]
        
        if self.time == -1:
            self.time = time.time()
        for i in range(8):
            pygame.draw.line(self.screen, (255, 255, 255), (240 + i * 50, 50), (240 + i * 50, 350))
            
        for i in range(7):
            pygame.draw.line(self.screen, (255, 255, 255), (240, 50 + i * 50), (590, 50 + i * 50))
        
        for i in range(7):
            for j in range(6):
                if self.places[i][j] == 1:
                    pygame.draw.circle(self.screen, (255, 0, 0), (265 + 50 * i, 325 - 50 * j), 20)
                if self.places[i][j] == 2:
                    pygame.draw.circle(self.screen, (255, 255, 0), (265 + 50 * i, 325 - 50 * j), 20)

        col = -1
        pressed = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()[0]
        if time.time() - self.time > 0.5:
            for i in range(7):
                if pressed and mousePos >= 240 + 50 * i and mousePos <= 290 + 50 * i:
                    col = i
                    break

            if col != -1:
                for i in range(6):
                    if not self.places[col][i]:
                        self.time = time.time()
                        self.places[col][i] = self.turn
                        self.turn = self.turn + 1
                        if self.turn == 3:
                            self.turn = 1
                        return
            

class TTTBoard():
    def __init__(self, screen):
        self.screen = screen
        self.squares = [0 for i in range(9)]
        self.surfs = [Line(WIDTH // 2 - TTTLENGTH / 2, HEIGHT // 2, 1, TTTLENGTH * 3), Line(WIDTH // 2 + TTTLENGTH / 2, HEIGHT // 2, 1, TTTLENGTH * 3), Line(WIDTH // 2, HEIGHT // 2 - TTTLENGTH / 2, TTTLENGTH * 3, 1), Line(WIDTH // 2, HEIGHT // 2 + TTTLENGTH / 2, TTTLENGTH * 3, 1)]
        self.turn = 1
        self.time = -1

    def update(self):
        for i in range(3):
            if self.squares[i] != 0 and self.squares[i] == self.squares[i + 3] and self.squares[i] == self.squares[i + 6]:
                return self.squares[i]
            if self.squares[3 * i] != 0 and self.squares[3 * i] == self.squares[3 * i + 1] and self.squares[3 * i] == self.squares[3 * i + 2]:
                return self.squares[i * 3]
        if self.squares[4] != 0 and ((self.squares[0] == self.squares[4] and self.squares[4] == self.squares[8]) or (self.squares[2] == self.squares[4] and self.squares[4] == self.squares[6])):
            return self.squares[4]
        flag = True
        for i in range(9):
            if not self.squares[i]:
                flag = False
        if flag:
            return 3
        for i in self.surfs:
            surf = pygame.Surface((i.width, i.height))
            surf.fill((255, 255, 255))
            rect = surf.get_rect(center = (i.x, i.y))
            screen.blit(surf, rect)
        for i in range(9):
            if self.squares[i]:
                if self.squares[i] == 1:
                    pygame.draw.line(self.screen, (0, 255, 255), (WIDTH // 2 + TTTLENGTH * (i % 3 - 1) - 35, HEIGHT // 2 + TTTLENGTH * (i // 3 - 1) - 35), (WIDTH // 2 + TTTLENGTH * (i % 3 - 1) + 35, HEIGHT // 2 + TTTLENGTH * (i // 3 - 1) + 35))
                    pygame.draw.line(self.screen, (0, 255, 255), (WIDTH // 2 + TTTLENGTH * (i % 3 - 1) + 35, HEIGHT // 2 + TTTLENGTH * (i // 3 - 1) - 35), (WIDTH // 2 + TTTLENGTH * (i % 3 - 1) - 35, HEIGHT // 2 + TTTLENGTH * (i // 3 - 1) + 35))
                elif self.squares[i] == 2:
                    pygame.draw.circle(self.screen, (255, 0, 0), (WIDTH // 2 + TTTLENGTH * (i % 3 - 1), HEIGHT // 2 + TTTLENGTH * (i // 3 - 1)), 35, 1)
        if pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()
            row = -1
            column = -1
            if mousePos[0] < WIDTH // 2 - TTTLENGTH / 2 and mousePos[0] > WIDTH // 2 - 3 * TTTLENGTH / 2:
                column = 0
            if mousePos[0] < WIDTH // 2 + TTTLENGTH / 2 and mousePos[0] > WIDTH // 2 - TTTLENGTH / 2:
                column = 1
            if mousePos[0] > WIDTH // 2 + TTTLENGTH / 2 and mousePos[0] < WIDTH // 2 + 3 * TTTLENGTH / 2:
                column = 2
            if mousePos[1] < HEIGHT // 2 - TTTLENGTH / 2 and mousePos[1] > HEIGHT // 2 - 3 * TTTLENGTH / 2:
                row = 0
            if mousePos[1] < HEIGHT // 2 + TTTLENGTH / 2 and mousePos[1] > HEIGHT // 2 - TTTLENGTH / 2:
                row = 1
            if mousePos[1] > HEIGHT // 2 + TTTLENGTH / 2 and mousePos[1] < HEIGHT // 2 + 3 * TTTLENGTH / 2:
                row = 2
            if row != -1 and column != -1:
                if not self.squares[3 * row + column]:
                    self.squares[3 * row + column] = self.turn
                    if self.turn == 1:
                        self.turn = 2
                    else:
                        self.turn = 1

class Line():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Button():
    def __init__(self, x, y, width, height, name, file = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.img = None
        if file:
            self.img = pygame.image.load(file)
            self.img = pygame.transform.rotozoom(self.img, 0, 0.08)

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
        if self.img:
            imgRect = self.img.get_rect(center = (self.x, self.y - 15))
            screen.blit(self.img, imgRect)
        screen.blit(text, textRect)

class RPSButton():
    def __init__(self, screen, x, y, symbol, width = 150, height = 100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.symbol = symbol
        self.screen = screen
    def update(self):
        mousePos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and mousePos[0] >= self.x - self.width / 2 and mousePos[0] <= self.x + self.width / 2 and mousePos[1] >= self.y - self.height / 2 and mousePos[1] <= self.y + self.height / 2:
            return self.symbol
        surf = pygame.Surface((self.width, self.height))
        surf.fill((255, 255, 255))
        rect = surf.get_rect(center = (self.x, self.y))
        text = font.render(self.symbol, True, (0, 0, 0))
        textRect = text.get_rect(center = (self.x, self.y))
        self.screen.blit(surf, rect)
        self.screen.blit(text, textRect)

class SnakeBoard():
    def __init__(self, screen):
        self.screen = screen
    def update(self):
        for i in range(41):
            pygame.draw.line(self.screen, (255, 255, 255), (240 + i * 10, 25), (240 + i * 10, 415))
            
        for i in range(40):
            pygame.draw.line(self.screen, (255, 255, 255), (240, 25 + i * 10), (640, 25 + i * 10))

class Snake():
    def __init__(self, screen):
        self.screen = screen
        self.snake = [Segment(3, 20, screen)]
        self.direction = None
    def update(self, pressed_keys, apple):
        output = 0
        if pressed_keys[K_RIGHT] and self.direction != "left":
            self.direction = "right"
        if pressed_keys[K_LEFT] and self.direction != "right":
            self.direction = "left"
        if pressed_keys[K_DOWN] and self.direction != "up":
            self.direction = "down"
        if pressed_keys[K_UP] and self.direction != "down":
            self.direction = "up"
        newY = self.snake[0].y
        newX = self.snake[0].x
        if self.direction == "up":
            newY = self.snake[0].y - 1
        if self.direction == "down":
            newY = self.snake[0].y + 1
        if self.direction == "left":
            newX = self.snake[0].x - 1
        if self.direction == "right":
            newX = self.snake[0].x + 1
        
        if newX > 39 or newX < 0 or newY < 0 or newY > 38:
            output = -1
        
        for i in self.snake[1:]:
            if i.x == newX and i.y == newY:
                output =  -1

        if apple.x == newX and apple.y == newY:
            self.snake.append(Segment(-100, -100, self.screen))
            output = 1
        
        for i in self.snake:
            newX, newY = i.update(newX, newY) 
        return output

class Apple():
    def __init__(self, screen):
        self.screen = screen
        self.x = 35
        self.y = 20
    def update(self, new = None):
        if new:
            self.x = random.randint(0, 39)
            self.y = random.randint(0, 38)
        surf = pygame.Surface((9, 9))
        surf.fill((255, 95, 31))
        rect = surf.get_rect(center = (self.x * 10 + 245, self.y * 10 + 30))
        self.screen.blit(surf, rect)

class Segment():
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
    def update(self, newX, newY):
        oldX = self.x
        oldY = self.y
        self.x = newX
        self.y = newY
        surf = pygame.Surface((9, 9))
        surf.fill((255, 0, 0))
        rect = surf.get_rect(center = (self.x * 10 + 245, self.y * 10 + 30))
        self.screen.blit(surf, rect)
        return oldX, oldY

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
buttons = []
buttonNames = ["Library", "Rock Paper Scissors", "Tic Tac Toe", "Pong", "Snake", "Space Invaders", "Connect 4"]
buttonFiles = [None, "RPS.png", "TTT.png", "Pong.png", "Snake.png", "SI.png", "C4.png"] 
running = buttonNames[0]
buttons.append(Button(60, 15, 100, 20, buttonNames[0]))
pongGameOver = False
for i in range(3):
    for j in range(2):
        buttons.append(Button(175 + 225 * i, 135 + 180 * j, 150, 120, buttonNames[1 + i * 2 + j], buttonFiles[i * 2 + j + 1]))
score = 0
player = Defender(30, 400, screen)
gameOver = False
board = TTTBoard(screen)

RPSSymbols = ["Rock", "Paper", "Scissors"]
RPSButtons = [RPSButton(screen, 175 + i * (95 + 150), HEIGHT // 2, RPSSymbols[i]) for i in range(3)]

TTTGameOver = False
snakeBoard = SnakeBoard(screen)
connect4 = C4Board(screen)

p1 = PongPlayer(40, 220, screen, 1)
p2 = PongPlayer(760, 220, screen, 2)
pongBall = PongBall(screen)
connect4Over = 0

snakePlayer = Snake(screen)
apple = Apple(screen)

RPSGameOver = False
snakeGameOver = False
snakeScore = 0

while running:
    fps = 60
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
        if running == buttonNames[1]:
            if RPSGameOver:
                if pygame.key.get_pressed()[K_r]:
                    RPSGameOver = False
                    RPSButtons = [RPSButton(screen, 175 + i * (95 + 150), HEIGHT // 2, RPSSymbols[i]) for i in range(3)]
                    continue
                
                computerText = font.render(f'Computer chose {computer}', True, (0, 255, 0))
                computerTextRect = computerText.get_rect()
                computerTextRect.center = (WIDTH // 2, HEIGHT // 2 - 120)
                screen.blit(computerText, computerTextRect)
                
                playerText = font.render(f'You chose {RPSGameOver}', True, (0, 255, 0))
                playerTextRect = playerText.get_rect()
                playerTextRect.center = (WIDTH // 2, HEIGHT // 2 - 80)
                screen.blit(playerText, playerTextRect)

                if (computer == "Rock" and RPSGameOver == "Scissors") or (computer == "Paper" and RPSGameOver == "Rock") or (computer == "Scissors" and RPSGameOver == "Paper"):
                    winner = "Computer"
                elif (RPSGameOver == "Rock" and computer == "Scissors") or (RPSGameOver == "Paper" and computer == "Rock") or (RPSGameOver == "Scissors" and computer == "Paper"):
                    winner = "Player"
                else:
                    winner = None
                if winner:
                    gameOverText = font.render(f'{winner} Won', True, (0, 255, 0))
                else:
                    gameOverText = font.render(f'There was a Tie', True, (0, 255, 0))
                gameOverTextRect = gameOverText.get_rect()
                gameOverTextRect.center = (WIDTH // 2, HEIGHT // 2 - 40)
                screen.blit(gameOverText, gameOverTextRect)

                playAgainText = font.render(f'Press R to restart', True, (0, 255, 0))
                playAgainTextRect = playAgainText.get_rect()
                playAgainTextRect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(playAgainText, playAgainTextRect)

                pygame.display.flip()
                fpsClock.tick(fps)
                continue

            for i in RPSButtons:
                RPSGameOver = i.update()
                if RPSGameOver:
                    break
            computer = RPSSymbols[random.randint(0, 2)]
            text = font.render(f'Computer Choice: {computer}', True, (0, 255, 0))
            textRect = text.get_rect(midleft = (330, 300))
            screen.blit(text, textRect)
        if running == buttonNames[2]:
            if TTTGameOver:
                if pygame.key.get_pressed()[K_r]:
                    TTTGameOver = False
                    board = TTTBoard(screen)
                    continue
                if TTTGameOver == 3:
                    gameOverText = font.render(f'There was a Tie', True, (0, 255, 0))
                else:
                    gameOverText = font.render(f'Player {TTTGameOver} Won', True, (0, 255, 0))
                gameOverTextRect = gameOverText.get_rect()
                gameOverTextRect.center = (WIDTH // 2, HEIGHT // 2 - 80)
                screen.blit(gameOverText, gameOverTextRect)

                playAgainText = font.render(f'Press R to restart', True, (0, 255, 0))
                playAgainTextRect = playAgainText.get_rect()
                playAgainTextRect.center = (WIDTH // 2, HEIGHT // 2 - 40)
                screen.blit(playAgainText, playAgainTextRect)

                pygame.display.flip()
                fpsClock.tick(fps)
                continue
            TTTGameOver = board.update()
        if running == buttonNames[3]:
            if pongGameOver:
                if pygame.key.get_pressed()[K_r]:
                    pongGameOver = False
                    p1 = PongPlayer(40, 220, screen, 1)
                    p2 = PongPlayer(760, 220, screen, 2)
                    pongBall = PongBall(screen)
                    continue

                gameOverText = font.render(f'Player {pongGameOver} Won', True, (0, 255, 0))
                gameOverTextRect = gameOverText.get_rect()
                gameOverTextRect.center = (WIDTH // 2, HEIGHT // 2 - 80)
                screen.blit(gameOverText, gameOverTextRect)

                playAgainText = font.render(f'Press R to restart', True, (0, 255, 0))
                playAgainTextRect = playAgainText.get_rect()
                playAgainTextRect.center = (WIDTH // 2, HEIGHT // 2 - 40)
                screen.blit(playAgainText, playAgainTextRect)

                pygame.display.flip()
                fpsClock.tick(fps)
                continue

            x = pongBall.update(p1, p2)
            if x == 1:
                p1.lives -= 1
                pongBall = PongBall(screen)
            if x == 2:
                p2.lives -= 1
                pongBall = PongBall(screen)
            if p1.lives == 0:
                pongGameOver = 2
            if p2.lives == 0:
                pongGameOver = 1
            
            lives1Text = font.render(f'Lives: {p1.lives}', True, (255, 0, 0))
            lives1TextRect = lives1Text.get_rect()
            lives1TextRect.midleft = (130, 15)
            screen.blit(lives1Text, lives1TextRect)

            lives2Text = font.render(f'Lives: {p2.lives}', True, (255, 0, 0))
            lives2TextRect = lives2Text.get_rect()
            lives2TextRect.midright = (780, 15)
            screen.blit(lives2Text, lives2TextRect)
            
            p1.update(pygame.key.get_pressed())
            p2.update(pygame.key.get_pressed())
        if running == buttonNames[4]:
            if snakeGameOver:
                if pygame.key.get_pressed()[K_r]:
                    snakePlayer = Snake(screen)
                    apple = Apple(screen)
                    snakeGameOver = False
                    snakeScore = 0
                    continue

                gameOverText = font.render(f'Game Over', True, (255, 0, 0))
                gameOverTextRect = gameOverText.get_rect()
                gameOverTextRect.center = (WIDTH // 2, HEIGHT // 2 - 80)
                screen.blit(gameOverText, gameOverTextRect)

                playAgainText = font.render(f'Press R to restart', True, (255, 0, 0))
                playAgainTextRect = playAgainText.get_rect()
                playAgainTextRect.center = (WIDTH // 2, HEIGHT // 2 - 40)
                screen.blit(playAgainText, playAgainTextRect)

                scoreText = font.render(f'Score: {snakeScore}', True, (0, 0, 255))
                scoreTextRect = scoreText.get_rect()
                scoreTextRect.center = (WIDTH // 2, HEIGHT // 2)
                screen.blit(scoreText, scoreTextRect)
                pygame.display.flip()
                fpsClock.tick(fps)
                continue
            fps = 10
            pressed_keys = pygame.key.get_pressed()
            snakeBoard.update()
            out = snakePlayer.update(pressed_keys, apple)
            scoreText = font.render(f'Score: {snakeScore}', True, (0, 0, 255))
            scoreTextRect = scoreText.get_rect(center = (WIDTH // 2 + 40, 10))
            screen.blit(scoreText, scoreTextRect)
            if out == -1:
                snakeGameOver = True
                continue
            if out == 1:
                snakeScore += 1
                apple.update(1)
            else:
                apple.update()
        if running == buttonNames[5]:
            if gameOver:
                if pygame.key.get_pressed()[K_r]:
                    gameOver = False
                    score = 0
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
            player.update(pressed_keys)
        if running == buttonNames[6]:
            if connect4Over:
                if pygame.key.get_pressed()[K_r]:
                    connect4Over = 0
                    connect4 = C4Board(screen)
                    continue
                gameOverText = font.render(f'Player {connect4Over} Won', True, (0, 255, 0))
                gameOverTextRect = gameOverText.get_rect()
                gameOverTextRect.center = (WIDTH // 2, HEIGHT // 2 - 80)
                screen.blit(gameOverText, gameOverTextRect)

                playAgainText = font.render(f'Press R to restart', True, (0, 255, 0))
                playAgainTextRect = playAgainText.get_rect()
                playAgainTextRect.center = (WIDTH // 2, HEIGHT // 2 - 40)
                screen.blit(playAgainText, playAgainTextRect)

                pygame.display.flip()
                fpsClock.tick(fps)
                continue

            connect4Over = connect4.update()

    if pygame.key.get_pressed()[K_TAB]:
        fps *= 6
    pygame.display.flip()
    fpsClock.tick(fps)


pygame.quit()
sys.exit()