import pygame
from pygame.locals import *
from pytmx import load_pygame
import os

# Global configuration options
SCREENSIZE              = [960, 540]
FPS                     = 30
TITLE                   = "Oh Mummy"
SHOW_MOUSE              = True
CURRENT_GAME_STATE      = 0
GAME_STATE_SPLASH       = 1
GAME_STATE_MENU         = 2
GAME_STATE_RUNNING      = 3
GAME_STATE_OVER         = 4
SOUND                   = False

AMAZON                  = (69, 139, 116)
WALL                    = (211, 84, 0)
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

# Define helper functions
def load_image(name, colorkey = None):
    fullname = os.path.join('data/img/', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        print(os.getcwd())
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()

    return image # , image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer:
        return NoneSound()

    fullname = os.path.join('data/snd/', name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)

    return sound

def exit_game():
    exit()

def pause_game():
    pause = 0
    pygame.mixer.pause()

    while pause == 0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause = -1

    pygame.mixer.unpause()

class Dashboard():
    def __init__(self, filename):
        self.game_dashboard = load_pygame(filename)
        self.score = 0
        self.inventory = []
        self.keys = []
        self.ammo = 0
        self.lives = 0

    def draw(self, screen):
        for layer in self.game_dashboard.visible_layers:
            for x, y, gid, in layer:
                tile = self.game_dashboard.get_tile_image_by_gid(gid)
                if tile != None:
                    screen.blit(tile, (x * self.game_dashboard.tilewidth, 
                                y * self.game_dashboard.tileheight))
    
    def update(self, player):
        pass
        '''
        self.score = player.get_score()
        self.inventory = player.get_score()
        self.keys = player.get_keys()
        self.ammo = player.get_ammo()
        self.lives = player.get_lives()
        '''

class Map():
    def __init__(self):
        self.map = [
            # 0 - border
            # 1 - path (unwalked)
            # 2 - wall
            # 3 - path (walked)
            # 4 - TBC
            # 5 - exit / entrance
            [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.map_set = {
            "0": BORDER,
            "1": PATH,
            "2": WALL,
            "3": TRAIL,
            "4": "TBC",
            "5": ENTRANCE
        }
        self.tile_size = 32
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])

    def draw(self, screen):
        for row in range(self.map_width):            
            for col in range(self.map_height):
                pygame.draw.rect(
                    screen, 
                    self.map_set[str(self.map[row][col])], 
                    (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                )          
        

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.pos = pos
        self.vel_x = 0
        self.vel_y = 0
        self.move_speed = 4
        self.image = load_image("character_temp.png")
        self.rect = self.image.get_rect()
    
    def draw(self):
        screen.blit(self.image, (self.pos))
    
    def update(self):
        self.pos = [self.pos[0] + (self.move_speed * self.vel_x), 
                    self.pos[1] + (self.move_speed * self.vel_y)]
    
    def get_position(self):
        return self.pos
    
    def get_tile_position(self):
        tile_coords = [self.pos[0] // 32, self.pos[1] // 32]
        return tile_coords
    
    def set_vel_x(self, direction):
        self.vel_x = direction
    
    def set_vel_y(self, direction):
        self.vel_y = direction


def main():
    # create the map
    level_map = Map()

    # create the dashboard
    
    # create the player
    player = Player([160, 32])

    # load a mob
    
    # create the Interface
    
    # start music
    if SOUND == True:
        background_track.play(-1)

    while True:
        # write event handlers here
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit_game()
                if event.key == K_UP:
                    player.set_vel_y(-1)
                if event.key == K_DOWN:
                    player.set_vel_y(1)
                if event.key == K_LEFT:
                    player.set_vel_x(-1)
                if event.key == K_RIGHT:
                    player.set_vel_x(1)
                if event.key == K_SPACE:
                    pass
                if event.key == K_p:
                    pause_game()
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    player.set_vel_y(0)
                if event.key == K_LEFT or event.key == K_RIGHT:
                    player.set_vel_x(0)

        # write game logic here
        player.update()
        
        # clear the screen before drawing
        screen.fill(AMAZON)

        # write draw code here
        level_map.draw(screen)
        player.draw()

        # display whatever is drawn
        pygame.display.update()

        # run at pre-set fps
        clock.tick(FPS)

if __name__ == '__main__':
    main()
