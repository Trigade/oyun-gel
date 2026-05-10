import pygame
from config.state import State
from config.button import Button

class GameOverState(State):
    def __init__(self, manager, final_score, screenshot):
        self.manager = manager
        self.score = final_score
        self.background_image = screenshot
        self.high_score = self.get_high_score()

        self.overlay = pygame.Surface((400, 600))
        self.overlay.fill((0, 0, 0))
        self.current_alpha = 0  
        self.target_alpha = 120 

        self.small_digit_width = 16
        self.small_digit_height = 24

        self.small_number_images = [
            pygame.transform.scale(
                pygame.image.load(f"images/{i}.png").convert_alpha(), 
                (self.small_digit_width, self.small_digit_height)
            ) for i in range(10)
        ]
        self.over_image = pygame.transform.scale(pygame.image.load(r"images\text_game_over.png"), (200, 60))
        self.panel_image = pygame.transform.scale(pygame.image.load(r"images\score_panel.png"), (240, 126))
        self.retry_btn = Button(r"images\button_resume.png", 140, 480, 50, 50) 
        self.menu_btn = Button(r"images\button_menu.png", 260, 480, 100, 50)
        self.score_font = pygame.font.SysFont("Arial", 30)

        if self.score > self.high_score:
            self.save_high_score(self.score)
            self.high_score = self.score
        
    def get_high_score(self):
        try:
            with open("score.txt", "r") as f:
                content = f.read().strip()
                if content: # Dosya boş değilse
                    return int(content)
                return 0
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self, score):
        try:
            with open("score.txt", "w") as f:
                f.write(str(score))
        except Exception as e:
            print(f"Skor kaydedilemedi: {e}")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            
            # TODO
            if self.retry_btn.is_clicked(event):
                from config.game_state import GameState
                self.manager.change(GameState(self.manager))
            
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
        screen.blit(self.background_image, (0, 0))

        screen.blit(self.overlay, (0, 0))

        screen.blit(self.over_image, (100, 200))
        screen.blit(self.panel_image, (80, 270))
        self.retry_btn.draw(screen)
        self.menu_btn.draw(screen)
        
        self.draw_panel_score(screen, self.score, 305)
        
        self.draw_panel_score(screen, self.high_score, 350)

    def draw_panel_score(self, screen, score, y_pos):
        score_str = str(score)
        padding = 2
        
        total_width = (len(score_str) * self.small_digit_width) + ((len(score_str) - 1) * padding)
        
        start_x = 270 - (total_width // 2)
        
        for char in score_str:
            digit_index = int(char)
            screen.blit(self.small_number_images[digit_index], (start_x, y_pos))
            start_x += self.small_digit_width + padding