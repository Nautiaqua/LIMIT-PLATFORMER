import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Limited Jump Platformer") # title for the window
        self.screen = pygame.display.set_mode((640, 576)) # Initialize screen.
        self.surface = pygame.Surface((160, 144))
        self.clock = pygame.time.Clock() # Initialize clock.
        
        self.playersprite = pygame.image.load('data/sprites/player_sprite_idle.png')
        self.player_pos = [64, 64] # determines player position
        self.movement = [False, False]
        

        self.collission_area = pygame.Rect(80, 50, 20, 50)

    def run(self):
        while True:
            self.player_pos[0] += (self.movement[0] - self.movement[1]) * 2 # move player left or right, the numberdeterminesthemovement speed

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

                

            self.surface.fill((174, 166, 145)) # fill the screen with the chosen color.
            
            playercoll = pygame.Rect(self.player_pos[0], self.player_pos[1], self.playersprite.get_width(), self.playersprite.get_height()) # player collision
            if playercoll.colliderect(self.collission_area):
                pygame.draw.rect(self.surface,(0, 100, 255), self.collission_area)
            else:
                pygame.draw.rect(self.surface,(0, 50, 255), self.collission_area)

            self.surface.blit(self.playersprite, self.player_pos)

            scaled = pygame.transform.scale(self.surface, (640, 576))
            self.screen.blit(scaled, (0, 0))

            pygame.display.update()
            self.clock.tick(60) # sets frame rate to 60 fps

Game().run()