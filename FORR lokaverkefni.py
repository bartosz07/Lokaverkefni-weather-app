import pygame
from pygame.locals import *
import random

pygame.init()

width = 480
height = 480
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Lokaverkefni')

grid_size = 20
num_rows = width // grid_size
num_cols = height // grid_size

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

black = (0, 0, 0)
blue = (25, 103, 181)
dark_green = (67, 160, 71)
light_green = (129, 199, 132)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

score = 0
gameover = False

clock = pygame.time.Clock()
fps = 12

class Apple:
    def __init__(self):
        self.randomize_location()
        
    def randomize_location(self):
        random_x = random.randint(0, num_cols - 1) * grid_size
        random_y = random.randint(0, num_rows - 1) * grid_size
        self.location = (random_x, random_y)
        
    def draw(self):
        square = pygame.Rect(self.location, (grid_size, grid_size))
        pygame.draw.rect(screen, red, square)

class Snake:
    def __init__(self):
        self.body = [(width / 2, height / 2)]
        self.direction = right
        self.head = self.body[0]
        
    def turn(self, direction):
        if len(self.body) == 1:
            self.direction = direction
        else:
            if direction == left or direction == right:
                if self.body[0][1] != self.body[1][1]:
                    self.direction = direction
            if direction == up or direction == down:
                if self.body[0][0] != self.body[1][0]:
                    self.direction = direction
        
    def move(self):
        x, y = self.direction
        next_x = (self.head[0] + x * grid_size)
        next_y = (self.head[1] + y * grid_size)
        
        if next_x < 0 or next_x >= width or next_y < 0 or next_y >= height:
            return True 
        
        next_x = next_x % width
        next_y = next_y % height
        next_location = (next_x, next_y)
        
        self.body.insert(0, next_location)
        self.head = self.body[0]
        
        if self.head == apple.location:
            apple.randomize_location()
            while apple.location in self.body:
                apple.randomize_location()
        else:
            self.body.pop()
        
    def check_collision(self):
        if self.head in self.body[1:]:
            return True
        return False
        
    def draw(self):
        for body_part in self.body:
            square = pygame.Rect(body_part, (grid_size, grid_size))
            pygame.draw.rect(screen, blue, square)
            pygame.draw.rect(screen, yellow, square, 2)

def draw_background():
    for x in range(num_cols):
        for y in range(num_rows):
            square = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, dark_green, square)
            else:
                pygame.draw.rect(screen, light_green, square)

apple = Apple()
snake = Snake()

font = pygame.font.SysFont('monoface', 16)

running = True
while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                snake.turn(up)
            elif event.key == K_DOWN:
                snake.turn(down)
            elif event.key == K_LEFT:
                snake.turn(left)
            elif event.key == K_RIGHT:
                snake.turn(right)
    
    draw_background()
    
    apple.draw()
    if snake.move():
        gameover = True
    
    snake.draw()
    
    text = font.render(f"Score: {len(snake.body) - 1}", 1, white)
    screen.blit(text, (10, 10))
    
    collision = snake.check_collision()
    if collision:
        gameover = True
        
    while gameover:
        clock.tick(fps)
        
        pygame.draw.rect(screen, black, (0, height / 2 - 50, width, 100))
        text = font.render("Game over! Ýttu á SPACE til að spila aftur", 1, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, height / 2)
        screen.blit(text, text_rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                gameover = False
                score = 0
                snake.body = [(width / 2, height / 2)]
                snake.direction = right
                snake.head = snake.body[0]
                apple.randomize_location()
            
    pygame.display.update()

pygame.quit()
