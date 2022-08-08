from multiprocessing.sharedctypes import Value
import pygame
from pygame import mixer
import time

pygame.font.init()
pygame.mixer.init()

BLACK = (0, 0, 0)

TITLE_FONT = pygame.font.Font('2Dumb.ttf', 30)
FONT = pygame.font.SysFont('comicsans', 20)
NOTE_FONT = pygame.font.SysFont('comicsans', 10)
background = pygame.image.load('settings_folder\\background_settings.png')
over_back = pygame.image.load('settings_folder\\over_back.png')
over_sound = pygame.image.load('settings_folder\\over_sound.png')
over_quit = pygame.image.load('settings_folder\\over_quit.png')

background_music = pygame.mixer.Sound('sounds\\background_music.wav')
background_music.set_volume(0.5)
background_music.play(-1)

slideover_music = pygame.mixer.Sound('sounds\\sliding_over_option.wav')
slideover_music.set_volume(0.5)
click_music = pygame.mixer.Sound('sounds\\click.wav')
click_music.set_volume(10.0)

def change_settings(settings_pos, mouse_pos):
    for key, value in settings_pos.items():
        if isinstance(value, tuple):
            if pygame.Rect(value).collidepoint(mouse_pos[0], mouse_pos[1]):
                enter_pressed = False
                capital = False
                new_namestr = ''
                while not enter_pressed:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN: enter_pressed = True  
                            else: 
                                try:
                                    if capital:
                                        new_namestr += chr(event.key).upper()
                                        capital = False
                                    else:
                                        new_namestr += chr(event.key)
                                except ValueError:
                                    capital = True
                if new_namestr != '':
                    new_settings = ''
                    with open('settings_folder\\snake_settings.txt') as f:
                        set_of_settings = f.read().split(' ')
                        set_of_settings[key[1]] = new_namestr
                        new_settings = ' '.join(set_of_settings)
                    with open('settings_folder\\snake_settings.txt', 'w') as f:
                            f.write(new_settings)

        else:
            for item in value:
                if pygame.Rect(item).collidepoint(mouse_pos[0], mouse_pos[1]):
                    if key == 'food':
                        new_settings = ''
                        with open('settings_folder\\food_settings.txt') as f:
                            set_of_settings = f.read().split(' ')
                            for i in range(len(set_of_settings)):
                                if set_of_settings[i][0] == '!' and i != value.index(item): set_of_settings[i] = set_of_settings[i][1:]
                                elif set_of_settings[i][0] != '!' and i == value.index(item): set_of_settings[i] = '!' + set_of_settings[i]
                            new_settings = ' '.join(set_of_settings)
                        with open('settings_folder\\food_settings.txt', 'w') as f:
                            f.write(new_settings)
                    else:
                        new_settings = ''
                        with open('settings_folder\\' + key[0] + '.txt') as f:
                            set_of_settings = f.read().split(' ')
                            setting_to_handle = set_of_settings[key[1]]
                            first_letter = setting_to_handle[0]
                            if first_letter == 'c':
                                options = setting_to_handle[1:].split('/')
                                for i in range(len(options)):
                                    if options[i][0] == '!' and value.index(item) != i: options[i] = options[i][1:]
                                    elif options[i][0] != '!' and value.index(item) == i: options[i] = '!' + options[i]
                            elif first_letter == 'd':
                                options = setting_to_handle[1:].split('/')
                                for i in range(len(options)):
                                    if options[i][0] == '|' and value.index(item) != i: options[i] = options[i][1:-1]
                                    elif options[i][0] != '|' and value.index(item) == i: options[i] = '|' + options[i] + '|'
                            setting_to_handle = first_letter + "/".join(options)
                            set_of_settings[key[1]] = setting_to_handle
                            new_settings = " ".join(set_of_settings)
                        with open('settings_folder\\' + key[0] + '.txt', 'w') as f:
                            f.write(new_settings)
                    break

