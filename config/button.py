import pygame


class Button:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.transform.scale(
            pygame.image.load(image_path).convert_alpha(), (width, height)
        )

        self.rect = self.image.get_rect(center=(x, y))
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
