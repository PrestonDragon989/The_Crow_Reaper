import math

import pygame


class DayNightCycle:
    def __init__(self):
        self.time = 0.9
        self.change_speed = 0.0009

        self.day_time = 0.9
        self.night_time = 5

        self.day_locked = False
        self.night_locked = False

    def update(self, display):
        darkness = (max(0, min(math.sin(self.time) * 500, 100)))

        new_display = pygame.Surface(display.get_size(), pygame.SRCALPHA)
        new_display.fill((155 + darkness, (darkness * 0.1) * 25 + 5, 155 + darkness))
        new_display.blit(display, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        if self.day_locked:
            self.time = self.day_time
        elif self.night_locked:
            self.time = self.night_time
        else:
            self.time += self.change_speed

        return new_display
