import pygame
from config.state import State

class GameOverState(State):
    def __init__(self, manager, final_score):
        self.manager = manager
        self.score = final_score
        
        self.over_image = pygame.transform.scale((pygame.image.load(r"images\text_game_over.png")),(200,60))
        self.panel_image = pygame.transform.scale((pygame.image.load(r"images\score_panel.png")),(240,126))


        # Fontlar
        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.score_font = pygame.font.SysFont("Arial", 30)
        
        # Skor dosyasını oku/yaz (High Score için)
        self.high_score = self.get_high_score()
        if self.score > self.high_score:
            self.save_high_score(self.score)
            self.high_score = self.score

    def get_high_score(self):
        with open("score.txt", "r") as f:
            return int(f.read())

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                    from config.game_state import GameState
                    self.manager.change(GameState(self.manager))
                
                # 'M' tuşuna basınca menüye dön
                if event.key == pygame.K_m:
                    from config.menu_state import MenuState
                    self.manager.change(MenuState(self.manager))

    def update(self):
        pass # Bu ekranda genelde hareketli bir şey olmaz

    def draw(self, screen):
        
        # "GAME OVER" Yazısı
        screen.blit(self.over_image,(100,200))
        screen.blit(self.panel_image,(80,270))

        
        # Skorlar
        score_surf = self.score_font.render(f"{self.score}", True, (255, 255, 255))
        high_surf = self.score_font.render(f"{self.high_score}", True, (255, 215, 0))
        
        screen.blit(score_surf, score_surf.get_rect(center=(270, 315)))
        screen.blit(high_surf, high_surf.get_rect(center=(270, 360)))
        
        # İpucu
        hint_surf = self.score_font.render("Tekrar: SPACE | Menü: M", True, (200, 200, 200))
        screen.blit(hint_surf, hint_surf.get_rect(center=(200, 500)))