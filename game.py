import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Limited Jump Platformer") # title for the window
        self.screen = pygame.display.set_mode((960, 864)) # Initialize screen.
        self.surface = pygame.Surface((320, 288))
        self.clock = pygame.time.Clock() #initialize clocc
        

        self.movement = [False, False]

        # This loads in all the assets from the data folder.
        self.assets = {
            'block': load_images('tiles/block'),
            'player': load_image('player/player_base.png')
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (15, 15))
        self.tilemap = Tilemap(self, tile_size = 16) # for the sake of clarity.

    def run(self):
        while True:
            self.surface.fill((174, 166, 145)) # fill the screen with the chosen color.

            self.tilemap.render(self.surface) #renders tilemap BEFORE player

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))  #moves player left and right
            self.player.render(self.surface) #renders player

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quits game, duh
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a: # d is left, a is right
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        if (self.player.canJump == True):
                            self.player.velocity[1] = -3
                            self.player.canJump = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            scaled = pygame.transform.scale(self.surface, (960, 864))
            self.screen.blit(scaled, (0, 0))

            pygame.display.update()
            self.clock.tick(60) # sets frame rate to 60 fps

Game().run()