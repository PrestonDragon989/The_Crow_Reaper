import math
import random
import sys

import moderngl
import pygame

import platform

from scripts.effects.sound import Sound
from scripts.renderer import Renderer

from scripts.effects.clouds import Clouds
from scripts.effects.day import DayNightCycle
from scripts.effects.particle import Particle
from scripts.effects.spark import Spark
from scripts.effects.text import Text
from scripts.entities.enemy import Enemy
from scripts.entities.player import Player
from scripts.levels import Levels
from scripts.sprites import get_assets
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()

        self.scale = 4 if "Linux" in platform.platform() else 2

        self.width = 320
        self.height = 240

        pygame.display.set_caption("The Crow Reaper")
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale),
                                              pygame.OPENGL | pygame.DOUBLEBUF)
        self.display = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)

        self.renderer = Renderer()

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.assets = get_assets()

        self.sound = Sound(self)

        pygame.mouse.set_visible(False)

        self.player = Player(self, [20, 40], (13, 13))
        self.movement = [False, False]
        self.dead = 0

        self.enemies = []
        self.enemy_projectiles = []

        self.tilemap = Tilemap(self, tile_size=16)

        self.levels = Levels(self)
        self.levels.load_sections()

        self.dayNightCycle = DayNightCycle()

        self.clouds = Clouds(self.assets["clouds"], count=16)

        self.text = Text(self.assets['font'], "data/images/pixelFont.ttf")

        self.scroll = [0, 0]

        self.screenshake = 0

        self.particles = []
        self.sparks = []

        self.leaf_spawners = []

        self.transition = -30

        self.load_level(self.levels.current_level())

    def load_level(self, level, loading_4_5=False):
        level_path = "data/maps/" + str(level) + ".json"
        self.tilemap.load(level_path)

        self.levels.update_level_shaders()

        self.levels.update_level_music(self.sound)

        self.enemies.clear()
        self.enemy_projectiles.clear()
        for spawner in self.tilemap.extract(
                [('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3),
                 ('spawners', 4), ('spawners', 5), ('spawners', 6), ('spawners', 7)],
                keep=False
        ):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self,
                                          random.choice(['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
                                          if spawner['variant'] == 1
                                          else ['red', 'orange', 'yellow', 'green', 'blue', 'purple'][spawner['variant']
                                                                                                      - 2],
                                          spawner['pos'], (8, 15)))
                self.enemies[-1].flip = random.randint(0, 1) == 1

        self.leaf_spawners.clear()
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.particles.clear()
        self.sparks.clear()

        self.player.reset(int(self.levels.level) - 1, loading_4_5=loading_4_5)
        self.movement = [False, False]
        self.player.update_level_features()

        self.dayNightCycle.time = 0.9

        self.transition = -30
        self.screenshake = 0

        self.scroll = [0, 0]
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])

        self.dead = 0

    def run(self):
        while True:
            self.display.blit(self.dayNightCycle.update(self.assets["background"]), (0, 0))

            # Render Scroll
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 27
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 27
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            render_scroll = (int(render_scroll[0] + (random.random() * self.screenshake - self.screenshake / 2)),
                             int(render_scroll[1] + (random.random() * self.screenshake - self.screenshake / 2)))

            self.screenshake = max(0, self.screenshake - 1)

            if self.dead:
                self.dead += 1
                if self.dead == 10 or self.dead == 20 or self.dead == 40:
                    self.player.die_animation()
                if self.dead >= 10:
                    self.transition = min(self.transition + 1, 30)
                if self.dead > 40:
                    if not self.levels.reached_four:
                        self.load_level(self.levels.current_level())
                    else:
                        self.levels.level = 4
                        self.load_level("4.5", loading_4_5=True)
                        if self.player.first_death:
                            self.levels.add_first_death_respawn_message(self.tilemap, self.text)
                            self.player.first_death = not self.player.first_death

            if not len(self.enemies) and not self.dead:
                self.transition += 1
                if self.transition > 30:
                    self.levels.update_level()
                    self.load_level(self.levels.current_level())
            if self.transition < 0:
                self.transition += 1

            self.clouds.update()
            self.clouds.render(self.display, render_scroll)

            self.tilemap.render(self.display, self.text, render_scroll)

            for projectile in self.enemy_projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['enemy/arrow'][0]
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                                        projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.enemy_projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(
                            Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                                  2 + random.random()))
                elif projectile[2] > 360:
                    self.enemy_projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]) and not self.dead:
                        self.enemy_projectiles.remove(projectile)
                        self.dead += 1
                        self.player.die_animation()
                        self.sound.effects['hit_1'].set_volume(1)
                        self.sound.effects["hit_1"].play()
                        self.sound.effects['hit_1'].set_volume(0.7)

            for projectile in self.player.projectiles.copy():
                projectile[0][0] += projectile[1][0]
                projectile[0][1] += projectile[1][1]
                projectile[-1][0] += 1
                projectile[3](projectile)
                destroy = False
                proj_rect = pygame.Rect(*projectile[0], *projectile[2])
                for enemy in self.enemies.copy():
                    if enemy.rect().colliderect(proj_rect):
                        self.enemies.remove(enemy.die())
                        destroy = True
                if self.tilemap.solid_check(projectile[0]):
                    destroy = True
                elif projectile[-1][0] > projectile[-1][1]:
                    destroy = True
                if destroy:
                    projectile[4](projectile)
                    self.player.projectiles.remove(projectile)

            # Updating and Rendering Enemies
            for enemy in self.enemies.copy():
                if ((self.player.pos[0] - enemy.pos[0]) ** 2 + (
                        self.player.pos[1] - enemy.pos[1]) ** 2) ** 0.5 <= 310:
                    kill = enemy.update(self.tilemap, (0, 0))
                    enemy.render(self.display, offset=render_scroll)
                    if kill:
                        self.enemies.remove(enemy.die())

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            # Updating Leaves from trees
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos,
                                                   velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            # Updating and Rendering Particles / Sparks
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            for particle in self.particles.copy():
                if ((self.player.pos[0] - particle.pos[0]) ** 2 + (
                        self.player.pos[1] - particle.pos[1]) ** 2) ** 0.5 <= 310:
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill:
                        self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = ((pygame.mouse.get_pos()[0] / self.scale) + self.scroll[0],
                                     (pygame.mouse.get_pos()[1] / self.scale) + self.scroll[1])
                        self.player.left_weapon(mouse_pos)
                    if event.button == 3:
                        mouse_pos = ((pygame.mouse.get_pos()[0] / self.scale) + self.scroll[0],
                                     (pygame.mouse.get_pos()[1] / self.scale) + self.scroll[1])
                        self.player.right_attack(mouse_pos)

                # Getting Key Down Presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True

                    if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.player.jump()

                    if event.key == pygame.K_LSHIFT:
                        self.player.dash()

                    if event.key == pygame.K_l:
                        self.player.level += 1
                    if event.key == pygame.K_n:
                        self.levels.update_level()
                        self.load_level(self.levels.current_level())
                    if event.key == pygame.K_c:
                        self.player.right_weapon = self.player.attacks.level_10_right_weapons[-1]
                        print("Weapon is now", self.player.right_weapon)

                # Getting Key Up Presses
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            # Displaying Custom Curser
            self.display.blit(self.assets['cursor'],
                              (pygame.mouse.get_pos()[0] / self.scale - 8, pygame.mouse.get_pos()[1] / self.scale - 8))

            self.player.render_gui(self.display, self.text)

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255),
                                   (self.display.get_width() // 2, self.display.get_height() // 2),
                                   (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            scaled_display = pygame.transform.scale(self.display, self.screen.get_size())

            frame_tex = self.renderer.surf_to_texture(scaled_display)
            frame_tex.use(0)
            self.renderer.program['tex'] = 0
            self.renderer.render_object.render(mode=moderngl.TRIANGLE_STRIP)

            pygame.display.flip()

            frame_tex.release()

            self.clock.tick(self.fps)


if __name__ == '__main__':
    Game().run()
