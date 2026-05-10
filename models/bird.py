import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, y, x=120):
        super().__init__()
        self.size = (60, 60)
        # Kuşun animasyon karelerini yükle ve boyutlandır
        self.images = [
            pygame.transform.scale(
                pygame.image.load(r"images\bird_down.png").convert_alpha(), self.size
            ),
            pygame.transform.scale(
                pygame.image.load(r"images\bird_mid.png").convert_alpha(), self.size
            ),
            pygame.transform.scale(
                pygame.image.load(r"images\bird_up.png").convert_alpha(), self.size
            ),
        ]

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.hiz = 0
        self.animation_speed = 0.15

    def animation(self):
        # Animasyon kareleri arasında geçiş yap
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.index = 0

        raw_image = self.images[int(self.index)]

        # Dikey hıza göre kuşu döndür (-90 ile 30 derece arası)
        rotation_angle = -self.hiz * 3
        if rotation_angle > 30:
            rotation_angle = 30
        if rotation_angle < -90:
            rotation_angle = -90

        self.image = pygame.transform.rotate(raw_image, rotation_angle)

        # Dönme sonrası merkez noktasını koru ve maskeyi güncelle
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def zipla(self):
        # Yukarı doğru ivme ver
        self.hiz = -8

    def update(self):
        # Yerçekimi etkisi ve konum güncelleme
        self.hiz += 0.5
        self.rect.y += self.hiz
        self.animation()

        # Çarpışma algılaması için daraltılmış alan
        self.hitbox = self.rect.inflate(-25, -25)
