import pygame
import random
from config.state import State
from config.land import Land
from config.button import Button
from models.bird import Bird
from models.pipe import Pipe

class GameState(State):
    def __init__(self, manager):
        self.manager = manager
        self.is_paused = False
        self.pause_start_time = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.bg = pygame.image.load(r"images\bg_day.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (400, 600))
        self.manager.music.load_music(r"audio\bg.mp3")
        self.manager.music.load_sound("coin", r"audio/coin.wav")
        self.manager.music.load_sound("jump", r"audio/zipla.wav")
        self.ready_image = pygame.transform.scale((pygame.image.load(r"images\text_ready.png")),(200,60))
        self.tutorial_image = pygame.transform.scale((pygame.image.load(r"images\tutorial.png")),(120,100))
        self.pause_btn = Button(r"images\button_pause.png", 360, 40, 40, 40)

        self.number_images = [
            pygame.transform.scale(
                pygame.image.load(f"images/{i}.png").convert_alpha(), 
                (30,55)
            ) for i in range(10)
        ]

        self.manager.music.play_music()

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
            if self.pause_btn.is_clicked(event)or (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
                if not self.is_paused:
                    self.pause_start_time = pygame.time.get_ticks()
                    self.is_paused = True
                else:
                    pause_duration = pygame.time.get_ticks() - self.pause_start_time
                    self.pipe_timer += pause_duration
                    self.is_paused = False
                return
            
            if not self.is_paused:
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                ):
                    if not self.game_started:
                        self.game_started = True
                        self.bird.zipla()
                        self.manager.music.play_sound("jump")
                        self.pipe_timer = pygame.time.get_ticks()
                    elif not self.is_game_over:
                        self.bird.zipla()
                        self.manager.music.play_sound("jump")

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.pause_btn.update(mouse_pos)

        if self.is_paused: #
            mouse_pos = pygame.mouse.get_pos()
            self.pause_btn.update(mouse_pos)
            return

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

            if self.is_game_over:
                self.manager.music.stop_music()
                self.manager.music.play_sound("hit") # Çarpma sesi
                
                from config.game_over_state import GameOverState
                screenshot = pygame.display.get_surface().copy()
                self.manager.change(GameOverState(self.manager, self.score, screenshot))

            for pipe in self.pipes:
                # TODO
                if (
                    not hasattr(pipe, "scored")
                    and pipe.rect.right < self.bird.rect.left
                ):
                    if hasattr(pipe, "is_top") and not pipe.is_top:
                        self.manager.music.play_sound("coin")
                        self.score += 1
                        pipe.scored = True
                        
    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        self.pipes.draw(screen)
        self.lands.draw(screen)
        screen.blit(self.bird.image, self.bird.rect)
        self.pause_btn.draw(screen)
        if not self.game_started:
            screen.blit(self.ready_image,(100,200))
            screen.blit(self.tutorial_image,(140,400))

        if self.is_paused:
            pause_overlay = pygame.Surface((400, 600), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 100)) # Siyah, yarı saydam
            screen.blit(pause_overlay, (0, 0))
            
            p_font = pygame.font.SysFont("Arial", 50, bold=True)
            p_surf = p_font.render("DURAKLATILDI", True, (255, 255, 255))
            p_rect = p_surf.get_rect(center=(200, 300))
            screen.blit(p_surf, p_rect)
            
            hint_surf = self.font.render("Devam etmek için butona basın", True, (200, 200, 200))
            screen.blit(hint_surf, hint_surf.get_rect(center=(200, 360)))

        if self.is_game_over:
            go_font = pygame.font.SysFont("Arial", 50, bold=True)
            go_surf = go_font.render("OYUN BİTTİ", True, (200, 0, 0))
            go_rect = go_surf.get_rect(center=(200, 300))
            screen.blit(go_surf, go_rect)
        self.draw_score(screen)
    
    def draw_score(self, screen):
        score_str = str(self.score)
        
        total_width = 0
        for char in score_str:
            total_width += self.number_images[int(char)].get_width() + 2
            
        start_x = (400 - total_width) // 2
        y_pos = 50
        for char in score_str:
            img = self.number_images[int(char)]
            screen.blit(img, (start_x, y_pos))
            start_x += img.get_width() + 2
