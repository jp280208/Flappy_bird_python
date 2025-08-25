import pygame
from sys import exit
import random
import os


GAME_WIDTH = 360
GAME_HEIGHT = 640

bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34 
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img


pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

def load_image_or_color(image_path, default_color, size):
    if os.path.exists(image_path):
        img = pygame.image.load(image_path)
        print(f"Imagem encontrada: {image_path}") 
        return pygame.transform.scale(img, size)
    else:
        print(f"Arquivo não encontrado: {image_path}. Usando cor de fallback.") 
        surface = pygame.Surface(size)
        surface.fill(default_color)
        return surface


background_image = load_image_or_color("assets/flappybirdbg.png", (100, 150, 255), (GAME_WIDTH, GAME_HEIGHT))
bird_image = load_image_or_color("assets/flappybird.png", (255, 255, 0), (bird_width, bird_height))
top_pipe_image = load_image_or_color("assets/toppipe.png", (0, 128, 0), (pipe_width, pipe_height))
bottom_pipe_image = load_image_or_color("assets/bottompipe.png", (0, 128, 0), (pipe_width, pipe_height))


bird = Bird(bird_image)
pipes = []
velocity_x = -2 
velocity_y = 0 
gravity = 0.4
score = 0
game_over = False

def draw():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)
    
    text_str = str(int(score))
    if game_over:
        text_str = "Game Over: " + text_str

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))

def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0) 

    if bird.y > GAME_HEIGHT:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5 
            pipe.passed = True
        
        if bird.colliderect(pipe):
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0) 

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2) 
    opening_space = GAME_HEIGHT/4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)

pygame.init() 
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500) 

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == create_pipes_timer and not game_over:
            create_pipes()
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                velocity_y = -6

            
                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False
    
    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60) 
