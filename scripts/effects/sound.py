import pygame


class Sound:
    def __init__(self, game):
        self.game = game

        self.effects = {
            'flap': pygame.mixer.Sound('data/sound/effects/flap.wav'),
            'dash': pygame.mixer.Sound('data/sound/effects/dash.wav'),
            'shoot': pygame.mixer.Sound('data/sound/effects/shoot.wav'),
            'wisp_1': pygame.mixer.Sound('data/sound/effects/wisp_1.wav'),
            'wisp_2': pygame.mixer.Sound('data/sound/effects/wisp_2.wav'),
            'wisp_3': pygame.mixer.Sound('data/sound/effects/wisp_3.wav'),
            'hit_1': pygame.mixer.Sound('data/sound/effects/hit_1.wav'),
            'hit_2': pygame.mixer.Sound('data/sound/effects/hit_2.wav'),
            'hit_3': pygame.mixer.Sound('data/sound/effects/hit_3.wav'),
            'hit_4': pygame.mixer.Sound('data/sound/effects/hit_4.wav'),
        }
        self.effects['flap'].set_volume(0.55)
        self.effects['dash'].set_volume(0.5)
        self.effects['shoot'].set_volume(0.3)
        self.effects['hit_1'].set_volume(0.7)
        self.effects['hit_2'].set_volume(0.7)
        self.effects['hit_3'].set_volume(0.7)
        self.effects['hit_4'].set_volume(0.7)
        self.effects['wisp_1'].set_volume(0.15)
        self.effects['wisp_2'].set_volume(0.125)
        self.effects['wisp_3'].set_volume(0.2)

        self.music = {
            "hub_music": pygame.mixer.Sound('data/sound/music/basic_hub_music.mp3'),
            "level_music_1": pygame.mixer.Sound('data/sound/music/fight_level_music_1.mp3'),
            "level_music_2": pygame.mixer.Sound('data/sound/music/fight_level_music_2.mp3'),
            "level_music_3": pygame.mixer.Sound('data/sound/music/fight_level_music_3.mp3'),
            "level_music_4": pygame.mixer.Sound('data/sound/music/fight_level_music_4.mp3'),
            "level_music_5": pygame.mixer.Sound('data/sound/music/fight_level_music_5.mp3'),
            "level_music_6": pygame.mixer.Sound('data/sound/music/fight_level_music_6.mp3'),
        }
        self.music["hub_music"].set_volume(0.7)
        for tune in range(1, 6):
            self.music[f'level_music_{tune}'].set_volume(0.2)

    def play_music(self, music="hub"):
        pygame.mixer.stop()

        if music == "hub":
            self.music['hub_music'].play(-1)
        elif int(music) in range(1, 6):
            self.music[f'level_music_{music}'].play(-1)
        else:
            self.music['hub_music'].play(-1)
