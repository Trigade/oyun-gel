import pygame
import sys
from config.button import Button
from config.land import Land

class MenuState:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Arial", 20)
    
        #TODO
        self.bg = pygame.image.load(r"images\bg_day.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (400, 600))

        self.bird = pygame.image.load(r"images\bird_mid.png").convert_alpha()
        self.bird = pygame.transform.scale(self.bird, (72, 72))

        self.land1 = Land(0)
        self.land2 = Land(166)
        self.land3 = Land(330)
        self.land4 = Land(500)
        self.lands = pygame.sprite.Group(self.land1, self.land2,self.land3, self.land4)      

        # Menü seçenekleri
        self.start_btn = Button("BASLA", 60, 470, 100, 50, (50, 150, 50), (100, 200, 100), self.font)
        self.exit_btn = Button("ÇIKIŞ", 260, 470, 100, 50, (150, 50, 50), (200, 100, 100), self.font)
        
        self.buttons = [self.start_btn, self.exit_btn]

    def enter(self):
        print("Menüye girildi.")

    def exit(self):
        print("Menüden çıkılıyor.")

    def handle_events(self, events):
        for event in events:
            # Buton tıklamalarını kontrol et
            if self.start_btn.is_clicked(event):
                print("kaya")
            if self.exit_btn.is_clicked(event):
                pygame.quit()
                import sys
                sys.exit()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse_pos)
            
        self.lands.update()
        if len(self.lands) < 4:
            new_land = Land(400)
            self.lands.add(new_land)

    def draw(self, screen):
        screen.blit(self.bg,(0,0)) #Arka plan
        # draw metodunda (Butonlardan hemen önce, arkaplandan sonra çizdir)
        self.lands.draw(screen)
        screen.blit(self.bird,(164,200))
        
        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        title_surf = title_font.render("Flappy Bird", True, (255, 255, 255))
        title_surf1 = title_font.render("Flappy Bird", True, (0, 0, 0))
        screen.blit(title_surf1, (50, 80))
        screen.blit(title_surf, (52, 82))
        
        for btn in self.buttons:
            btn.draw(screen)