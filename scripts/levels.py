import os
import random


class Levels:
    def __init__(self, game):
        self.game = game

        self.level = 1
        self.level_section = 1

        self.reached_four = False

        self.level_sections = {
            "Levels are here. Neat, right?": True,
        }

    def load_sections(self):
        for file in os.listdir("data/maps"):
            if not file.endswith(".json") or os.path.isdir(f"data/maps/{file}"):
                maps = []
                for level in os.listdir(f"data/maps/{file}"):
                    maps.append(str(level)[:-5])
                maps.reverse()
                self.level_sections[str(file)] = maps

    def pick_map(self, level_section):
        return int(random.choice(self.level_sections[str(level_section)]))

    def current_level(self):
        if self.level <= 4:
            return str(self.level)
        else:
            return str(self.level) + "/" + str(self.level_section)

    def update_level(self):
        if self.level <= 3:
            self.level += 1
        else:
            self.reached_four = True
            if str(self.level + 1) in self.level_sections:
                self.level += 1
            self.level_section = self.pick_map(self.level)

