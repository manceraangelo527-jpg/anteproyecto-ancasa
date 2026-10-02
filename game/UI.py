import pygame

#display settings
height = 600
width = 800
height_text = 200
height_graphics = height - height_text

#Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
DARK_GRAY = (35, 35, 45)
TEXT_WHITE = (240, 240, 240)
GREEN_STATS = (100, 230, 130)
YELLOW_OPTION = (230, 220, 100)

class Interface_User:
    def __init__(self,):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ancasa Game: La Misión del Caballero")

        #Types of fonts
        self.text_source = pygame.font.SysFont("Arial", 18)
        self.text_stats_source = pygame.font.SysFont("Arial", 15, bold=True)
        self.text_option_source = pygame.font.SysFont("Arial", 18, bold=True)

        #Define screen areas
        self.rect_graphics = pygame.Rect(0, 0, width, height_graphics)
        self.rect_text = pygame.Rect(0, height_graphics, width, height_text)

    def draw(self, history_text, options, player):
        #Draw screen up
        pygame.draw.rect(self.screen, WHITE, self.rect_graphics)

        #Draw text area
        pygame.draw.rect(self.screen, DARK_GRAY, self.rect_text)
        pygame.draw.rect(self.screen, BLACK, self.rect_text, 3)

        #stats bar
        info_stats = f"Caballero: {player['name']} | Vida: {player['life']} HP | Dinero: {player['money']} monedas"
        sup_stats = self.text_stats_source.render(info_stats, True, GREEN_STATS)
        self.screen.blit(sup_stats, (20, 410))

        #texto Narrativo
        y_text = 435
        for line in history_text.split('\n'):
            sup_text = self.text_source.render(line, True, TEXT_WHITE)
            self.screen.blit(sup_text, (20, y_text))
            y_text += 22

        #Options
        y_opc = 515
        for opcion in options:
            sup_opc = self.text_option_source.render(opcion, True, YELLOW_OPTION)
            self.screen.blit(sup_opc, (30, y_opc))
            y_opc += 24

        pygame.display.flip()