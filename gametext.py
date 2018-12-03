import pygame
import math

class GameText():
    def __init__(self, screensize, valign = 1, halign = 1, size = 16, color = (255, 255, 255), bg_color = (0, 0, 0), border = 0, font = 'data/fnt/PressStart2P-Regular.ttf', animation = 0):
        self.message = "This is a test"
        self.display = True             # set to True for testing
        self.font = pygame.font.Font(font, size)
        self.valign = valign
        self.halign = halign
        self.xpos = 5
        self.ypos = 300
        self.color = color
        self.bg_color = bg_color
        self.border = border
        self.text = self.font.render(str(self.message), False, self.color)
        self.screen_width = screensize[0]
        self.screen_height = screensize[1]
        self.animate = True
        self.frame = 0
        self.max_frames = len(self.message)
        self.frame_cache = []
    
    def set_message(self, message):
        self.message = message
        # TBC - pass multiple messages in list

    def set_valign(self, value):
        # sets the vertical alignment of the text
        self.ypos = (self.screen_height // 2) - (self.text.get_rect().height // 2)
    
    def set_halign(self, value):
        # sets the horizontal alignment of the text
        self.xpos = (self.screen_width // 2) - (self.text.get_rect().width // 2)

    def set_display(self, state):
        # true state will result in message rendering
        self.display = state
    
    def animate_text(self):
        self.frame_cache = list(self.message)
        text = ""
        for i in range(0, self.frame):
            text += self.frame_cache[i]
        self.frame += 1
        if self.frame > self.max_frames:
            self.frame = 0
        return text
    
    def draw_border(self, icon):
        border_icon = self.font.render(icon, False, self.color)
        icon_width = border_icon.get_rect().width
        icon_height = border_icon.get_rect().height
        border_width = math.ceil((self.text.get_rect().width + 80) // icon_width)
        border_height = math.ceil(self.text.get_rect().height // icon_height)
        horizontal = ""
        vertical = ""
        for i in range(0, border_width):
            horizontal += icon
        return self.font.render(horizontal, False, self.color)

    def draw(self, screen):
        if self.display:
            bar = self.draw_border("#")
            x = (self.screen_width // 2) - (bar.get_rect().width // 2)
            y = 10
            screen.blit(bar, (x, y))
            msg = self.animate_text()
            text = self.font.render(str(msg), False, self.color)
            #text = self.font.render(str(self.message), False, self.color)
            screen.blit(text, (self.xpos, self.ypos))
            pygame.time.wait(100)
    '''
    def set_message(self, message):
        if type(message) == str:
            self.message.append(message)
        else:
            for line in message:
                self.message.append(str(line))
    '''