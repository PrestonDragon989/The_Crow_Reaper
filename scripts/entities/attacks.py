import math
import random

from scripts.effects.trails import ProjectileTrails


class PlayerAttacks:
    def __init__(self, player, game):
        self.game = game
        self.player = player

        self.trails = ProjectileTrails(self.game)

        self.level_4_left_weapons = [self.great_wisp, self.basic_dual_wisp, self.standard_backstab_wisp]
        self.level_4_right_weapons = [self.basic_beam]

        self.level_5_left_weapons = [self.amazing_wisp, self.basic_triple_wisp, self.standard_tripstab_wisp]
        self.level_5_right_weapons = [self.simple_beam]

        self.level_6_left_weapons = [self.standard_bow_wisp, self.standard_dual_wisp, self.standard_hexastab_wisp]
        self.level_6_right_weapons = [self.standard_beam]

        self.level_7_left_weapons = [self.standard_triple_wisp, self.perfect_wisp, self.standard_nonastab_wisp]
        self.level_7_right_weapons = [self.great_beam]

        self.level_8_left_weapons = [self.great_bow_wisp, self.basic_quad_wisp, self.standard_decastab_wisp]
        self.level_8_right_weapons = [self.amazing_beam]

        self.level_9_left_weapons = [self.perfect_bow_wisp, self.standard_quad_wisp, self.standard_multistab_wisp]
        self.level_9_right_weapons = [self.perfect_beam]

        self.level_10_left_weapons = [self.true_reaper_bow_wisp, self.true_reaper_wisp, self.basic_true_reaper_swarm_wisp]
        self.level_10_right_weapons = [self.true_reaper_beam]

        self.can_dash = False
        self.damage_dash = False

        self.basic_wisp_speed = 1.5
        self.last_basic_wisp = 0
        self.basic_wisp_timer = 45

        self.simple_wisp_speed = 1.7
        self.last_simple_wisp = 0
        self.simple_wisp_timer = 42

        self.standard_wisp_speed = 1.9
        self.last_standard_wisp = 0
        self.standard_wisp_timer = 40

        self.great_wisp_speed = 2.05
        self.last_great_wisp = 0
        self.great_wisp_timer = 40

        self.last_basic_beam = 0
        self.basic_beam_timer = 43

        self.basic_dual_wisp_speed = 1.5
        self.last_basic_dual_wisp = 0
        self.basic_dual_wisp_timer = 40

        self.standard_backstab_wisp_speed = 1.9
        self.last_standard_backstab_wisp = 0
        self.standard_backstab_wisp_timer = 39

    def update(self):
        self.last_basic_wisp = max(0, self.last_basic_wisp - 1)
        self.last_simple_wisp = max(0, self.last_simple_wisp - 1)
        self.last_standard_wisp = max(0, self.last_standard_wisp - 1)
        self.last_great_wisp = max(0, self.last_great_wisp - 1)
        self.last_basic_beam = max(0, self.last_basic_beam - 1)
        self.last_basic_dual_wisp = max(0, self.last_basic_dual_wisp - 1)
        self.last_standard_backstab_wisp = max(0, self.last_standard_backstab_wisp - 1)

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
            self.game.sound.effects["wisp_1"].play()

    def simple_wisp(self, mouse_pos):
        if not self.last_simple_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed = (self.simple_wisp_speed * math.cos(direction), self.simple_wisp_speed * math.sin(direction))
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed, (3, 3), self.trails.simple_wisp_trail,
                                            self.trails.simple_projectile_burst, [0, 125]])
            self.last_simple_wisp += self.simple_wisp_timer
            self.game.sound.effects["wisp_1"].play()

    def standard_wisp(self, mouse_pos):
        if not self.last_standard_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed = (self.standard_wisp_speed * math.cos(direction), self.standard_wisp_speed * math.sin(direction))
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed, (3, 3), self.trails.standard_wisp_trail,
                                            self.trails.standard_projectile_burst, [0, 125]])
            self.last_standard_wisp += self.standard_wisp_timer
            self.game.sound.effects["wisp_3"].play()

    def great_wisp(self, mouse_pos):
        if not self.last_great_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed = (self.great_wisp_speed * math.cos(direction), self.great_wisp_speed * math.sin(direction))
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed, (3, 3), self.trails.great_wisp_trail,
                                            self.trails.great_projectile_burst, [0, 125]])
            self.last_great_wisp += self.great_wisp_timer
            self.game.sound.effects["wisp_3"].play()

    def amazing_wisp(self, mouse_pos):
        if not self.last_great_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed = ((self.great_wisp_speed + 0.4) * math.cos(direction),
                     (self.great_wisp_speed + 0.4) * math.sin(direction))
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed, (3, 3), self.trails.great_wisp_trail,
                                            self.trails.great_projectile_burst, [0, 125]])
            self.last_great_wisp += self.great_wisp_timer - 4
            self.game.sound.effects["wisp_3"].play()

    def perfect_wisp(self, mouse_pos):
        if not self.last_great_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed = ((self.great_wisp_speed + 0.7) * math.cos(direction),
                     (self.great_wisp_speed + 0.7) * math.sin(direction))
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed, (4, 4), self.trails.perfect_wisp_trail,
                                            self.trails.perfect_projectile_burst, [0, 125]])
            self.last_great_wisp += self.great_wisp_timer - 9
            self.game.sound.effects["wisp_3"].play()

    def true_reaper_wisp(self, mouse_pos):
        if not self.last_great_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            speed_1 = ((self.great_wisp_speed + 1.3) * math.cos(direction),
                       (self.great_wisp_speed + 1.3) * math.sin(direction))
            speed_2 = ((self.great_wisp_speed + 1.3 / 2) * math.cos(direction),
                       (self.great_wisp_speed + 1.3 / 2) * math.sin(direction))
            speed_3 = ((self.great_wisp_speed + 1.3 / 3) * math.cos(direction),
                       (self.great_wisp_speed + 1.3 / 3) * math.sin(direction))
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed_1, (4, 4), self.trails.true_reaper_wisp_trail,
                                            self.trails.true_reaper_projectile_burst, [0, 125]])
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed_2, (3, 3), self.trails.perfect_wisp_trail,
                                            self.trails.perfect_projectile_burst, [0, 125]])
            self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                            speed_3, (3, 3), self.trails.great_wisp_trail,
                                            self.trails.great_projectile_burst, [0, 125]])
            self.last_great_wisp += self.great_wisp_timer - 16
            self.game.sound.effects["wisp_3"].play()

    def basic_beam(self, mouse_pos):
        if not self.last_basic_beam:
            direction = math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                   mouse_pos[0] - self.player.rect().center[0])

            for i in range(3):
                pos = [self.player.rect().centerx + (i * 5.4) * math.cos(direction),
                       self.player.rect().centery + (i * 5.4) * math.sin(direction)]
                self.player.projectiles.append([pos,
                                                (0, 0), (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_wisp_trail, [0, 7]])
            self.last_basic_beam += self.basic_beam_timer + 6
            self.game.sound.effects["wisp_2"].play()

    def simple_beam(self, mouse_pos):
        if not self.last_basic_beam:
            direction = math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                   mouse_pos[0] - self.player.rect().center[0])

            for i in range(5):
                pos = [self.player.rect().centerx + (i * 5.4) * math.cos(direction),
                       self.player.rect().centery + (i * 5.4) * math.sin(direction)]
                self.player.projectiles.append([pos,
                                                (0, 0), (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_wisp_trail, [0, 7]])
            self.last_basic_beam += self.basic_beam_timer + 2
            self.game.sound.effects["wisp_2"].play()

    def standard_beam(self, mouse_pos):
        if not self.last_basic_beam:
            direction = math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                   mouse_pos[0] - self.player.rect().center[0])

            for i in range(9):
                pos = [self.player.rect().centerx + (i * 5.4) * math.cos(direction),
                       self.player.rect().centery + (i * 5.4) * math.sin(direction)]
                self.player.projectiles.append([pos,
                                                (0, 0), (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_wisp_trail, [0, 7]])
            self.last_basic_beam += self.basic_beam_timer + 2
            self.game.sound.effects["wisp_2"].play()

    def great_beam(self, mouse_pos):
        if not self.last_basic_beam:
            direction = math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                   mouse_pos[0] - self.player.rect().center[0])

            for i in range(13):
                pos = [self.player.rect().centerx + (i * 5.4) * math.cos(direction),
                       self.player.rect().centery + (i * 5.4) * math.sin(direction)]
                self.player.projectiles.append([pos,
                                                (0, 0), (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_wisp_trail, [0, 7]])
            self.last_basic_beam += self.basic_beam_timer + 4
            self.game.sound.effects["wisp_2"].play()

    def amazing_beam(self, mouse_pos):
        if not self.last_basic_beam:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                     mouse_pos[0] - self.player.rect().center[0]))
            for offset in [0, 1, 2, 3, 4, 5]:
                direct = math.radians((direction + (offset * 60)) % 360)
                if offset == 0:
                    num = 14
                else:
                    num = 6
                for i in range(num):
                    pos = [self.player.rect().centerx + (i * 5.4) * math.cos(direct),
                           self.player.rect().centery + (i * 5.4) * math.sin(direct)]
                    self.player.projectiles.append([pos,
                                                    (0, 0), (3, 3), self.trails.basic_wisp_trail,
                                                    self.trails.basic_wisp_trail, [0, 7]])
            self.last_basic_beam += self.basic_beam_timer + 5
            self.game.sound.effects["wisp_2"].play()

    def perfect_beam(self, mouse_pos):
        if not self.last_basic_beam:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0]))
            for offset in [0, 1, 2, 3, 4, 5]:
                direct = math.radians((direction + (offset * 60)) % 360)
                num = random.randint(12, 17)
                for i in range(num):
                    pos = [self.player.rect().centerx + (i * 5.4) * math.cos(direct),
                           self.player.rect().centery + (i * 5.4) * math.sin(direct)]
                    self.player.projectiles.append([pos,
                                                    (0, 0), (3, 3), self.trails.basic_wisp_trail,
                                                    self.trails.basic_wisp_trail, [0, 7]])
            self.last_basic_beam += self.basic_beam_timer + 8
            self.game.sound.effects["wisp_2"].play()

    def true_reaper_beam(self, mouse_pos):
        if not self.last_basic_beam:
            direction = math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                   mouse_pos[0] - self.player.rect().center[0])
            for offset in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                direct = math.radians((direction + (offset * 30)) % 360)
                num = random.randint(15, 22)
                for i in range(num):
                    pos = [self.player.rect().centerx + (i * 5.4) * math.cos(direct),
                           self.player.rect().centery + (i * 5.4) * math.sin(direct)]
                    self.player.projectiles.append([pos,
                                                    (0, 0), (3, 3), self.trails.basic_wisp_trail,
                                                    self.trails.basic_wisp_trail, [0, 7]])
            self.last_basic_beam += self.basic_beam_timer
            self.game.sound.effects["wisp_2"].play()

    def basic_dual_wisp(self, mouse_pos):
        if not self.last_basic_dual_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            offset_direction = math.radians(math.degrees(direction - 180) % 360)
            speed = (self.basic_dual_wisp_speed * math.cos(direction), self.basic_dual_wisp_speed * math.sin(direction))

            for offset in [-1, 1]:
                pos = [self.player.rect().centerx + (4 * offset) * math.cos(offset_direction),
                       self.player.rect().centery + (4 * offset) * math.sin(offset_direction)]

                self.player.projectiles.append([pos,
                                                speed, (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_projectile_burst, [0, 125]])
                self.last_basic_dual_wisp += self.basic_dual_wisp_timer
                self.game.sound.effects["wisp_1"].play(1)

    def standard_dual_wisp(self, mouse_pos):
        if not self.last_basic_dual_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            offset_direction = math.radians(math.degrees(direction - 180) % 360)
            speed = (self.standard_wisp_speed * math.cos(direction), self.standard_wisp_speed * math.sin(direction))

            for offset in [-1, 1]:
                pos = [self.player.rect().centerx + (4 * offset) * math.cos(offset_direction),
                       self.player.rect().centery + (4 * offset) * math.sin(offset_direction)]

                self.player.projectiles.append([pos,
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_basic_dual_wisp += self.basic_dual_wisp_timer
                self.game.sound.effects["wisp_1"].play(1)

    def standard_triple_wisp(self, mouse_pos):
        if not self.last_basic_dual_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            offset_direction = math.radians(math.degrees(direction - 180) % 360)
            speed = (self.standard_wisp_speed * math.cos(direction), self.standard_wisp_speed * math.sin(direction))

            for offset in [-1, 0, 1]:
                pos = [self.player.rect().centerx + (6 * offset) * math.cos(offset_direction),
                       self.player.rect().centery + (6 * offset) * math.sin(offset_direction)]

                self.player.projectiles.append([pos,
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_basic_dual_wisp += self.basic_dual_wisp_timer + 3
                self.game.sound.effects["wisp_1"].play(1)

    def basic_triple_wisp(self, mouse_pos):
        if not self.last_basic_dual_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            offset_direction = math.radians(math.degrees(direction - 180) % 360)
            speed = (self.basic_dual_wisp_speed * math.cos(direction), self.basic_dual_wisp_speed * math.sin(direction))

            for offset in [-1, 0, 1]:
                pos = [self.player.rect().centerx + (7 * offset) * math.cos(offset_direction),
                       self.player.rect().centery + (7 * offset) * math.sin(offset_direction)]

                self.player.projectiles.append([pos,
                                                speed, (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_projectile_burst, [0, 125]])
                self.last_basic_dual_wisp += self.basic_dual_wisp_timer
                self.game.sound.effects["wisp_1"].play(2)

    def standard_quad_wisp(self, mouse_pos):
        if not self.last_basic_dual_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            offset_direction = math.radians(math.degrees(direction - 180) % 360)
            speed = (self.basic_dual_wisp_speed * math.cos(direction), self.basic_dual_wisp_speed * math.sin(direction))

            for offset in [-1.25, -0.5, 0.5, 1.25]:
                pos = [self.player.rect().centerx + (7 * offset) * math.cos(offset_direction),
                       self.player.rect().centery + (7 * offset) * math.sin(offset_direction)]

                self.player.projectiles.append([pos,
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_basic_dual_wisp += self.basic_dual_wisp_timer
                self.game.sound.effects["wisp_1"].play(2)

    def basic_quad_wisp(self, mouse_pos):
        if not self.last_basic_dual_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            offset_direction = math.radians(math.degrees(direction - 180) % 360)
            speed = (self.basic_dual_wisp_speed * math.cos(direction), self.basic_dual_wisp_speed * math.sin(direction))

            for offset in [-1.25, -0.5, 0.5, 1.25]:
                pos = [self.player.rect().centerx + (7 * offset) * math.cos(offset_direction),
                       self.player.rect().centery + (7 * offset) * math.sin(offset_direction)]

                self.player.projectiles.append([pos,
                                                speed, (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_projectile_burst, [0, 125]])
                self.last_basic_dual_wisp += self.basic_dual_wisp_timer
                self.game.sound.effects["wisp_1"].play(2)

    def basic_true_reaper_swarm_wisp(self, mouse_pos):
        if not self.last_basic_dual_wisp:
            direction = math.radians(math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                             mouse_pos[0] - self.player.rect().center[0])) % 360)
            offset_direction = math.radians(math.degrees(direction - 180) % 360)
            speed = (self.basic_dual_wisp_speed * math.cos(direction),
                     self.basic_dual_wisp_speed * math.sin(direction))

            for offset in [-2, -1.75, -1.5, -1.25, -0.5, 0.5, 1.25, 1.5, 1.75, 2]:
                pos = [self.player.rect().centerx + (7 * offset) * math.cos(offset_direction),
                       self.player.rect().centery + (7 * offset) * math.sin(offset_direction)]

                self.player.projectiles.append([pos,
                                                speed, (3, 3), self.trails.basic_wisp_trail,
                                                self.trails.basic_projectile_burst, [0, 125]])
                self.last_basic_dual_wisp += self.basic_dual_wisp_timer
                self.game.sound.effects["wisp_1"].play(2)

    def standard_backstab_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [0, 1]:
                new_direction = math.radians((direction + (i * 180)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_standard_backstab_wisp += self.standard_backstab_wisp_timer
                self.game.sound.effects["wisp_2"].play(1)

    def standard_tripstab_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [0, 1, 2]:
                new_direction = math.radians((direction + (i * 120)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_standard_backstab_wisp += self.standard_backstab_wisp_timer - 5
                self.game.sound.effects["wisp_2"].play(1)

    def standard_hexastab_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [0, 1, 2, 3, 4, 5]:
                new_direction = math.radians((direction + (i * 60)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_standard_backstab_wisp += self.standard_backstab_wisp_timer - 5
                self.game.sound.effects["wisp_2"].play(2)

    def standard_nonastab_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                new_direction = math.radians((direction + (i * 40)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_standard_backstab_wisp += self.standard_backstab_wisp_timer - 10
                self.game.sound.effects["wisp_2"].play(2)

    def standard_decastab_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12, 14]:
                new_direction = math.radians((direction + (i * 24)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_standard_backstab_wisp += self.standard_backstab_wisp_timer - 10
                self.game.sound.effects["wisp_2"].play(2)

    def standard_multistab_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29]:
                new_direction = math.radians((direction + (i * 12)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
                self.last_standard_backstab_wisp += self.standard_backstab_wisp_timer - 10
                self.game.sound.effects["wisp_2"].play(2)

    def standard_bow_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [1, 0, -1]:
                new_direction = math.radians((direction + (i * 10)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
            self.last_standard_backstab_wisp += (self.standard_backstab_wisp_timer + 75)
            self.game.sound.effects["wisp_2"].play(1)

    def great_bow_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [1.5, 0.5, -0.5, -1.5]:
                new_direction = math.radians((direction + (i * 6.5)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
            self.last_standard_backstab_wisp += (self.standard_backstab_wisp_timer + 85)
            self.game.sound.effects["wisp_2"].play(2)

    def amazing_bow_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [1.5, 0.5, -0.5, -1.5]:
                new_direction = math.radians((direction + (i * 6.5)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
            self.last_standard_backstab_wisp += (self.standard_backstab_wisp_timer + 75)
            self.game.sound.effects["wisp_2"].play(2)

    def perfect_bow_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [1.5, 0.75, 0, -0.75, -1.5]:
                new_direction = math.radians((direction + (i * 6.5)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
            self.last_standard_backstab_wisp += (self.standard_backstab_wisp_timer + 72)
            self.game.sound.effects["wisp_2"].play(2)

    def true_reaper_bow_wisp(self, mouse_pos):
        if not self.last_standard_backstab_wisp:
            direction = math.degrees(math.atan2(mouse_pos[1] - self.player.rect().center[1],
                                                mouse_pos[0] - self.player.rect().center[0])) % 360
            for i in [3, 2.25, 1.5, 0.75, 0, -0.75, -1.5, -2.25, -3]:
                new_direction = math.radians((direction + (i * 6.5)) % 360)
                speed = (self.standard_backstab_wisp_speed * math.cos(new_direction),
                         self.standard_backstab_wisp_speed * math.sin(new_direction))
                self.player.projectiles.append([[self.player.rect().centerx, self.player.rect().centery],
                                                speed, (3, 3), self.trails.standard_wisp_trail,
                                                self.trails.standard_projectile_burst, [0, 125]])
            self.last_standard_backstab_wisp += (self.standard_backstab_wisp_timer + 67)
            self.game.sound.effects["wisp_2"].play(3)
