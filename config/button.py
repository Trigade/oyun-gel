import pygame

class Button:
    def __init__(self, image_path, x, y, width, height):
        # Resmi yükle ve belirtilen boyuta ölçekle
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))
        
        # Rect'i oluştur ve merkezini/konumunu ayarla
        # Çizim yaparken kolaylık olması için x ve y koordinatlarını buraya kaydediyoruz
        self.rect = self.image.get_rect(center=(x, y))
        self.is_hovered = False

    def update(self, mouse_pos):
        # Mouse resmin (rect) üzerinde mi kontrol et
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        # Butonu rect'in konumuna göre çiz (Böylece koordinatlar otomatik eşleşir)
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False