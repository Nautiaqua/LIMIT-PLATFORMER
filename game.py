import sys
import pygame

from scripts.utils import load_image
from scripts.entities import PhysicsEntity

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Limited Jump Platformer") # title for the window
        self.screen = pygame.display.set_mode((640, 576)) # Initialize screen.
        self.surface = pygame.Surface((160, 144))
        self.clock = pygame.time.Clock() # Initialize clock.
        

        self.movement = [False, False]
        self.assets = {
            'player' : load_image('player/player_sprite_idle.png')
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (50, 50))

    def run(self):
        while True:
            self.surface.fill((174, 166, 145)) # fill the screen with the chosen color.

            self.player.update((self.movement[0] - self.movement[1], 0))  #moves player left and right
            self.player.render(self.surface) #renders player

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quits game, duh
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d: # d is left, a is right
                        self.movement[0] = True
                    if event.key == pygame.K_a:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    if event.key == pygame.K_a:
                        self.movement[1] = False

            scaled = pygame.transform.scale(self.surface, (640, 576))
            self.screen.blit(scaled, (0, 0))

            pygame.display.update()
            self.clock.tick(60) # sets frame rate to 60 fps

Game().run()