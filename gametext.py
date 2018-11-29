import pygame

class GameText():
    def __init__(self, valign = 1, halign = 1, size = 16, color = (255, 255, 255), bg_color = (0, 0, 0), border = 0, font = 'data/fnt/PressStart2P-Regular.ttf', animation = 0):
        self.message = "This is a test"
        self.display = True             # set to True for testing
        self.font = pygame.font.Font(font, size)
        self.valign = valign
        self.halign = halign
        self.color = color
        self.bg_color = bg_color
        self.border = border
    
    def set_display(self, state):
        # true state will result in message rendering
        self.display = state
    
    def draw(self, screen):
        if self.display:
            text = self.font.render(str(self.message), False, self.color)
            screen.blit(text, (5, 355))
    '''
    def set_message(self, message):
        if type(message) == str:
            self.message.append(message)
        else:
            for line in message:
                self.message.append(str(line))
    '''