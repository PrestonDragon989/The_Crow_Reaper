import pygame.font


class Text:
    def __init__(self, font, font_path):
        self.font = font
        self.font_path = font_path

        self.font_cache = {

        }

    def basic_display(self, surf, pos, text, color):
        surf.blit(self.font.render(text, False, color), pos)

    def sized_display(self, surf, pos, text, color, size):
        if str(size) in self.font_cache:
            surf.blit(self.font_cache[str(size)].render(text, False, color), pos)
        else:
            self.font_cache[str(size)] = pygame.font.Font(self.font_path, size)
            surf.blit(self.font_cache[str(size)].render(text, False, color), pos)

    def add_text_to_tilemap(self, tilemap, pos, text, color, size):
        tilemap.text.append({"pos": pos, "text": text, "color": color, "size": size})

    def show_last_souls(self, tilemap, player):
        self.add_text_to_tilemap(tilemap, (95, 30), f"Souls Collected: ", (255, 235, 255), 12)
        self.add_text_to_tilemap(tilemap, (76 + 112, 30), f"{player.last_soul_collection}", (44, 199, 199), 12)
