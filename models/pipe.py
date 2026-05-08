import pygame
from numpy import random

class Pipes(pygame.sprite.Sprite):
    def __init__(self, x, renk=(0, 102, 0)):
        super().__init__()
        self.boy = random.randint(100, 400)
        self.image = pygame.image.load(r"images\pipe.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, self.boy))
        self.rect = self.image.get_rect(midbottom=(x, 650))
        self.hiz = 3

    def update(self):
        self.rect.x -= self.hiz
        if self.rect.right < 0:
            self.kill()

class TopPipes(pygame.sprite.Sprite):
    def __init__(self, x,alfa):
            super().__init__()
            self.boy = 500
            self.image = pygame.image.load(r"images\pipe.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, self.boy-100))
            self.rect = self.image.get_rect(midbottom=(x, alfa))
            self.hiz = 3

    def update(self):
        self.rect.x -= self.hiz
        if self.rect.right < 0:
            self.kill()
