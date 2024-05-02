import os

import pygame

from scripts.tilemap import AUTOTILE_TYPES, PHYSICS_TILES

BASE_IMG_PATH = 'data/images/'


def get_assets():
    assets = {
        # Player Animations
        "player/idle": Animation(load_images("entities/player/idle"), 15, loop=True),
        "player/run": Animation(load_images("entities/player/run"), 4, loop=True),
        "player/fly": Animation(load_images("entities/player/fly"), 4, loop=True),
        "player/flap": Animation(load_images("entities/player/flap"), 1, loop=False),

        # Tile sets
        "grass_custom": load_tileset("tiles/grass_1.png", sprite_size=(16, 16), columns=3, rows=3, flip=False),
        "grass": convert_to_autotile(load_images("tiles/grass", flip=False)),
        "stone": load_images("tiles/stone", flip=False),
        "decor": load_images("tiles/decor", flip=False),
        "large_decor": load_images("tiles/large_decor", flip=False),

        # Clouds
        "clouds": load_images("clouds"),

        # Background
        "background": load_image("background.png"),

        # Particles
        "particle/particle": Animation(load_images("particles/particle"), img_dur=6, loop=False),
        "particle/leaf": Animation(load_images("particles/leaf"), img_dur=20, loop=False),
        "particle/shadow": Animation(load_images("particles/shadow"), img_dur=6, loop=False),

        # Enemy Bow & Arrow
        "enemy/bow": load_spritesheet('entities/enemies/bow.png', (6, 10), (10, 10), 1),
        "enemy/arrow": [pygame.transform.scale(load_spritesheet('entities/enemies/arrow.png', (7, 1), (7, 7), 1)[0], (15, 2))],

        # Curser
        "cursor": load_image("cursor.png"),

        # Pixel Font
        "font": pygame.font.Font("data/images/pixelFont.ttf", 16)
    }
    # Adding each enemy color for Idle & Run
    enemy_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    for color in enemy_colors:
        assets[f"enemy/{color}/idle"] = Animation(load_spritesheet(f'entities/enemies/{color}/idle.png', (13, 17), (18, 18), 16), img_dur=6)
        assets[f"enemy/{color}/run"] = Animation(load_spritesheet(f'entities/enemies/{color}/run.png', (13, 17), (18, 18), 7), img_dur=4)

    # Adding Tinted Colors
    for color in [((255, 0, 0), "red"), ((255, 155, 0), "orange"), ((255, 233, 0), "yellow"), ((0, 255, 0), "green"), ((0, 0, 255), "blue"), ((0, 0, 155), "cyan"), ((100, 100, 255), "light_cyan"), ((255, 0, 180), "purple")]:
        for tile in ["grass", "grass_custom", "stone", "decor", "large_decor"]:
            if tile != "grass_custom":
                assets[f"{tile}_{color[1]}"] = tint_images(load_images(f"tiles/{tile}"), color[0])
                if tile == "grass":
                    assets[f"{tile}_{color[1]}"] = convert_to_autotile(assets[f"{tile}_{color[1]}"])
            if tile == "grass_custom":
                assets[f"{tile}_{color[1]}"] = tint_images(load_tileset("tiles/grass_1.png", sprite_size=(16, 16), columns=3, rows=3, flip=False), color[0])
            if tile in PHYSICS_TILES:
                AUTOTILE_TYPES.add(f"{tile}_{color[1]}")
                PHYSICS_TILES.add(f"{tile}_{color[1]}")

    return assets


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path, flip=False):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    if flip:
        images.reverse()
    return images


def convert_to_autotile(images):
    new_order = []
    for change in [0, 1, 2, 5, 8, 4, 6, 3, 7]:
        new_order.append(images[change])
    return new_order


def load_spritesheet(path, sprite_size=(0, 0), cell_size=(0, 0), sprites=1, flip=False):
    images = []
    spritesheet_image = load_image(path)
    for i in range(sprites):
        images.append(spritesheet_image.subsurface(pygame.Rect(cell_size[0] * i, 0, sprite_size[0], sprite_size[1])))
    if flip:
        images.reverse()
    return images


def load_tileset(path, sprite_size=(0, 0), columns=1, rows=1, flip=False, convert_for_autotile=True):
    images = []
    spritesheet_image = load_image(path)
    for row in range(rows):
        for col in range(columns):
            location = (sprite_size[0] * col, sprite_size[1] * row)
            images.append(spritesheet_image.subsurface(pygame.Rect(location[0], location[1], sprite_size[0], sprite_size[1])))
    if convert_for_autotile:
        new_order = []
        for change in [0, 1, 2, 5, 8, 7, 6, 3, 4]:
            new_order.append(images[change])
        images = new_order
    if flip:
        images.reverse()
    return images


def tint_images(images, color):
    tinted_images = []
    for img in images.copy():
        new_display = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        new_display.fill(color)
        img.blit(new_display, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        tinted_images.append(img)
    return tinted_images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]