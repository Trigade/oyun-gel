import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        pipe_height = 340
        self.is_top = is_top

        # Borunun üstte veya altta olmasına göre görseli yükle ve boyutlandır
        if is_top:
            self.image = pygame.image.load(
                r"images\pipe_green_down.png"
            ).convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, pipe_height))
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            self.image = pygame.image.load(r"images\pipe_green_up.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, pipe_height))
            self.rect = self.image.get_rect(midtop=(x, y))

        # Hassas çarpışma algılaması için maske oluştur
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3

    def update(self):
        # Boruyu sola doğru hareket ettir
        self.rect.x -= self.speed

        # Ekranın dışına çıkan boruyu bellekten sil
        if self.rect.right < -20:
            self.kill()