def handle_settings(win, settings_pos, x_settings_name, x_settings, x, y):
    with open('settings_folder\\' + x_settings_name + '.txt') as f:
        if x_settings_name == 'food_settings':
            settings_pos['food'] = []
            colors = f.read().split(' ')
            x = 255
            for i in range(len(colors)):
                if i % 3 == 0 and i > 0:
                    y += 50
                if colors[i][0] == '!':
                    pygame.draw.rect(win, colors[i][1:], (x + 50 * (i % 3), y, 30, 30))
                    pygame.draw.rect(win, BLACK, (x + 50 * (i % 3) - 2, y - 2, 30 + 4, 30 + 4), 2)
                else:
                    pygame.draw.rect(win, colors[i], (x + 50 * (i % 3), y, 30, 30))
                settings_pos['food'].append((x + 50 * (i % 3), y, 30, 30))
        else:
            set_of_settings = f.read().split(' ')
            i = 0
            for setting in set_of_settings:
                if setting[0] == 'c':
                    settings_pos[(x_settings_name, i)] = []
                    rects = [color for color in setting[1:].split('/')]
                    text = FONT.render(x_settings[i], True, BLACK)
                    x1 = x + (640 - text.get_width() - len(rects) * 50) // 2
                    y1 = y + 60 * i + (60 - text.get_height()) // 2
                    win.blit(text, (x1, y1))
                    j = 0
                    for rect in rects:
                        if rect[0] != '!':
                            pygame.draw.rect(win, pygame.Color(rect), (x1 + text.get_width() + 20 + 50 * j, y1, 30, 30))
                        else:
                            pygame.draw.rect(win, pygame.Color(rect[1:]), (x1 + text.get_width() + 20 + 50 * j, y1, 30, 30))
                            pygame.draw.rect(win, BLACK, (x1 + text.get_width() + 20 + 50 * j - 2, y1 - 2, 30 + 4, 30 + 4), 2)
                        settings_pos[(x_settings_name, i)].append((x1 + text.get_width() + 20 + 50 * j, y1, 30, 30))
                        j += 1

                elif setting[0] == 'd':
                    settings_pos[(x_settings_name, i)] = []
                    tab_sum = FONT.render('    ', True, BLACK).get_width()
                    rects = [FONT.render(value, True, BLACK) for value in setting[1:].split('/')]
                    text = FONT.render(x_settings[i], True, BLACK)
                    total_len = sum([option.get_width() for option in rects]) + len(rects) * tab_sum
                    x1 = x + (640 - text.get_width() - total_len) // 2
                    y1 = y + 60 * i + (60 - text.get_height()) // 2
                    win.blit(text, (x1, y1))
                    prev_sum, j = 0, 1
                    for rect in rects:
                        win.blit(rect, (x1 + text.get_width() + tab_sum * j + prev_sum, y1))
                        settings_pos[(x_settings_name, i)].append((x1 + text.get_width() + tab_sum * j + prev_sum, y1, rect.get_width(), rect.get_height()))
                        prev_sum, j = prev_sum + rect.get_width(), j + 1

                else:
                    text = FONT.render(x_settings[i] + '    ' + setting, True, BLACK)
                    x1 = x + (640 - text.get_width()) // 2
                    y1 = y + 60 * i + (60 - text.get_height()) // 2
                    win.blit(text, (x1, y1))
                    settings_pos[(x_settings_name, i)] = (x1, y1, text.get_width(), text.get_height())
                i += 1

def draw(win, background_image, settings_pos):
    win.blit(background_image, (0, 0))

    snake_title = TITLE_FONT.render('Snake', True, BLACK)
    food_title = TITLE_FONT.render('Food', True, BLACK)
    gameplay_title = TITLE_FONT.render('Gameplay', True, BLACK)
    grid_title = TITLE_FONT.render('Grid', True, BLACK)
    note = NOTE_FONT.render('To change name or species click on option or current name. After you finish entering hit enter!!', True, BLACK)
    win.blit(snake_title, (0 + (640 - snake_title.get_width()) // 2, 120 + (110 - snake_title.get_height()) // 2))
    win.blit(food_title, (0 + (640 - food_title.get_width()) // 2, 410 + (110 - food_title.get_height()) // 2))
    win.blit(gameplay_title, (640 + (640 - gameplay_title.get_width()) // 2, 120 + (110 - gameplay_title.get_height()) // 2))
    win.blit(grid_title, (640 + (640 - grid_title.get_width()) // 2, 410 + (110 - grid_title.get_height()) // 2))
    win.blit(note, (0 + (640 - note.get_width()) // 2, 120 + (110 - snake_title.get_height()) // 2 + snake_title.get_height()))

    snake_settings = ['snake name:', 'species:', 'snake color:']
    grid_settings = ['size:', 'bg color:', 'line color:']
    gameplay_settings = ['speed:', 'at the edge:', 'movement:']
    handle_settings(win, settings_pos, 'snake_settings', snake_settings, 0, 200)
    handle_settings(win, settings_pos, 'grid_settings', grid_settings, 640, 490)
    handle_settings(win, settings_pos, 'gameplay_settings', gameplay_settings, 640, 200)
    handle_settings(win, settings_pos, 'food_settings', None, 0, 520)

    pygame.display.update()

def settings(win):
    run = True
    slide = True
    background_image = background
    settings_pos = {}

    with open('sounds\\sound.txt', 'r') as f:
        sound = int(f.read())
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if 1180 < mouse_position[0] < 1260 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'quit'
                elif 1060 < mouse_position[0] < 1140 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    sound = not sound
                    with open('sounds\\sound.txt', 'w') as f:
                        f.write(str(int(sound)))
                elif 940 < mouse_position[0] < 1020 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'back'
                change_settings(settings_pos, mouse_position)

        if not sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        mouse_position = pygame.mouse.get_pos()

        if 940 < mouse_position[0] < 1020 and 20 < mouse_position[1] < 100:    #specials
            background_image = over_back
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 1060 < mouse_position[0] < 1140 and 20 < mouse_position[1] < 100:
            background_image = over_sound
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 1180 < mouse_position[0] < 1260 and 20 < mouse_position[1] < 100:
            background_image = over_quit
            if sound and slide:
                slideover_music.play()
                slide = False
        else:
            background_image = background
            slide = True

        draw(win, background_image, settings_pos)