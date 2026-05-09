import pygame


class MusicManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.sounds = {}
        self.is_muted = False
        self.volume = 0.5

    def load_music(self, file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(self.volume)
        except pygame.error as e:
            print(f"Müzik yüklenemedi: {e}")

    def play_music(self, loop=-1):
        if not self.is_muted:
            pygame.mixer.music.play(loop)

    def stop_music(self, fade_time=800):
        pygame.mixer.music.fadeout(fade_time)

    def load_sound(self, name, file_path):
        try:
            self.sounds[name] = pygame.mixer.Sound(file_path)
            self.sounds[name].set_volume(self.volume)
        except pygame.error as e:
            print(f"Ses efekti yüklenemedi: {e}")

    def play_sound(self, name):
        if name in self.sounds and not self.is_muted:
            self.sounds[name].play()

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
