import pygame
from config.state import State
from config.button import Button

class GameOverState(State):
    def __init__(self, manager, final_score, screenshot): # screenshot parametresini ekledik
        self.manager = manager
        self.score = final_score
        self.background_image = screenshot # Oyunun donmuş son karesi
        
        # Kararma katmanı
        self.overlay = pygame.Surface((400, 600))
        self.overlay.fill((0, 0, 0))
        self.current_alpha = 0  
        self.target_alpha = 120 

        # Diğer görseller ve butonlar
        self.over_image = pygame.transform.scale(pygame.image.load(r"images\text_game_over.png"), (200, 60))
        self.panel_image = pygame.transform.scale(pygame.image.load(r"images\score_panel.png"), (240, 126))
        self.retry_btn = Button(r"images\button_resume.png", 140, 480, 50, 50) 
        self.menu_btn = Button(r"images\button_menu.png", 260, 480, 100, 50)
        self.score_font = pygame.font.SysFont("Arial", 30)
        self.high_score = self.get_high_score()

    def get_high_score(self):
        try:
            with open("score.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self, score):
        with open("score.txt", "w") as f:
            f.write(str(score))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            
            # TODO: 'R' tuşuna veya 'Space'e basınca oyunu yeniden başlat
            if self.retry_btn.is_clicked(event):
                from config.game_state import GameState
                self.manager.change(GameState(self.manager))
            
            # Menü Butonu
            if self.menu_btn.is_clicked(event):
                from config.menu_state import MenuState
                self.manager.change(MenuState(self.manager))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.retry_btn.update(mouse_pos)
        self.menu_btn.update(mouse_pos)

        if self.current_alpha < self.target_alpha:
            self.current_alpha += 4 # Kararma hızı
            if self.current_alpha > self.target_alpha:
                self.current_alpha = self.target_alpha
            self.overlay.set_alpha(self.current_alpha)

    def draw(self, screen):
        # 1. Önce oyunun o anki "donmuş" fotoğrafını çiz
        screen.blit(self.background_image, (0, 0))

        # 2. Üzerine kararma katmanını çiz
        screen.blit(self.overlay, (0, 0))

        # 3. Paneli ve butonları çiz
        screen.blit(self.over_image, (100, 200))
        screen.blit(self.panel_image, (80, 270))
        self.retry_btn.draw(screen)
        self.menu_btn.draw(screen)
        
        # Skorları çiz
        score_surf = self.score_font.render(f"{self.score}", True, (255, 255, 255))
        high_surf = self.score_font.render(f"{self.high_score}", True, (255, 215, 0))
        screen.blit(score_surf, score_surf.get_rect(center=(270, 315)))
        screen.blit(high_surf, high_surf.get_rect(center=(270, 360)))