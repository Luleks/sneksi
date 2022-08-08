import pygame
from snake import MpSnake
from snake import Part
import random
import csv
import time

pygame.init()

RED = (255, 0, 0)
DARKGREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (160, 32, 240)
DIMENSION = 600
GRID_SIZE = 20
GAP = DIMENSION // GRID_SIZE

FONT = pygame.font.Font('2Dumb.ttf', 30)
FONT1 = pygame.font.Font('2Dumb.ttf', 40)
FONT2 = pygame.font.Font('2Dumb.ttf', 26)
background = pygame.image.load('offline_folder\\background_offline.png')
game_over = pygame.image.load('offline_folder\\game_over.png')
game_over_ = pygame.image.load('offline_folder\\game_over_.png')

background_music = pygame.mixer.Sound('sounds\\background_music.wav')
background_music.set_volume(0.5)
background_music.play(-1)

def get_food(snake, food, score):
    snake_head_rect = pygame.Rect(snake.head.x, snake.head.y, snake.head.GAP, snake.head.GAP)
    food_rect = pygame.Rect(food.x, food.y, food.GAP, food.GAP)
    if snake_head_rect.colliderect(food_rect):
        score += 1
        snake.add_part()

        pos = [(part.x, part.y) for part in snake.body]
        x = random.randrange(snake.start_x, snake.start_x + DIMENSION, food.GAP)
        y = random.randrange(snake.start_y, snake.start_y + DIMENSION, food.GAP)
        while (x, y) in pos:
            x = random.randrange(snake.start_x, snake.start_x + DIMENSION, food.GAP)
            y = random.randrange(snake.start_y, snake.start_y + DIMENSION, food.GAP)
        
        food.x, food.y = x, y
    return score

def write_scoreboard(score1, score2):
    local_time = time.localtime()
    date_time = time.strftime('%d/%B/%Y', local_time)
    with open('info_folder\\result_history.csv') as f:
        reader = csv.DictReader(f)
        items = list(reader)
        read = [(item['home'], item['score'], item['away'], item['date']) for item in items]
    toWrite = ([('snake1', str(score1)+'-'+str(score2), 'snake2', date_time)] + read)[:-1]

    with open('info_folder\\result_history.csv', 'w', newline = '') as f:
        fieldnames = ['home','score','away','date']
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        for i in range(0, len(toWrite)):
            writer.writerow({'home':toWrite[i][0], 'score':toWrite[i][1], 'away':toWrite[i][2], 'date':toWrite[i][3]})


