import pygame

class Land(pygame.sprite.Sprite):
    def __init__(self,x,y=544,hiz=5):
        super().__init__()
        self.x = x
        self.image = pygame.image.load(r"images\land.png").convert_alpha()
        self.y = 544
        self.hiz = 5

    def update(self):
        pass