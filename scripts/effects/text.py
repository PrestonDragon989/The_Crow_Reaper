import pygame.font


class Text:
    def __init__(self, font, font_path):
        self.font = font
        self.font_path = font_path

    def basic_display(self, surf, pos, text, color):
        surf.blit(self.font.render(text, False, color), pos)

    def sized_display(self, surf, pos, text, color, size):
        surf.blit(pygame.font.Font(self.font_path, size).render(text, False, color), pos)
