import json
import math
import random

from scripts.effects.particle import Particle
from scripts.effects.spark import Spark
from scripts.entities.entity import PhysicsEntity

from scripts.entities.attacks import PlayerAttacks


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size, anim_offset=(-1, -3))

        self.assets = self.game.assets

        self.air_time = 0

        self.jumps = 2
        self.max_jumps = 2

        self.dashing = 0

        with open("data/info/souls.json", "r") as file:
            self.soul_data = json.load(file)
        with open("data/info/levels.json", "r") as file:
            self.level_data = json.load(file)

        self.level = 1
        self.last_level = 0
        self.souls = 0
        self.last_souls = -1

        self.projectiles = []

        self.attacks = PlayerAttacks(self, self.game)

        self.left_weapon = self.attacks.basic_wisp
        self.right_weapon = None

    def reset(self, last_level):
        self.dashing = 5

        self.projectiles.clear()

        self.air_time = 0
        self.jumps = self.max_jumps

        self.velocity = [0, 0]

        if not self.game.levels.reached_four:
            self.souls = int(self.soul_data[str(last_level)]["souls"])
            self.last_souls = self.souls - 1
            self.level = int(self.soul_data[str(last_level)]["level"])
            self.last_level = self.level - 1
        else:
            self.souls = int(self.soul_data[str(4.5)]["souls"])
            self.last_souls = self.souls - 1
            self.level = int(self.soul_data[str(4.5)]["level"])
            self.last_level = self.level - 1

    def update_level_features(self):
        self.max_jumps = 2 + max(0, math.floor(self.level / 2))
        self.jumps = self.max_jumps

        self.attacks.can_dash = self.level >= 2
        self.attacks.damage_dash = self.level >= 5

        if self.level >= 4:
            self.left_weapon = random.choice(self.attacks.level_3_left_weapons)
        elif self.level >= 3:
            self.left_weapon = self.attacks.standard_wisp
        elif self.level >= 2:
            self.left_weapon = self.attacks.simple_wisp
        elif self.level >= 0:
            self.left_weapon = self.attacks.basic_wisp

        self.last_level = self.level

    def check_falling_death(self, tilemap):
        if self.air_time >= (220 + (80 if self.jumps else 0)):
            if tilemap.can_see_point(self.pos, (self.pos[0], self.pos[1] + 100)):
                return True
        return False

    def update(self, tilemap, movement=(0, 0)):
        movement = [movement[0] * 1.2, movement[1] * 1.4]

        super().update(tilemap, movement=movement)

        self.air_time += 1

        if self.check_falling_death(tilemap):
            self.game.dead += 1
            self.die_animation()

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = self.max_jumps

        if self.air_time > 4 and not self.collisions['down']:
            if self.action == "flap" and not self.animation.done:
                self.set_action("flap")
            elif self.action == "flap" and self.animation.done:
                self.set_action("fly")
            else:
                self.set_action("fly")
        elif movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(
                    Particle(self.game, 'shadow', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(
                Particle(self.game, 'shadow', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
            speed = random.random() * 3.5
            pos = (self.rect().center[0], self.rect().center[1] + random.randint(-5, 5))
            self.game.sparks.append(Spark(pos,
                                          math.radians(180) if not self.flip else math.radians(1),
                                          speed, color=random.choice(
                    [(255, 155, 255), (205, 105, 205), (155, 55, 155), (155, 55, 255)])))

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        if self.last_souls != self.souls:
            for soul_num in list(self.level_data.keys())[::-1]:
                if self.souls >= int(soul_num):
                    self.level = self.level_data[soul_num]
                    break
            self.last_souls = self.souls

        if self.last_level != self.level:
            self.update_level_features()

        self.attacks.update()

    def jump(self):
        if self.jumps:
            self.set_action("flap")
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5

    def dash(self):
        if not self.dashing and self.attacks.can_dash:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60

    def left_attack(self, mouse_pos):
        self.attacks.player = self
        self.left_weapon(mouse_pos)

    def die_animation(self):
        self.game.screenshake = max(35, self.game.screenshake + 35)
        for i in range(165):
            angle = random.random() * math.pi * 2
            speed = random.random() * 5
            self.game.sparks.append(Spark(self.rect().center, angle, 3 + random.random(), color=random.choice(
                [(255, 155, 255), (205, 105, 205), (155, 55, 155), (155, 55, 255)])))
            for I in range(2):
                self.game.particles.append(Particle(self, 'particle', self.rect().center,
                                               velocity=[math.cos(angle + math.pi) * speed * 0.7,
                                                         math.sin(angle + math.pi) * speed * 0.7],
                                               frame=random.randint(0, 7)))
                self.game.particles.append(Particle(self, 'shadow', self.rect().center,
                                               velocity=[math.cos(angle + math.pi) * speed * 1.7,
                                                         math.sin(angle + math.pi) * speed * 1.7],
                                               frame=random.randint(0, 7)))

    def render_gui(self, surf, text):
        text.sized_display(surf, (5, 5), "Level: ", (0, 0, 0), 14)
        text.sized_display(surf, (50, 5), str(self.level), (40, 232, 19), 14)

        text.sized_display(surf, (5, 20), "Souls: ", (0, 0, 0), 14)
        text.sized_display(surf, (50, 20), str(self.souls), (44, 199, 199), 14)


