import pygame


class Land(pygame.sprite.Sprite):
    def __init__(self, x, y=544, hiz=3):
        super().__init__()
        self.image = pygame.image.load(r"images\land.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hiz = hiz
        self.genislik = self.image.get_width()

    def update(self):
        self.rect.x -= self.hiz

        if self.rect.right <= 0:
            self.kill()
