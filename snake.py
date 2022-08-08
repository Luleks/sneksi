import pygame
from pygame import mixer
import time
import random

pygame.init()
pygame.mixer.init()

class Part:
    def __init__(self, dirx, diry, x, y, color, GAP):
        self.dirx = dirx
        self.diry = diry
        self.x = x
        self.y = y
        self.color = color
        self.GAP = GAP
        self.len = self.GAP - 5
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x + 3, self.y + 3, self.len, self.len))
    
    def move(self):
        self.x = self.x + self.GAP * self.dirx
        self.y = self.y + self.GAP * self.diry

class Snake:
    body = []
    turns = {}
    
    def __init__(self, dirx, diry, x, y, color, GAP, grid_size):
        self.dirx = dirx
        self.diry = diry
        self.x = x + GAP * grid_size // 2
        self.y = y + GAP * grid_size // 2
        self.color = color
        self.GAP = GAP
        self.grid_size = grid_size
        self.head = Part(self.dirx, self.diry, self.x, self.y, self.color, self.GAP)
        self.body.append(self.head)
    
    def draw(self, win):
        for part in self.body:
            part.draw(win)
    
    def reset(self):
        self.body = []
        self.turns = {}
        self.head = Part(self.dirx, self.diry, self.x, self.y, self.color, self.GAP)
        self.body.append(self.head)
    
    def add_part(self):
        if self.body[-1].dirx == 1: 
            self.body.append(Part(self.body[-1].dirx, self.body[-1].diry, self.body[-1].x - self.GAP, self.body[-1].y, self.color, self.GAP))
        elif self.body[-1].dirx == -1:
            self.body.append(Part(self.body[-1].dirx, self.body[-1].diry, self.body[-1].x + self.GAP, self.body[-1].y, self.color, self.GAP))
        elif self.body[-1].diry == 1:
            self.body.append(Part(self.body[-1].dirx, self.body[-1].diry, self.body[-1].x, self.body[-1].y - self.GAP, self.color, self.GAP))
        elif self.body[-1].diry == -1:
            self.body.append(Part(self.body[-1].dirx, self.body[-1].diry, self.body[-1].x, self.body[-1].y + self.GAP, self.color, self.GAP))

