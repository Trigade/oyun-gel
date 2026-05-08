import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, y, x=150):
        super().__init__()
        self.image = pygame.image.load(r"images\bird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz = 0

    def zipla(self):
        self.hiz = -8

    def update(self):
        self.hiz += 0.5
        self.rect.y += self.hiz