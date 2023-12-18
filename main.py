import pygame
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.resolution = self.width, self.height = 640, 400
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def render(self):
        pygame.display.update()
    def cleanup(self):
        pygame.quit()
 
    def main(self):
        if self.on_init() == False:
            self._running = False

        # Event handler
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.render()

        self.cleanup()
 

if __name__ == "__main__" :
    App().main()