import pygame
from pygame import mixer
import time

pygame.init()

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

FONT = pygame.font.Font('2Dumb.ttf', 50)
background = pygame.image.load('multiplayer_folder\\background_multiplayer.png')
over_sound = pygame.image.load('multiplayer_folder\\over_sound.png')
over_back = pygame.image.load('multiplayer_folder\\over_back.png')

background_music = pygame.mixer.Sound('sounds\\background_music.wav')
background_music.set_volume(0.5)
background_music.play(-1)

slideover_music = pygame.mixer.Sound('sounds\\sliding_over_option.wav')
slideover_music.set_volume(0.5)
click_music = pygame.mixer.Sound('sounds\\click.wav')
click_music.set_volume(10.0)

def draw(win, rectangle_colors, background_image):
    offline = FONT.render('Offline', True, BLACK)
    online = FONT.render('Online', True, BLACK)

    win.blit(background_image, (0, 0))

    for i in range(2):
        pygame.draw.rect(win, rectangle_colors[i], (580, 250 + 150 * i, 440, 100)) # Pos and dimensions predetermined
    
    win.blit(offline, (580 + (440 - offline.get_width()) // 2, 250 + (100 - offline.get_height()) // 2))
    win.blit(online, (580 + (440 - online.get_width()) // 2, 400 + (100 - online.get_height()) // 2))

    pygame.display.update()

def multiplayer(win):
    run = True
    slide = True
    rectangle_colors = [WHITE, WHITE]
    background_image = background

    with open('sounds\\sound.txt', 'r') as f:
        sound = int(f.read())
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if 820 < mouse_position[0] < 900 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'main_menu'
                elif 700 < mouse_position[0] < 780 and 20 < mouse_position[1] < 100:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    sound = not sound
                    with open('sounds\\sound.txt', 'w') as f:
                        f.write(str(int(sound)))
                elif 580 < mouse_position[0] < 1020 and 250 < mouse_position[1] < 350:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'offline'
                elif 580 < mouse_position[0] < 1020 and 400 < mouse_position[1] < 500:
                    if sound: click_music.play()
                    time.sleep(0.5)
                    return 'online'

        if not sound:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        mouse_position = pygame.mouse.get_pos()

        if 580 < mouse_position[0] < 1020 and 250 < mouse_position[1] < 350:    #mode
            rectangle_colors = [GREY, WHITE]
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 580 < mouse_position[0] < 1020 and 400 < mouse_position[1] < 500:
            rectangle_colors = [WHITE, GREY]
            if sound and slide:
                slideover_music.play()
                slide = False

        elif 700 < mouse_position[0] < 780 and 20 < mouse_position[1] < 100:
            background_image = over_sound
            if sound and slide:
                slideover_music.play()
                slide = False
        elif 820 < mouse_position[0] < 900 and 20 < mouse_position[1] < 100:
            background_image = over_back
            if sound and slide:
                slideover_music.play()
                slide = False
        else:
            rectangle_colors = [WHITE, WHITE]
            background_image = background
            slide = True

        draw(win, rectangle_colors, background_image)