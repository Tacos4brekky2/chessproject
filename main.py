import pygame
from pygame.locals import *
import config
import setup as st
 
class App:
    def __init__(self):
        self._running = True
        self.screen = pygame.display.set_mode(st.SCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.board = pygame.Rect(0, 0, 600, 600)
 
    def main(self):
        # Event handler
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.render()

        self.cleanup()

    def cleanup(self):
        pygame.quit()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def render(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.board)
        pygame.display.update()


if __name__ == "__main__" :
    pygame.init()
    App().main()