import pygame
from network import Network

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

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw(win, snake1, snake2, food1, food2, score1, score2, game_start):
    win.blit(background, (0, 0))

    player_1 = FONT.render(snake1.name + '  score: ' + str(score1), True, BLACK)
    player_2 = FONT.render(snake2.name + '  score: ' + str(score2), True, BLACK)

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

    if not game_start:
        textx = FONT1.render('Waiting for opponent', True, WHITE)
        draw_rect_alpha(win, (0, 0, 0, 200), (20, 50, 600, 600))
        win.blit(textx, (20 + (600 - textx.get_width()) // 2, 50 + (600 - textx.get_height()) // 2))

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
        if snake1.play_again:
            draw_rect_alpha(win, (0, 0, 0, 200), (0 + (1280 - game_over_.get_width()) // 2, 0 + (700 - game_over_.get_height()) // 2, 200, 60))
        win.blit(play_again, (0 + (1280 - game_over_.get_width()) // 2 + (200 - play_again.get_width()) // 2, 0 + (700 - game_over_.get_height()) // 2 + (60 - play_again.get_height()) // 2))
        win.blit(main_menu, (0 + (1280 - game_over_.get_width()) // 2 + (200 - main_menu.get_width()) // 2, 60 + (700 - game_over_.get_height()) // 2 + (60 - main_menu.get_height()) // 2))
        print()

    pygame.display.update()

def online(win):
    run = True
    n = Network()
    snake1 = n.get_info()

    clock = pygame.time.Clock()
    FPS = 10
    with open('sounds\\sound.txt', 'r') as f:
        print(f.seek(0), f.read(), len(f.read()))
        f.seek(0)
        sound = int(f.read())

    with open('online_folder\\game_start.txt', 'r') as f:
        print(f.seek(0), f.read(), len(f.read()))
        f.seek(0)
        game_start = int(f.read())

    while run:
        clock.tick(FPS)
        snake2 = n.send(snake1)
        snake2.translate_position()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake1.main_menu = True
                n.send(snake1)
                return 'quit'

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 620 < pos[0] <  660 and 0 < pos[1] < 40:
                    #snake1.main_menu = True
                    #n.send(snake1)
                    return 'main_menu'

                if snake1.game_over and snake2.game_over:
                    if 540 < pos[0] < 740 and 290 < pos[1] < 350:
                        snake1.play_again = True
                    elif 540 < pos[0] < 740 and 350 < pos[1] < 410:
                        snake1.main_menu = True
                        n.send(snake1)
                        return 'main_menu'

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]: snake1.change_dir('up')
                elif keys[pygame.K_DOWN]: snake1.change_dir('down')
                elif keys[pygame.K_LEFT]: snake1.change_dir('left')
                elif keys[pygame.K_RIGHT]: snake1.change_dir('right')

        if snake1.play_again and snake2.play_again:
            snake1.reset()
            snake1.score = 0
            snake1.reset_food()
            snake1.game_over = False
            snake1.reseted = True
            if snake1.reseted and snake2.reseted:
                snake1.play_again = False

        if not snake1.game_over and not snake2.game_over:
            snake1.reseted = False

        if snake2.main_menu:
            game_start = 0
            with open('online_folder\\game_start.txt', 'w') as f:
                f.write(str(0))
            snake1.reset()
            snake1.score = 0
            snake1.reset_food()
            snake1.game_over = False

        pygame.time.delay(50)
        if game_start:
            snake1.move()
            snake1.get_food()
            snake1.is_game_over()
        else:
            with open('online_folder\\game_start.txt', 'r') as f:
                game_start = int(f.read())

        if not sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        draw(win, snake1, snake2, snake1.food, snake2.food, snake1.score, snake2.score, game_start)
        snake2 = n.send(snake1)