class SpSnake(Snake):
    pre_pause = []
    def __init__(self, dirx, diry, x, y, color, GAP, grid_size, settings):
        super().__init__(dirx, diry, x, y, color, GAP, grid_size)
        (self.edge, self.controls) = SpSnake.unpack_settings(settings)
        self.pause = False
    
    def move(self, click_music, slide_music):
        with open('sounds\\sound.txt', 'r') as f:
            sound = int(f.read())
        with open('singleplayer_folder\slide.txt', 'r') as f:
            slide = int(f.read())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 1180 < pos[0] < 1260 and 20 < pos[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'main_menu'
                elif 1180 < pos[0] < 1260 and 140 < pos[1] < 220:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    sound = not sound
                    with open('sounds\\sound.txt', 'w') as f:
                        f.write(str(int(sound)))
                elif 1180 < pos[0] < 1260 and 260 < pos[1] < 340:
                    self.pause = not self.pause
           
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[self.controls[0]] and self.head.diry != 1 and not self.pause:
                    self.head.dirx, self.head.diry = 0, -1
                    self.turns[self.head.x, self.head.y] = (0, -1)
                elif keys[self.controls[1]] and self.head.diry != -1 and not self.pause:
                    self.head.dirx, self.head.diry = 0, 1
                    self.turns[self.head.x, self.head.y] = (0, 1)
                elif keys[self.controls[2]] and self.head.dirx != 1 and not self.pause:
                    self.head.dirx, self.head.diry = -1, 0
                    self.turns[self.head.x, self.head.y] = (-1, 0)
                elif keys[self.controls[3]] and self.head.dirx != -1 and not self.pause:
                    self.head.dirx, self.head.diry = 1, 0
                    self.turns[self.head.x, self.head.y] = (1, 0)
                elif keys[pygame.K_ESCAPE]:
                    self.pause = not self.pause

        for i, part in enumerate(self.body):
            if (part.x, part.y) in self.turns:
                (part.dirx, part.diry) =  self.turns[part.x, part.y]
                if i == len(self.body) - 1:
                    self.turns.pop((part.x, part.y))
            if not self.pause:
                part.move()

            if part.x > 340 + self.GAP * self.grid_size - part.GAP and self.edge: part.x = 340
            elif part.x < 340 and self.edge: part.x = 340 + self.GAP * self.grid_size - part.GAP
            elif part.y > 50 + self.GAP * self.grid_size - part.GAP and self.edge: part.y = 50
            elif part.y < 50 and self.edge: part.y = 50 + self.GAP * self.grid_size - part.GAP

        if not sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
        
        pos = pygame.mouse.get_pos()
        if 1180 < pos[0] < 1260 and 20 < pos[1] < 100:
            if sound and slide: slide_music.play()
            slide = 0
            with open('singleplayer_folder\slide.txt', 'w') as f:
                f.write(str(int(slide)))
            return 1
        elif 1180 < pos[0] < 1260 and 140 < pos[1] < 220:
            if sound and slide: slide_music.play()
            slide = 0
            with open('singleplayer_folder\slide.txt', 'w') as f:
                f.write(str(int(slide)))
            return 2
        elif 1180 < pos[0] < 1260 and 260 < pos[1] < 340:
            if sound and slide: slide_music.play()
            slide = 0
            with open('singleplayer_folder\slide.txt', 'w') as f:
                f.write(str(int(slide)))
            return 3
        else:
            slide = 1
            with open('singleplayer_folder\slide.txt', 'w') as f:
                f.write(str(int(slide)))
            return 0

    @staticmethod
    def unpack_settings(settings):
        (edge, controls) = settings
        if edge == 'pass': edge = True
        elif edge == 'die': edge = False

        if controls == 'WASD': controls = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
        elif controls == 'arrows': controls = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        elif controls == 'IJKL': controls = [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l]

        return (edge, controls)

class MpSnake(Snake):
    def __init__(self, dirx, diry, x, y, color, GAP, grid_size, start_x, start_y):
        self.body = []
        self.turns = {}
        self.dirx = dirx
        self.diry = diry
        self.x = x + GAP * grid_size // 2
        self.y = y + GAP * grid_size // 2
        self.color = color
        self.GAP = GAP
        self.grid_size = grid_size
        self.head = Part(self.dirx, self.diry, self.x, self.y, self.color, self.GAP)
        self.body.append(self.head)
        self.start_x, self.start_y = start_x, start_y
        self.game_over = False
    
    def change_dir(self, direction):
        if direction == 'up' and self.head.diry != 1:
            self.head.dirx, self.head.diry = 0, -1
            self.turns[(self.head.x, self.head.y)] = (0, -1)
        elif direction == 'down' and self.head.diry != -1:
            self.head.dirx, self.head.diry = 0, 1
            self.turns[(self.head.x, self.head.y)] = (0, 1)
        elif direction == 'left' and self.head.dirx != 1:
            self.head.dirx, self.head.diry = -1, 0
            self.turns[(self.head.x, self.head.y)] = (-1, 0)
        elif direction == 'right' and self.head.dirx != -1:
            self.head.dirx, self.head.diry = 1, 0
            self.turns[(self.head.x, self.head.y)] = (1, 0)
    
    def move(self):
        for i, part in enumerate(self.body):
            if (part.x, part.y) in self.turns:
                (part.dirx, part.diry) =  self.turns[part.x, part.y]
                if i == len(self.body) - 1:
                    self.turns.pop((part.x, part.y))
            if not self.game_over:
                part.move()

            if part.x > self.start_x + self.GAP * self.grid_size - part.GAP: part.x = self.start_x
            elif part.x < self.start_x: part.x = self.start_x + self.GAP * self.grid_size - part.GAP
            elif part.y > 50 + self.GAP * self.grid_size - part.GAP: part.y = 50
            elif part.y < 50: part.y = 50 + self.GAP * self.grid_size - part.GAP

class OnlineSnake(MpSnake):
    def __init__(self, dirx, diry, x, y, color, GAP, grid_size, start_x, start_y, score):
        self.body = []
        self.turns = {}
        self.dirx = dirx
        self.diry = diry
        self.x = x + GAP * grid_size // 2
        self.y = y + GAP * grid_size // 2
        self.color = color
        self.GAP = GAP
        self.grid_size = grid_size
        self.head = Part(self.dirx, self.diry, self.x, self.y, self.color, self.GAP)
        self.body.append(self.head)
        self.start_x, self.start_y = start_x, start_y
        self.game_over = False
        self.score = score
        self.food = Part(0, 0, 20 + 3 * GAP, 50 + 3 * GAP, (160, 32, 240), GAP)
        self.name = OnlineSnake.get_name('settings_folder\\snake_settings.txt')
        self.play_again = False
        self.main_menu = False
        self.reseted = False

    def translate_position(self):
        for part in self.body:
            part.x += 640
            self.start_x += 640
            self.x += 640
    
    def get_food(self):
        head_rect = pygame.Rect(self.head.x, self.head.y, self.head.GAP, self.head.GAP)
        food_rect = pygame.Rect(self.food.x, self.food.y, self.food.GAP, self.food.GAP)
        if head_rect.colliderect(food_rect):
            self.score += 1
            self.add_part()

            pos = [(part.x, part.y) for part in self.body]
            x = random.randrange(self.start_x, self.start_x + self.GAP * self.grid_size, self.GAP)
            y = random.randrange(self.start_y, self.start_y + self.GAP * self.grid_size, self.food.GAP)
            while (x, y) in pos:
                x = random.randrange(self.start_x, self.start_x + self.GAP * self.grid_size, self.food.GAP)
                y = random.randrange(self.start_y, self.start_y + self.GAP * self.grid_size, self.food.GAP)
            
            self.food.x, self.food.y = x, y
    
    def is_game_over(self):
        if (self.head.x, self.head.y) in [(part.x, part.y) for part in self.body[1:]]:
            self.game_over = True
    
    def translate_position(self):
        for part in self.body:
            part.x += 640
        self.food.x += 640

    def reset_food(self):
        self.food = Part(0, 0, 20 + 3 * self.GAP, 50 + 3 * self.GAP, (160, 32, 240), self.GAP)
    
    @staticmethod
    def get_name(file):
        with open(file) as f:
            name = (f.read().split(' '))[0]
        return name