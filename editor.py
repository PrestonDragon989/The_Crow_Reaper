import math
import sys
import os

import pygame

from tkinter import filedialog, colorchooser
from tkinter import simpledialog

from scripts.effects.day import DayNightCycle
from scripts.effects.text import Text
from scripts.sprites import load_images, load_spritesheet, load_tileset, load_image, tint_images, convert_to_autotile
from scripts.tilemap import Tilemap, PHYSICS_TILES, AUTOTILE_TYPES

RENDER_SCALE = 4.0  # USED TO BE 2.0


class Editor:
    def __init__(self):
        self.tilemap = Tilemap(self, tile_size=16)

        self.file, contin = self.get_file()
        print(f"Opened file: {self.file}")

        if not contin:
            return
        pygame.init()

        pygame.display.set_caption("editor")
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            "grass": convert_to_autotile(load_images("tiles/grass", flip=False)),
            'grass_custom': load_tileset('tiles/grass_1.png', (16, 16), 3, 3, convert_for_autotile=True),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners': [load_image('entities/player/idle/0.png'), load_image('entities/enemies/misc.png')],
        }
        # Adding Enemy Colors
        enemy_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        for color in enemy_colors:
            self.assets["spawners"].append(load_spritesheet(f'entities/enemies/{color}/idle.png', (18, 18), (18, 18), 1)[0].subsurface(pygame.Rect(3, 2, 9, 16)), )

        # Adding Tinted Colors
        for color in [((255, 0, 0), "red"), ((255, 155, 0), "orange"), ((255, 233, 0), "yellow"), ((0, 255, 0), "green"), ((0, 0, 255), "blue"), ((255, 0, 180), "purple")]:
            for tile in ["grass", "grass_custom", "stone", "decor", "large_decor"]:
                if tile != "grass_custom":
                    self.assets[f"{tile}_{color[1]}"] = tint_images(load_images(f"tiles/{tile}"), color[0])
                    if tile == "grass":
                        self.assets[f"{tile}_{color[1]}"] = convert_to_autotile(self.assets[f"{tile}_{color[1]}"])
                if tile == "grass_custom":
                    self.assets[f"{tile}_{color[1]}"] = tint_images(
                        load_tileset("tiles/grass_1.png", sprite_size=(16, 16), columns=3, rows=3, flip=False),
                        color[0])
                if tile in PHYSICS_TILES:
                    AUTOTILE_TYPES.add(f"{tile}_{color[1]}")
                    PHYSICS_TILES.add(f"{tile}_{color[1]}")

        self.movement = [False, False, False, False]

        # Background
        self.background = load_image("background.png")
        self.dayNightCycle = DayNightCycle()

        self.text = Text(pygame.font.Font("data/images/pixelFont.ttf", 16), "data/images/pixelFont.ttf")

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)

        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

        self.run()

    def get_file(self):
        file = filedialog.asksaveasfilename(initialdir='data/maps',
                                            title="Select JSON Map", confirmoverwrite=False)
        print(f"Opening {file}")
        try:
            if os.path.exists(file):
                self.tilemap.load(file)
                return file, True
        except TypeError:
            pass
        except KeyError:
            return file, True
        try:
            f = open(file, 'w')
            f.write('{\n\n}')
            f.close()
            print(f"Creating {file}")
            return file, True
        except TypeError or FileNotFoundError:
            return 'N/A', False

    def run(self):
        while True:
            self.display.blit(self.dayNightCycle.update(self.background), (0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, self.text, offset=render_scroll, optimize_offgrid=False, spawners=True)

            current_tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_image.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_image, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                       tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_image, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = \
                    {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1],
                                         tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
                for text in self.tilemap.text.copy():
                    text_rect = pygame.Rect(text['pos'][0] - self.scroll[0], text['pos'][1] - self.scroll[1],
                                            16, 16)
                    if text_rect.collidepoint(mpos):
                        self.tilemap.text.remove(text)

            self.display.blit(current_tile_image, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group],
                                                               'variant': self.tile_variant, 'pos': (mpos[0]
                                                                                                     + self.scroll[0],
                                                                                                     mpos[1] +
                                                                                                     self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save(self.file)
                        print(f"Saving {self.file}")
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_c:
                        self.tilemap = Tilemap(self, tile_size=16)
                        self.file, null = self.get_file()
                    if event.key == pygame.K_l:
                        text = simpledialog.askstring("What text do you want to display", "Please input text to be displayed: ")
                        size = simpledialog.askinteger("What size do you want it to display", "Please input font size:")
                        color = colorchooser.askcolor(title="Choose a color")[0]

                        self.tilemap.text.append({'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1]), 'text': text, "color": color, "size": size})

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.text.sized_display(self.display, (0, 228), f"Tile: {self.tile_list[self.tile_group]}", (0, 0, 0), 10)
            self.text.sized_display(self.display, (0, 219), f"Variant: {self.tile_variant}", (0, 0, 0), 10)
            self.text.sized_display(self.display, (235, 228), f"MPos: {round(mpos[0], 1)}, {round(mpos[1], 1)}", (0, 0, 0), 10)
            self.text.sized_display(self.display, (145, 228), f"Pos: {round(self.scroll[0], 1) + self.display.get_width() / 2}, {round(self.scroll[1], 1) + self.display.get_height() / 2}", (0, 0, 0), 10)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Editor()
    print(f"Closing {__file__}")
