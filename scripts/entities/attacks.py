import math
import random

import pygame

from scripts.effects.particle import Particle
from scripts.effects.trails import ProjectileTrails


class PlayerAttacks:
    def __init__(self, player, game):
        self.game = game
        self.player = player

        self.trails = ProjectileTrails(self.game)

        self.basic_wisp_speed = 1.5
        self.last_basic_wisp = 0
        self.basic_wisp_timer = 45

        self.simple_wisp_speed = 1.9
        self.last_simple_wisp = 0
        self.simple_wisp_timer = 40

    def update(self):
        self.last_basic_wisp = max(0, self.last_basic_wisp - 1)
        self.last_simple_wisp = max(0, self.last_simple_wisp - 1)

    def get_projectile_rect(self, pos, size):
        return pygame.Rect(pos[0], pos[1], size[0], size[1])

    def basic_wisp(self, mouse_pos):
        if not self.last_basic_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed = (self.basic_wisp_speed * math.cos(direction), self.basic_wisp_speed * math.sin(direction))

            # Player Projectile Structure | Pos     Slope    Size   Render   Death   Distance
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed, (3, 3), self.trails.basic_wisp_trail,
                                            self.trails.basic_projectile_burst, [0, 125]])
            self.last_basic_wisp += self.basic_wisp_timer

    def simple_wisp(self, mouse_pos):
        if not self.last_simple_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed = (self.simple_wisp_speed * math.cos(direction), self.simple_wisp_speed * math.sin(direction))

            # Player Projectile Structure | Pos     Slope    Size   Render   Death   Distance
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed, (3, 3), self.trails.simple_wisp_trail,
                                            self.trails.simple_projectile_burst, [0, 125]])
            self.last_simple_wisp += self.simple_wisp_timer
