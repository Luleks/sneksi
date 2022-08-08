import pygame
from pygame import mixer
import time
from snake import SpSnake
from snake import Part
import random
import csv

pygame.init()

BLACK = (0, 0, 0)
DIMENSION = 600

FONT0 = pygame.font.SysFont('comicsans', 20)
FONT = pygame.font.Font('2Dumb.ttf', 24)
FONT1 = pygame.font.Font('2Dumb.ttf', 40)
FONT2 = pygame.font.Font('2Dumb.ttf', 26)
background = pygame.image.load('singleplayer_folder\\background_singleplayer.png')
over_sound = pygame.image.load('singleplayer_folder\\over_sound.png')
over_pause = pygame.image.load('singleplayer_folder\\over_pause.png')
over_quit = pygame.image.load('singleplayer_folder\\over_quit.png')
game_over_ = pygame.image.load('singleplayer_folder\\game_over.png')
images = [background, over_quit, over_sound, over_pause]

background_music = pygame.mixer.Sound('sounds\\background_music.wav')
background_music.set_volume(0.5)
background_music.play(-1)

slideover_music = pygame.mixer.Sound('sounds\\sliding_over_option.wav')
slideover_music.set_volume(0.5)
click_music = pygame.mixer.Sound('sounds\\click.wav')
click_music.set_volume(10.0)

def get_settings(file):
    settings_to_return = []

    with open('settings_folder\\' + file + '.txt') as f:
        set_of_settings = f.read().split(' ')
        for setting in set_of_settings:
            if setting[0] == 'c':
                for color in setting[1:].split('/'):
                    if color[0] == '!':
                        settings_to_return.append(color[1:])
            elif setting[0] == 'd':
                for option in setting[1:].split('/'):
                    if option[0] == '|':
                        try:
                            settings_to_return.append(int(option[1:-1]))
                        except ValueError:
                            settings_to_return.append(option[1:-1])

    return tuple(settings_to_return)

def get_food_color():
    with open('settings_folder\\food_settings.txt') as f:
        for color in f.read().split(' '):
            if color[0] == '!':
                return color[1:]

def get_food(snake, food, score):
    snake_head_rect = pygame.Rect(snake.head.x, snake.head.y, snake.head.GAP, snake.head.GAP)
    food_rect = pygame.Rect(food.x, food.y, food.GAP, food.GAP)
    if snake_head_rect.colliderect(food_rect):
        score += 1
        snake.add_part()

        pos = [(part.x, part.y) for part in snake.body]
        x = random.randrange(340, 900, food.GAP)
        y = random.randrange(50, 650, food.GAP)
        while (x, y) in pos:
            x = random.randrange(340, 900, food.GAP)
            y = random.randrange(50, 650, food.GAP)
        
        food.x, food.y = x, y
    return score

def check_scoreboard(score):
    with open('settings_folder\\snake_settings.txt') as f:
        name = f.read().split(' ')[0]
    local_time = time.localtime()
    date_time = time.strftime('%d/%B/%Y', local_time)
    
    with open('info_folder\\personal_bests.csv') as f:
        reader = csv.DictReader(f)
        items = list(reader)
        nums = [item['num'] for item in items]
        scores = [(item['name'], int(item['score']), item['date']) for item in items]
        scores.append((name, score, date_time))
        scores = sorted(scores, key = lambda entry:entry[1], reverse = True)[:-1]

    with open('info_folder\\personal_bests.csv', 'w', newline = '') as f:
        fieldnames = ['num','name','score','date']
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        for i in range(0, len(scores)):
            writer.writerow({'num':nums[i], 'name':scores[i][0], 'score':scores[i][1], 'date':scores[i][2]})

