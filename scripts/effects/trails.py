import math
import random

import pygame

from scripts.effects.particle import Particle
from scripts.effects.spark import Spark


class ProjectileTrails:
    def __init__(self, game):
        self.game = game

    def basic_wisp_trail(self, projectile):
        proj_rect = pygame.Rect(*projectile[0], *projectile[2])
        pvelocity = [projectile[1][0] * -0.5, projectile[1][1] * -0.5]
        self.game.particles.append(
            Particle(self.game, 'particle' if random.randint(1, 10) == 1 else "shadow",
                     proj_rect.center, velocity=pvelocity, frame=random.randint(0, 7)))

    def basic_projectile_burst(self, projectile, num_projectiles=10):
        proj_rect = pygame.Rect(*projectile[0], *projectile[2])
        for num in range(num_projectiles):
            angle = random.random() * math.pi * 2
            speed = random.random() * 0.5 + 0.5
            pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
            self.game.particles.append(
                Particle(self.game, 'shadow', proj_rect.center,
                         velocity=pvelocity, frame=random.randint(0, 7)))

    def simple_wisp_trail(self, projectile):
        proj_rect = pygame.Rect(*projectile[0], *projectile[2])
        pvelocity = [projectile[1][0] * -0.7, projectile[1][1] * -0.7]
        self.game.particles.append(
            Particle(self.game, 'particle' if random.randint(1, 10) == 1 else "shadow",
                     proj_rect.center, velocity=pvelocity, frame=random.randint(0, 7)))
        if random.randint(1, 7) == 1:
            pos = (proj_rect.center[0] - projectile[1][0] * 2.3, proj_rect.center[1] - projectile[1][1] * 2.3)
            self.game.sparks.append(
                Spark(pos,
                      math.radians(math.degrees(math.atan2(pvelocity[1], pvelocity[0])) % 360 + random.randint(-10, 10)),
                      2.5, color=random.choice(
                        [(255, 155, 255), (205, 105, 205), (155, 55, 155), (155, 55, 255)]))
            )

    def simple_projectile_burst(self, projectile, num_projectiles=13):
        proj_rect = pygame.Rect(*projectile[0], *projectile[2])
        for num in range(num_projectiles):
            angle = random.random() * math.pi * 2
            speed = random.random() * 0.5 + 0.6
            pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
            self.game.particles.append(
                Particle(self.game, 'shadow', proj_rect.center,
                         velocity=pvelocity, frame=random.randint(0, 7)))
        for spark in range(num_projectiles // 5):
            angle = random.random() * math.pi * 2
            speed = random.random() * 0.5 + 0.8
            pvelocity = math.atan2(*[math.sin(angle) * speed, math.cos(angle) * speed])
            self.game.sparks.append(
                Spark(proj_rect.center, pvelocity, 2, random.choice(
                        [(255, 155, 255), (205, 105, 205), (155, 55, 155), (155, 55, 255)])))

    def standard_wisp_trail(self, projectile):
        proj_rect = pygame.Rect(*projectile[0], *projectile[2])
        pvelocity = [projectile[1][0] * -0.9, projectile[1][1] * -0.9]
        self.game.particles.append(
            Particle(self.game, 'particle' if random.randint(1, 10) == 1 else "shadow",
                     proj_rect.center, velocity=pvelocity, frame=random.randint(0, 7)))
        if random.randint(1, 5) == 1:
            pos = (proj_rect.center[0] - projectile[1][0] * 2.3, proj_rect.center[1] - projectile[1][1] * 2.3)
            self.game.sparks.append(
                Spark(pos,
                      math.radians(math.degrees(math.atan2(pvelocity[1], pvelocity[0])) % 360 + random.randint(-10, 10)),
                      2.5, color=random.choice(
                        [(255, 155, 255), (205, 105, 205), (155, 55, 155), (155, 55, 255)]))
            )

    def standard_projectile_burst(self, projectile, num_projectiles=16):
        proj_rect = pygame.Rect(*projectile[0], *projectile[2])
        for num in range(num_projectiles):
            angle = random.random() * math.pi * 2
            speed = random.random() * 0.5 + 0.6
            pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
            self.game.particles.append(
                Particle(self.game, 'shadow', proj_rect.center,
                         velocity=pvelocity, frame=random.randint(0, 7)))
        for spark in range(num_projectiles // 3):
            angle = random.random() * math.pi * 2
            speed = random.random() * 0.5 + 0.8
            pvelocity = math.atan2(*[math.sin(angle) * speed, math.cos(angle) * speed])
            self.game.sparks.append(
                Spark(proj_rect.center, pvelocity, 2, random.choice(
                        [(255, 155, 255), (205, 105, 205), (155, 55, 155), (155, 55, 255)])))
