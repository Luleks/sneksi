import pygame
from pygame import mixer
import time

pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

FONT = pygame.font.Font('2Dumb.ttf', 50)
background = pygame.image.load('main_menu_folder\\background_main.png')
over_info = pygame.image.load('main_menu_folder\\over_info.png')
over_sound = pygame.image.load('main_menu_folder\\over_sound.png')
over_settings = pygame.image.load('main_menu_folder\\over_settings.png')
over_quit = pygame.image.load('main_menu_folder\\over_quit.png')

background_music = pygame.mixer.Sound('sounds\\background_music.wav')
background_music.set_volume(0.5)
#background_music.play(-1)

slideover_music = pygame.mixer.Sound('sounds\\sliding_over_option.wav')
slideover_music.set_volume(0.5)
click_music = pygame.mixer.Sound('sounds\\click.wav')
click_music.set_volume(10.0)

def draw(win, rectangle_colors, background_image):
    singleplayer = FONT.render('Singleplayer', True, BLACK)
    multiplayer = FONT.render('Multiplayer', True, BLACK)
    ai = FONT.render('AI plays Sneksi', True, BLACK)

    win.blit(background_image, (0, 0))

    for i in range(3):
        pygame.draw.rect(win, rectangle_colors[i], (580, 250 + 150 * i, 440, 100)) # Pos and dimensions predetermined
    
    win.blit(singleplayer, (580 + (440 - singleplayer.get_width()) // 2, 250 + (100 - singleplayer.get_height()) // 2))
    win.blit(multiplayer, (580 + (440 - multiplayer.get_width()) // 2, 400 + (100 - multiplayer.get_height()) // 2))
    win.blit(ai, (580 + (440 - ai.get_width()) // 2, 550 + (100 - ai.get_height()) // 2))
    
    pygame.display.update()

def main_menu(win):
    run = True
    slide = True
    rectangle_colors = [WHITE, WHITE, WHITE]
    background_image = background

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
                elif 580 < mouse_position[0] < 1020 and 250 < mouse_position[1] < 350:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'singleplayer'
                elif 580 < mouse_position[0] < 1020 and 400 < mouse_position[1] < 500:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'multiplayer'
                elif 580 < mouse_position[0] < 1020 and 550 < mouse_position[1] < 650:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'ai'
                elif 580 < mouse_position[0] < 660 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'info'
                elif 820 < mouse_position[0] < 900 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'settings' 

        if not sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        mouse_position = pygame.mouse.get_pos()

        if 580 < mouse_position[0] < 1020 and 250 < mouse_position[1] < 350:    #mode
            rectangle_colors = [GREY, WHITE, WHITE]
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 580 < mouse_position[0] < 1020 and 400 < mouse_position[1] < 500:
            rectangle_colors = [WHITE, GREY, WHITE]
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 580 < mouse_position[0] < 1020 and 550 < mouse_position[1] < 650:
            rectangle_colors = [WHITE, WHITE, GREY]
            if sound and slide:
                slideover_music.play()
                slide = False

        elif 580 < mouse_position[0] < 640 and 20 < mouse_position[1] < 100:    #specials
            background_image = over_info
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
            rectangle_colors = [WHITE, WHITE, WHITE]
            background_image = background
            slide = True

        draw(win, rectangle_colors, background_image)