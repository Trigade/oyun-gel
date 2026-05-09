import pygame
import random
from config.state import State
from config.land import Land
from models.bird import Bird
from models.pipe import Pipe


class GameState(State):
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Arial", 30)

        self.bg = pygame.image.load(r"images\bg_day.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (400, 600))
        self.manager.music.load_music(r"audio\coin.wav")

        self.game_started = False
        self.is_game_over = False

        self.lands = pygame.sprite.Group()
        for i in range(4):
            self.lands.add(Land(i * 166))

        self.pipes = pygame.sprite.Group()
        self.bird = Bird(300)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)

        self.score = 0
        self.pipe_timer = 0
        self.pipe_frequency = 1500

    def spawn_pipes(self):
        x_pos = 450
        gap_size = 150
        gap_center = random.randint(150, 400)

        top_y = gap_center - (gap_size // 2)
        # TODO
        top_pipe = Pipe(x_pos, top_y, True)

        bottom_y = gap_center + (gap_size // 2)
        bottom_pipe = Pipe(x_pos, bottom_y, False)

        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys

                sys.exit()

            if event.type == pygame.KEYDOWN or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                if not self.game_started:
                    self.game_started = True
                    self.bird.zipla()
                    self.pipe_timer = pygame.time.get_ticks()  # Zamanlayıcıyı başlat
                elif not self.is_game_over:
                    self.bird.zipla()

    def update(self):
        self.lands.update()
        if len(self.lands) < 4:
            self.lands.add(Land(400))

        if self.game_started and not self.is_game_over:
            current_time = pygame.time.get_ticks()
            if current_time - self.pipe_timer > self.pipe_frequency:
                self.spawn_pipes()
                self.pipe_timer = current_time

            # TODO
            self.all_sprites.update()

            if pygame.sprite.spritecollide(
                self.bird, self.pipes, False, pygame.sprite.collide_mask
            ):  #
                self.is_game_over = True

            for land in self.lands:
                if pygame.sprite.collide_mask(self.bird, land):
                    self.is_game_over = True

            if self.bird.rect.top <= -13 or self.bird.rect.bottom >= 564:
                self.is_game_over = True

            for pipe in self.pipes:
                # TODO
                if (
                    not hasattr(pipe, "scored")
                    and pipe.rect.right < self.bird.rect.left
                ):
                    if hasattr(pipe, "is_top") and not pipe.is_top:
                        self.score += 1
                        pipe.scored = True

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        self.pipes.draw(screen)
        self.lands.draw(screen)
        screen.blit(self.bird.image, self.bird.rect)

        if not self.game_started:
            ready_font = pygame.font.SysFont("Arial", 30, bold=True)
            ready_surf = ready_font.render("Hazırsan 'Space' bas", True, (255, 215, 0))
            ready_rect = ready_surf.get_rect(center=(200, 500))
            screen.blit(ready_surf, ready_rect)

        score_surf = self.font.render(f"Skor: {self.score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        if self.is_game_over:
            go_font = pygame.font.SysFont("Arial", 50, bold=True)
            go_surf = go_font.render("OYUN BİTTİ", True, (200, 0, 0))
            go_rect = go_surf.get_rect(center=(200, 300))
            screen.blit(go_surf, go_rect)
