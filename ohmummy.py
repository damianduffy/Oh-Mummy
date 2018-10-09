import pygame
from pygame.locals import *
from pytmx import load_pygame
import os
import random
import math

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


# Define helper functions
def load_image(name, colorkey = None):
    fullname = os.path.join('data/img/', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
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


def distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def check_collision(player, enemy_list):
    player_center = player.get_center()
    hit_dist = 32

    for enemy in enemy_list:
        if distance(player_center, enemy.get_center()) < hit_dist:
            return True 
    return False


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
            "4": OPEN,
            "5": ENTRANCE,
            "7": EXIT
        }
        self.map_secrets = [
            [2, 2], [2, 4], [2, 6], [2, 8],
            [4, 2], [4, 4], [4, 6], [4, 8],
            [6, 2], [6, 4], [6, 6], [6, 8],
            [8, 2], [8, 4], [8, 6], [8, 8],
        ]
        self.door = [5, 0]
        self.map_target = 16
        self.map_unlocked = []
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
    
    def check_tile_passable(self, pos):
        tile = [pos[0] // self.tile_size, pos[1] // self.tile_size]
        if self.map[tile[1]][tile[0]] % 2 == 0:
            return False
        return True
    
    def get_tile_value(self, tile):
        return self.map[tile[1]][tile[0]]
    
    def set_tile_value(self, tile, value):
        self.map[tile[1]][tile[0]] = value
    
    def update(self, player):
        for tile in self.map_secrets:
            if self.check_surrounded(tile, 3) == 8:
                self.map[tile[1]][tile[0]] = 4
                self.map_unlocked.append(tile)
                self.map_secrets.remove(tile)
                player.scored(5)

        if len(self.map_unlocked) == self.map_target:
            self.map[self.door[1]][self.door[0]] = 7

    def check_surrounded(self, tile, value):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.map[tile[1] + i][tile[0] + j] == value:
                    count += 1
        return count


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.pos = pos
        self.vel_x = 0
        self.vel_y = 0
        self.move_speed = 4
        self.image = load_image("explorer.png")
        self.rect = self.image.get_rect()
        self.size = 32
        self.dest_pos = [pos[0], pos[1]]
        self.moving_x = False
        self.moving_y = False
        self.image_frame = 0
        self.image_direction = "SOUTH"
        self.image_max_frames = 4
        self.animate_clock = 0
        self.animate_speed = 180        # lower number is faster
        self.image_animate = {
            "NORTH": 0,
            "SOUTH": 1,
            "WEST": 2,
            "EAST": 3,
            "DEAD": 4
        }
    
    def draw(self):
        if pygame.time.get_ticks() >= self.animate_clock + self.animate_speed:
            self.animate()
        screen.blit(self.image, self.pos, ((self.image_frame * self.size), (self.image_animate[self.image_direction] * self.size), 32, 32))

    def update(self, map):
        if self.moving_x == True:
            if self.arrived_x():
                next_move_pos = [self.dest_pos[0] + (self.size * self.vel_x), self.dest_pos[1]]
                if map.check_tile_passable(next_move_pos):
                    self.dest_pos[0] = next_move_pos[0]
        else:
            if self.arrived_x():
                self.vel_x = 0
        
        if self.moving_y == True:
            if self.arrived_y():
                next_move_pos = [self.dest_pos[0], self.dest_pos[1] + (self.size * self.vel_y)]
                if map.check_tile_passable(next_move_pos):
                    self.dest_pos[1] = next_move_pos[1]
        else:
            if self.arrived_y():
                self.vel_y = 0
        
        x_vel = self.get_delta(self.pos[0], self.dest_pos[0])
        y_vel = self.get_delta(self.pos[1], self.dest_pos[1])

        # update player position
        self.pos[0] = self.pos[0] + (self.move_speed * x_vel)
        self.pos[1] = self.pos[1] + (self.move_speed * y_vel)

        # select correct sprite depending on which direction player facing
        if x_vel < 0:
            self.image_direction = "WEST"
        elif x_vel > 0:
            self.image_direction = "EAST"
        elif y_vel > 0:
            self.image_direction = "SOUTH"
        elif y_vel < 0:
            self.image_direction = "NORTH"

        # update the map tile
        if map.get_tile_value(self.get_current_tile()) == 1:
            map.set_tile_value(self.get_current_tile(), 3)
        
        # display the score
        print("SCORE:", self.score)
    
    def animate(self):
        self.animate_clock = pygame.time.get_ticks()
        if self.vel_x != 0 or self.vel_y != 0:
            self.image_frame += 1
            if self.image_frame == self.image_max_frames:
                self.image_frame = 0
        else:
            self.image_frame = 0
        
    def arrived_x(self):
        if self.pos[0] == self.dest_pos[0]:
            return True
        return False
    
    def arrived_y(self):
        if self.pos[1] == self.dest_pos[1]:
            return True
        return False

    def get_delta(self, orig, dest):
        if dest - orig > 0:
            return 1
        elif dest - orig < 0:
            return -1
        else:
            return 0

    def get_current_tile(self):
        return [self.pos[0] // self.size, self.pos[1] // self.size]

    def get_pos(self):
        return self.pos
    
    def get_center(self):
        return [self.pos[0] + (self.size // 2), self.pos[1] + (self.size // 2)]

    def set_vel_x(self, direction):
        if direction != 0:
            self.moving_x = True
            self.vel_x = direction
        else:
            self.moving_x = False
    
    def set_vel_y(self, direction):
        if direction != 0:
            self.moving_y = True
            self.vel_y = direction
        else:
            self.moving_y = False

    def scored(self, value):
        self.score += value

class Mummy(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel_x = 0
        self.vel_y = 0
        self.move_speed = 2
        self.image = load_image("mummy.png")
        self.rect = self.image.get_rect()
        self.size = 32
        self.dest_pos = [pos[0], pos[1]]
        self.moving_x = False
        self.moving_y = False
        self.image_frame = 0
        self.image_direction = "SOUTH"
        self.image_max_frames = 4
        self.animate_clock = 0
        self.animate_speed = 180        # lower number is faster
        self.image_animate = {
            "NORTH": 0,
            "SOUTH": 1,
            "WEST": 2,
            "EAST": 3,
            "DEAD": 4
        }

    def draw(self):
        if pygame.time.get_ticks() >= self.animate_clock + self.animate_speed:
            self.animate()
        screen.blit(self.image, self.pos, ((self.image_frame * self.size), (self.image_animate[self.image_direction] * self.size), 32, 32))

    def update(self, map, player):
        # if stationary, select next tile to move to based on player location and available routes
        if self.pos == self.dest_pos and self.pos != player.get_pos():
            # check what surrounding tiles are passable
            valid_routes = [False, False, False, False]
            if map.check_tile_passable([self.pos[0], self.pos[1] - self.size]):
                # north
                valid_routes[0] = True
            if map.check_tile_passable([self.pos[0], self.pos[1] + self.size]):
                # south
                valid_routes[1] =True
            if map.check_tile_passable([self.pos[0] + self.size, self.pos[1]]):
                # east
                valid_routes[2] = True
            if map.check_tile_passable([self.pos[0] - self.size, self.pos[1]]):
                # west
                valid_routes[3] = True
            
            self.set_dest_pos(player.get_pos(), valid_routes)

        # update position based on delta to dest tile
        self.pos[0] = self.pos[0] + (self.move_speed * self.get_delta(self.pos[0], self.dest_pos[0]))
        self.pos[1] = self.pos[1] + (self.move_speed * self.get_delta(self.pos[1], self.dest_pos[1]))
    
    def animate(self):
        self.animate_clock = pygame.time.get_ticks()
        
        self.image_frame += 1
        if self.image_frame == self.image_max_frames:
            self.image_frame = 0
        
    def get_delta(self, orig, dest):
        if dest - orig > 0:
            return 1
        elif dest - orig < 0:
            return -1
        else:
            return 0

    def get_pos(self):
        return self.pos
    
    def get_center(self):
        return [self.pos[0] + (self.size // 2), self.pos[1] + (self.size // 2)]

    def get_current_tile(self):
        return [self.pos[0] // self.size, self.pos[1] // self.size]
    
    def set_dest_pos(self, player_pos, valid_moves):
        prefer_x = False
        prefer_y = False

        delta_x = player_pos[0] - self.pos[0]
        delta_y = player_pos[1] - self.pos[1]

        if abs(delta_x) > abs(delta_y):
            if valid_moves[2] == True or valid_moves[3] == True:
                prefer_x = True
            else:
                prefer_y = True
        else:
            if valid_moves[0] == True or valid_moves[1] == True:
                prefer_y = True
            else:
                prefer_x = True

        if prefer_x == True:
            if valid_moves[2] == True and delta_x > 0:
                # go east
                self.dest_pos[0] = self.dest_pos[0] + self.size
                self.image_direction = "EAST"
            elif valid_moves[3] == True and delta_x < 0:
                # go west
                self.dest_pos[0] = self.dest_pos[0] - self.size
                self.image_direction = "WEST"
        else:
            if valid_moves[0] == True and delta_y < 0:
                # go north
                self.dest_pos[1] = self.dest_pos[1] - self.size
                self.image_direction = "NORTH"
            elif valid_moves[1] == True and delta_y > 0:
                # go south
                self.dest_pos[1] = self.dest_pos[1] + self.size
                self.image_direction = "SOUTH"


def main():
    # create the map
    level_map = Map()
    background_track = load_sound("oh-mummy.ogg")

    # create the dashboard
    
    # create the player
    player = Player([160, 0])

    # load a mob
    enemies = []
    enemies.append(Mummy([32, 32]))
    enemies.append(Mummy([32 * 8, 32]))
    enemies.append(Mummy([32, 32 * 8]))
    
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
        player.update(level_map)
        for enemy in enemies:
            enemy.update(level_map, player)
        level_map.update(player)
        print("End game:", check_collision(player, enemies))
        
        # clear the screen before drawing
        screen.fill(AMAZON)

        # write draw code here
        level_map.draw(screen)
        player.draw()
        for enemy in enemies:
            enemy.draw()

        # display whatever is drawn
        pygame.display.update()

        # run at pre-set fps
        clock.tick(FPS)

if __name__ == '__main__':
    main()
