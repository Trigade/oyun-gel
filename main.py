import pygame
import sys
from config.menu_state import MenuState
from config.state_manager import StateManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("State Manager Projesi")
    clock = pygame.time.Clock()

    manager = StateManager()
    manager.push(MenuState(manager)) # İlk olarak menüyü aç

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Aktif durum varsa yönet
        if manager.active:
            manager.active.handle_events(events)
            manager.active.update()
            manager.active.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()