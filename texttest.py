import pygame
from pygame.locals import *
from gametext import GameText

# Global configuration options
SCREENSIZE              = [352, 375]#[960, 540]
FPS                     = 30
TITLE                   = "Oh Mummy"
SHOW_MOUSE              = True
CURRENT_GAME_STATE      = 0
GAME_STATE_SPLASH       = 1
GAME_STATE_MENU         = 2
GAME_STATE_RUNNING      = 3
GAME_STATE_OVER         = 4
SOUND                   = True

AMAZON                  = (69, 139, 116)
WALL                    = (211, 84, 0)
OPEN                    = (0, 0 , 0)
PATH                    = (154, 125, 10)
EXIT                    = (93, 173, 226)
ENTRANCE                = (142, 68, 173)
TRAIL                   = (244, 208, 63)
BORDER                  = (146, 43, 33)

# Initialize game engine, screen and clock
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.mouse.set_visible(SHOW_MOUSE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 14)

def exit_game():
    exit()

def main():
    # create the map
    
    # create the player

    # create the dashboard
    
    # load a mob
    
    # create the Interface
    message = GameText()

    # start music

    while True:
        # write event handlers here
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit_game()
                if event.key == K_SPACE:
                    message.display(True)

        # write game logic here


        # clear the screen before drawing
        screen.fill(AMAZON)

        # write draw code here
        message.draw(screen)

        # display whatever is drawn
        pygame.display.update()

        # run at pre-set fps
        clock.tick(FPS)

if __name__ == '__main__':
    main()