def draw(win, snake1, snake2, food1, food2, score1 = 0, score2 = 0):
    win.blit(background, (0, 0))

    player_1 = FONT.render('WASD  score:  ' + str(score1), True, BLACK)
    player_2 = FONT.render('arrows   score:  ' + str(score2), True, BLACK)

    win.blit(player_1, (20 + (600 - player_1.get_width()) // 2, 0 + (50 - player_1.get_height()) // 2))
    win.blit(player_2, (660 + (600 - player_2.get_width()) // 2, 0 + (50 - player_2.get_height()) // 2))

    pygame.draw.rect(win, DARKGREEN, (20, 50, 600, 600))
    pygame.draw.rect(win, DARKGREEN, (660, 50, 600, 600))

    for i in range(GRID_SIZE + 1):
        pygame.draw.line(win, RED, (20 + GAP * i, 50), (20 + GAP * i, 650))
        pygame.draw.line(win, RED, (20, 50 + GAP * i), (620, 50 + GAP * i))
        pygame.draw.line(win, RED, (660 + GAP * i, 50), (660 + GAP * i, 650))
        pygame.draw.line(win, RED, (660, 50 + GAP * i), (1260, 50 + GAP * i))

    food1.draw(win)
    food2.draw(win)
    snake1.draw(win)
    snake2.draw(win)

    if snake1.game_over:
        roast = FONT1.render('You died', True, BLACK)
        score_text = FONT1.render("Your score: " + str(score1), True, BLACK)

        x = 20 + (600 - game_over.get_width()) // 2
        y = 50 + (600 - game_over.get_height()) // 2
        win.blit(game_over, (x, y))
        win.blit(roast, (x + (500 - roast.get_width()) // 2, y + (150 - roast.get_height()) // 2))
        win.blit(score_text, (x + (500 - score_text.get_width()) // 2, y + 150 + (150 - score_text.get_height()) // 2))

        if snake2.game_over and score1 > score2:
            outcome = FONT1.render('Winner!', True, BLACK)
            y1 = y + 150 + (150 - score_text.get_height()) // 2
            h_diff = y1 - (y + (150 - roast.get_height()) // 2 +  roast.get_height())
            win.blit(outcome, (x + (500 - outcome.get_width()) // 2, y1 - h_diff + (h_diff - outcome.get_height()) // 2))
        elif snake2.game_over and score1 == score2:
            outcome = FONT1.render('Draw!', True, BLACK)
            y1 = y + 150 + (150 - score_text.get_height()) // 2
            h_diff = y1 - (y + (150 - roast.get_height()) // 2 +  roast.get_height())
            win.blit(outcome, (x + (500 - outcome.get_width()) // 2, y1 - h_diff + (h_diff - outcome.get_height()) // 2))
        elif snake2.game_over and score1 < score2:
            outcome = FONT1.render('Loser!', True, BLACK)
            y1 = y + 150 + (150 - score_text.get_height()) // 2
            h_diff = y1 - (y + (150 - roast.get_height()) // 2 +  roast.get_height())
            win.blit(outcome, (x + (500 - outcome.get_width()) // 2, y1 - h_diff + (h_diff - outcome.get_height()) // 2))
    
    if snake2.game_over:
        roast = FONT1.render('You died', True, BLACK)
        score_text = FONT1.render("Your score: " + str(score2), True, BLACK)

        x = 660 + (600 - game_over.get_width()) // 2
        y = 50 + (600 - game_over.get_height()) // 2
        win.blit(game_over, (x, y))
        win.blit(roast, (x + (500 - roast.get_width()) // 2, y + (150 - roast.get_height()) // 2))
        win.blit(score_text, (x + (500 - score_text.get_width()) // 2, y + 150 + (150 - score_text.get_height()) // 2))

        if snake1.game_over and score2 > score1:
            outcome = FONT1.render('Winner!', True, BLACK)
            y1 = y + 150 + (150 - score_text.get_height()) // 2
            h_diff = y1 - (y + (150 - roast.get_height()) // 2 +  roast.get_height())
            win.blit(outcome, (x + (500 - outcome.get_width()) // 2, y1 - h_diff + (h_diff - outcome.get_height()) // 2))
        elif snake1.game_over and score2 == score1:
            outcome = FONT1.render('Draw!', True, BLACK)
            y1 = y + 150 + (150 - score_text.get_height()) // 2
            h_diff = y1 - (y + (150 - roast.get_height()) // 2 +  roast.get_height())
            win.blit(outcome, (x + (500 - outcome.get_width()) // 2, y1 - h_diff + (h_diff - outcome.get_height()) // 2))
        elif snake1.game_over and score2 < score1:
            outcome = FONT1.render('Loser!', True, BLACK)
            y1 = y + 150 + (150 - score_text.get_height()) // 2
            h_diff = y1 - (y + (150 - roast.get_height()) // 2 +  roast.get_height())
            win.blit(outcome, (x + (500 - outcome.get_width()) // 2, y1 - h_diff + (h_diff - outcome.get_height()) // 2))

    if snake1.game_over and snake2.game_over:
        play_again = FONT2.render('Play again', True, BLACK)
        main_menu = FONT2.render('Main menu', True, BLACK)
        win.blit(game_over_, (0 + (1280 - game_over_.get_width()) // 2, 0 + (700 - game_over_.get_height()) // 2))
        pygame.draw.rect(win, BLACK, (0 + (1280 - game_over_.get_width()) // 2, 0 + (700 - game_over_.get_height()) // 2, 200, 120), 2)
        pygame.draw.line(win, BLACK, ((1280 - game_over_.get_width()) // 2, 350), ((1280 - game_over_.get_width()) // 2 + 200, 350), 2)
        win.blit(play_again, (0 + (1280 - game_over_.get_width()) // 2 + (200 - play_again.get_width()) // 2, 0 + (700 - game_over_.get_height()) // 2 + (60 - play_again.get_height()) // 2))
        win.blit(main_menu, (0 + (1280 - game_over_.get_width()) // 2 + (200 - main_menu.get_width()) // 2, 60 + (700 - game_over_.get_height()) // 2 + (60 - main_menu.get_height()) // 2))
        print()

    pygame.display.update()

def offline(win):
    run = True
    snake1 = MpSnake(1, 0, 20, 50, WHITE, GAP, GRID_SIZE, 20, 50)
    snake2 = MpSnake(1, 0, 660, 50, WHITE, GAP, GRID_SIZE, 660, 50)
    food1 = Part(0, 0, 20 + 3 * GAP, 50 + 3 * GAP, PURPLE, GAP)
    food2 = Part(0, 0, 660 + 3 * GAP, 50 + 3 * GAP, PURPLE, GAP)
    score1, score2 = 0, 0

    clock = pygame.time.Clock()
    FPS = 10
    with open('sounds\\sound.txt', 'r') as f:
        sound = int(f.read())

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 620 < pos[0] <  660 and 0 < pos[1] < 40:
                    return 'main_menu'
                if snake1.game_over and snake2.game_over:
                    write_scoreboard(score1, score2)
                    if 540 < pos[0] < 740 and 290 < pos[1] < 350:
                        snake1.reset()
                        snake2.reset()
                        snake1.game_over, snake2.game_over = False, False
                        score1, score2 = 0, 0
                    elif 540 < pos[0] < 740 and 350 < pos[1] < 410:
                        return 'main_menu'
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]: snake1.change_dir('up')
                elif keys[pygame.K_s]: snake1.change_dir('down')
                elif keys[pygame.K_a]: snake1.change_dir('left')
                elif keys[pygame.K_d]: snake1.change_dir('right')
                if keys[pygame.K_UP]: snake2.change_dir('up')
                elif keys[pygame.K_DOWN]: snake2.change_dir('down')
                elif keys[pygame.K_LEFT]: snake2.change_dir('left')
                elif keys[pygame.K_RIGHT]: snake2.change_dir('right')

        pygame.time.delay(50)
        snake1.move()
        snake2.move()
        score1 = get_food(snake1, food1, score1)
        score2 = get_food(snake2, food2, score2)

        if (snake1.head.x, snake1.head.y) in [(part.x, part.y) for part in snake1.body[1:]]:
            snake1.game_over = True
        if (snake2.head.x, snake2.head.y) in [(part.x, part.y) for part in snake2.body[1:]]:
            snake2.game_over = True

        if not sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        draw(win, snake1, snake2, food1, food2, score1, score2)