def draw_game_over(win, score):
    roast = FONT1.render('You died', True, BLACK)
    play_again = FONT2.render('Play again', True, BLACK)
    menu_main = FONT2.render('Main menu', True, BLACK)
    score_text = FONT1.render("Your score: " + str(score), True, BLACK)

    win.blit(game_over_, (390, 200))
    win.blit(roast, (390 + (500 - roast.get_width()) // 2, 200 + (80 - roast.get_height()) // 2))
    win.blit(score_text, (390 + (500 - score_text.get_width()) // 2, 280 + (80 - score_text.get_height()) // 2))

    y = 200 + (300 - roast.get_height()) // 2 + roast.get_height() + (80 - 60) // 2
    pygame.draw.rect(win, BLACK, (450, y, 160, 60), 2)
    pygame.draw.rect(win, BLACK, (670, y, 160, 60), 2)
    win.blit(play_again, (450 + (160 - play_again.get_width()) // 2, y + (60 - play_again.get_height()) // 2))
    win.blit(menu_main, (670 + (160 - menu_main.get_width()) // 2, y + (60 - menu_main.get_height()) // 2))

def draw(win, grid_size, grid_color, line_color, background_image, snake, food, game_end, score = 0):
    win.blit(background_image, (0, 0))

    local_time = time.localtime()
    date_time = time.strftime('%d/%B/%Y, %H:%M', local_time)
    time_to_display = FONT.render(date_time, True, BLACK)
    win.blit(time_to_display, (940 + (340 - time_to_display.get_width()) // 2, 650 - time_to_display.get_height()))

    score_to_display = FONT1.render('SCORE', True, BLACK)
    win.blit(score_to_display, (940 + (340 - score_to_display.get_width()) // 2, 340 + (224 - score_to_display.get_height()) // 2))
    score_value = FONT1.render(str(score), True, BLACK)
    win.blit(score_value, (940 + (340 - score_value.get_width()) // 2, 340 + (224 - score_to_display.get_height()) // 2 + score_to_display.get_height()))

    pause = FONT0.render('To (un)pause press Esc', True, BLACK)
    win.blit(pause, (0 + (340 - pause.get_width()) // 2, 0 + (700 - pause.get_height()) // 2))

    pygame.draw.rect(win, pygame.Color(grid_color), (340, 50, DIMENSION, DIMENSION))
    GAP = DIMENSION // grid_size
    for i in range(grid_size+1):
        pygame.draw.line(win, pygame.Color(line_color), (340 + GAP * i, 50), (340 + GAP * i, 650))
        pygame.draw.line(win, pygame.Color(line_color), (340, 50 + GAP * i), (940, 50 + GAP * i))
    
    snake.draw(win)
    food.draw(win)
    
    if game_end: draw_game_over(win, score)

    pygame.display.update()

def singleplayer(win):
    run = True
    index = 0
    score = 0
    game_end = False

    FPS = 10
    clock = pygame.time.Clock()
    speed = get_settings('gameplay_settings')[0]

    (grid_size, grid_color, line_color) = get_settings('grid_settings')
    snake_color = get_settings('snake_settings')[0]
    food_color = get_food_color()
    snake = SpSnake(1, 0, 340, 50, snake_color, DIMENSION // grid_size, grid_size, get_settings('gameplay_settings')[1:]) 
    snake.reset()
    food = Part(0, 0, 340 + 3 * DIMENSION // grid_size, 50 + 3 * DIMENSION // grid_size, food_color, DIMENSION // grid_size)

    while run:
        if speed == 'slow':
            pygame.time.delay(100)
        elif speed == 'medium':
            pygame.time.delay(50)
        clock.tick(FPS)
        index = snake.move(click_music, slideover_music)
        score = get_food(snake, food, score)

        if index == 'main_menu':
            return 'main_menu'
        elif index == 'quit':
            return 'quit'

        snake_on_right = snake.head.x > 340 + snake.head.GAP * grid_size - snake.head.GAP
        snake_on_left = snake.head.x < 340
        snake_on_up = snake.head.y < 50
        snake_on_down = snake.head.y > 50 + snake.head.GAP * grid_size - snake.head.GAP
        snake_ded = (snake_on_right or snake_on_left or snake_on_down or snake_on_up) and not snake.edge
        if (snake.head.x, snake.head.y) in [(part.x, part.y) for part in snake.body[1:]] or snake_ded:
            check_scoreboard(score)
            game_end = True
            not_clicked = True
            while not_clicked:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        y = 200 + (300 - FONT.render('You died', True, BLACK).get_height()) // 2 + FONT.render('You died', True, BLACK).get_height() + (80 - 60) // 2
                        pos = pygame.mouse.get_pos()
                        if 450 < pos[0] < 610 and y < pos[1] < y + 60:
                            snake.reset()
                            game_end = False
                            not_clicked = False
                            score = 0
                            food.x, food.y = 340 + 3 * DIMENSION // grid_size, 50 + 3 * DIMENSION // grid_size
                        elif 670 < pos[0] < 830 and y < pos[1] < y + 60:
                            return 'main_menu'
                draw(win, grid_size, grid_color, line_color, images[index], snake, food, game_end, score)

        draw(win, grid_size, grid_color, line_color, images[index], snake, food, game_end, score)