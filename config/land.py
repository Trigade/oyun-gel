import pygame

class Land(pygame.sprite.Sprite):
    def __init__(self, x, y=544, hiz=4):
        super().__init__()
        # Görseli yükle
        self.image = pygame.image.load(r"images\land.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image,(200,56))
        # Görselin konumunu ve boyutunu belirle
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hiz = hiz
        self.genislik = self.image.get_width()

    def update(self):
        # Zemini sola doğru hareket ettir
        self.rect.x -= self.hiz
        
        # Eğer zemin tamamen ekranın dışına çıktıysa sağ tarafa geri dön
        if self.rect.right <= 0:
            self.kill()