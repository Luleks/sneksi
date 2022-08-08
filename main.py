import pygame
from main_menu import main_menu
from info import info
from settings import settings
from singleplayer import singleplayer
from multiplayer import multiplayer
from offline import offline
from client import online
from ai_menu import ai_menu

WIDTH, HEIGHT = 1280, 700

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sneksi by Lule')

if __name__ == '__main__':
    main_menu_run = True
    info_run = False
    settings_run = False
    singleplayer_run = False
    multiplayer_run = False
    offline_run = False
    online_run = False
    ai_run = False
    game_run = True

    while game_run:

        if main_menu_run:
            running = main_menu(win)
            main_menu_run = False
            if running == 'singleplayer':
                singleplayer_run = True
            elif running == 'multiplayer':
                multiplayer_run = True
            elif running == 'ai':
                ai_run = True
            elif running == 'info':
                info_run = True
            elif running == 'settings':
                settings_run = True
            elif running == 'quit':
                game_run = False
        
        elif info_run:
            running = info(win)
            info_run = False
            if running == 'back':
                main_menu_run = True
            elif running == 'settings':
                settings_run = True
            elif running == 'quit':
                game_run = False
        
        elif settings_run:
            running = settings(win)
            settings_run = False
            if running == 'back':
                main_menu_run = True
            elif running == 'quit':
                game_run = False

        elif singleplayer_run:
            running = singleplayer(win)
            singleplayer_run = False
            if running == 'main_menu':
                main_menu_run = True
            elif running == 'quit':
                game_run = False

        elif multiplayer_run:
            running = multiplayer(win)
            multiplayer_run = False
            if running == 'main_menu':
                main_menu_run = True
            elif running == 'quit':
                game_run = False
            elif running == 'offline':
                offline_run = True
            elif running == 'online':
                online_run = True
    
        elif offline_run:
            running = offline(win)
            offline_run = False
            if running == 'quit':
                game_run = False
            elif running == 'main_menu':
                main_menu_run = True
        
        elif online_run:
            while True:
                running = online(win)
                break
            online_run = False
            if running == 'quit':
                game_run = False
            elif running == 'main_menu':
                main_menu_run = True

        elif ai_run:
            running = ai_menu(win)
            if running == 'quit':
                game_run = False
            elif running == 'main_menu':
                main_menu_run = True
        
    pygame.quit()