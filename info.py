import pygame
from pygame import mixer
import time
import csv

pygame.font.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 77)

FONT = pygame.font.Font('2Dumb.ttf', 20)
FONT1 = pygame.font.SysFont('comicsans', 20)
FONT2 = pygame.font.SysFont('comicsans', 40)
background = pygame.image.load('info_folder\\background_info.png')
over_back = pygame.image.load('info_folder\\over_back.png')
over_sound = pygame.image.load('info_folder\\over_sound.png')
over_settings = pygame.image.load('info_folder\\over_settings.png')
over_quit = pygame.image.load('info_folder\\over_quit.png')
blur = pygame.image.load('info_folder\\blur.png')

background_music = pygame.mixer.Sound('sounds\\background_music.wav')
background_music.set_volume(0.5)
background_music.play(-1)

slideover_music = pygame.mixer.Sound('sounds\\sliding_over_option.wav')
slideover_music.set_volume(0.5)
click_music = pygame.mixer.Sound('sounds\\click.wav')
click_music.set_volume(10.0)

def draw(win, background_image, blured_part):
    win.blit(background_image, (0, 0))

    if blured_part == 'pb':
        win.blit(blur, (60, 100))
        title = FONT2.render('Personal Bests', True, BLACK)
        win.blit(title, (60 + (460 - title.get_width()) // 2, 100 + (90 - title.get_height()) // 2))
        with open('info_folder\\personal_bests.csv', 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)
            i = 1
            for item in items:
                string = FONT1.render(item['num'] + '   ' + item['name'] + '    ' + item['score'] + '    ' + item['date'], True, BLACK)
                win.blit(string, (60 + (460 - string.get_width()) // 2, 145 + 45 * i + (45 - string.get_height()) // 2))
                i += 1

    elif blured_part == 'h2h':
        win.blit(blur, (60, 100))
        title = FONT2.render('Result History', True, BLACK)
        win.blit(title, (60 + (460 - title.get_width()) // 2, 100 + (90 - title.get_height()) // 2))
        with open('info_folder\\result_history.csv') as f:
            reader = csv.DictReader(f)
            items = list(reader)
            i = 1
            for item in items:
                string = FONT1.render(item['home'] + '  ' + item['score'] + '   ' + item['away'] + '    ' + item['date'], True, BLACK)
                win.blit(string, (60 + (460 - string.get_width()) // 2, 145 + 45 * i + (45 - string.get_height()) // 2))
                i += 1
    
    with open('info_folder\\info.txt', 'r') as f:
        i = 0
        while (text := f.readline()) != '':
            if (text[0] == '!'):
                text_ = FONT.render(text[1:], True, DARK_BLUE)
            else:
                text_ = FONT.render(text, True, BLACK)
            win.blit(text_, (580 + (440 - text_.get_width()) // 2, 250 + 40 * i + (40 - text_.get_height()) // 2))
            i += 1

    pygame.display.update()

def info(win):
    run = True
    slide = True
    background_image = background
    blured_part = False

    with open('sounds\\sound.txt', 'r') as f:
        sound = int(f.read())
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if 940 < mouse_position[0] < 1020 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'quit'
                elif 700 < mouse_position[0] < 780 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    sound = not sound
                    with open('sounds\\sound.txt', 'w') as f:
                        f.write(str(int(sound)))
                elif 580 < mouse_position[0] < 660 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'back'
                elif 820 < mouse_position[0] < 900 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'settings'
                elif 631 < mouse_position[0] < 969 and 493 < mouse_position[1] < 526:
                    if blured_part == False or blured_part == 'h2h': blured_part = 'pb'
                    else: blured_part = False
                elif 645 < mouse_position[0] < 955 and 533 < mouse_position[1] < 566:
                    if blured_part == False or blured_part == 'pb': blured_part = 'h2h'
                    else: blured_part = False

        if not sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        mouse_position = pygame.mouse.get_pos()

        if 580 < mouse_position[0] < 640 and 20 < mouse_position[1] < 100:    #specials
            background_image = over_back
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 700 < mouse_position[0] < 780 and 20 < mouse_position[1] < 100:
            background_image = over_sound
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 820 < mouse_position[0] < 900 and 20 < mouse_position[1] < 100:
            background_image = over_settings
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 940 < mouse_position[0] < 1020 and 20 < mouse_position[1] < 100:
            background_image = over_quit
            if sound and slide:
                slideover_music.play()
                slide = False
        else:
            background_image = background
            slide = True

        draw(win, background_image, blured_part)