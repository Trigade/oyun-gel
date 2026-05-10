import pygame
from config.button import Button
from config.land import Land


class MenuState:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Arial", 20)

        # TODO

        self.is_fading = False
        self.shadow_alpha = 0
        self.shadow_surf = pygame.Surface((400, 600))
        self.shadow_surf.fill((0, 0, 0))
        self.title = pygame.transform.scale((pygame.image.load(r"images\title.png")),(270,75))
        self.bg = pygame.image.load(r"images\bg_day.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (400, 600))

        self.bird = pygame.image.load(r"images\bird_mid.png").convert_alpha()
        self.bird = pygame.transform.scale(self.bird, (72, 72))
        self.lands = pygame.sprite.Group()
        for i in range(4):
            self.lands.add(Land(i * 166))

        self.start_btn = Button(r"images\button_play.png", 100, 500, 120, 70)
        self.exit_btn = Button(r"images\button_score.png", 300, 500, 120, 70)
        self.buttons = [self.start_btn,self.exit_btn]

    def enter(self):
        self.manager.music.load_music(r"audio/theme.ogg")
        self.manager.music.play_music()

    def exit(self):
        pass

    def handle_events(self, events):
        for event in events:
            if not self.is_fading:
                if self.start_btn.is_clicked(event):
                    self.manager.music.stop_music()
                    self.is_fading = True
                if self.exit_btn.is_clicked(event):
                    pass

    def update(self):
        if not self.is_fading:
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                btn.update(mouse_pos)
        else:
            self.shadow_alpha += 5
            if self.shadow_alpha >= 255:
                self.shadow_alpha = 255
            if self.shadow_alpha == 255:
                from config.game_state import GameState

                self.manager.music.stop_music()
                self.manager.change(GameState(self.manager))

        self.lands.update()
        if len(self.lands) < 4:
            self.lands.add(Land(400))

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        self.lands.draw(screen)
        screen.blit(self.bird, (164, 200))

        screen.blit(self.title, (65, 120))
        for btn in self.buttons:
            btn.draw(screen)

        if self.shadow_alpha > 0:
            self.shadow_surf.set_alpha(self.shadow_alpha)
            screen.blit(self.shadow_surf, (0, 0))
