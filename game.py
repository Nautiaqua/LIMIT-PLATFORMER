import sys
import pygame
import json
import os

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("LimitJump!") # title for the window
        self.screen = pygame.display.set_mode((960, 864), vsync=1) # Initialize screen.
        self.surface = pygame.Surface((320, 288))
        self.clock = pygame.time.Clock() #initialize clocc

        self.movement = [False, False]
        self.noJumps = False
        self.levelReset = False

        # this handles the level loading.
        self.levelPath = "data/levels/"
        self.currentLevel = "hub" + ".json"
        # i have no clue why i dont use current level ngl

        # this loads in all the assets from the data folder.
        self.assets = {
            'block': load_images('tiles/block'),
            'sign': load_images('tiles/sign'),
            'spike': load_images('tiles/spike'),
            'door' : load_images('tiles/door'),
            'exitdoor': load_images('tiles/exitdoor'),
            'numbers': load_images('tiles/numbers'),
            'player': load_image('player/player_base.png')
        }

        # this part is for the jump popup thingymajigy
        self.font = pygame.font.SysFont('Arial', 20)
        self.popup_text = ''
        self.popup_timer = 120 #this is based on frames.

        self.tilemap = Tilemap(self, tile_size = 16) # for the sake of clarity.

        # replace this with main menu later on
        self.tilemap.load(self.levelPath + self.currentLevel)

        self.player = PhysicsEntity(self, 'player', 255, (50, 50), (15, 15))
        self.cTileType = 'None'
        
    def screen_wipe(self, duration=500, reverse=False):
        fade_surface = pygame.Surface(self.screen.get_size()).convert()
        fade_surface.fill((0, 0, 0))
        start_time = pygame.time.get_ticks()

        while True:
            now = pygame.time.get_ticks()
            elapsed = now - start_time
            if elapsed > duration:
                break

            alpha = min(255, int((elapsed / duration) * 255))
            fade_surface.set_alpha(alpha)

            # Redraw last frame behind the fade
            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_size()), (0, 0))
            self.screen.blit(fade_surface, (0, 0))

            pygame.display.update()
            self.clock.tick(60)

    def load_level(self, levelName, transition = False):
        if (transition):
            self.screen_wipe()
        self.tilemap.load(self.levelPath + levelName)
        self.noJumps = False
        self.player.pos = [50, 50]  # or a position from the level data
        self.player.JumpsLeft = json.load(open(self.levelPath + levelName)).get("maxjumps", 1)
        self.player.velocity = [0, 0]
        self.player.coyote_timer = 0
        self.currentLevel = levelName

    def hubappear(self):
        self.isHub = json.load(open(self.levelPath + self.currentLevel)).get("ishub", False)
        self.alreadyprinted = False

        self.hubFont = pygame.font.SysFont('Arial', 12)
        self.hubText = '^ this is your jump count.\ndo not let it run out!'
        self.hubTextTimer = 120
        
        # debug code lol
        if self.isHub and self.alreadyprinted == False:
            print("ITS THE HUB AREA")
            
        if self.hubTextTimer > 0 and self.isHub:
            hubText_surface = self.hubFont.render(self.hubText, True, (0, 0, 0))
            hubText_surface.set_alpha(100)
            text_rect = hubText_surface.get_rect(center=(160, 150)) 
            self.surface.blit(hubText_surface, text_rect)

    def run(self):
        while True:
            self.deltatime = self.clock.tick(60) / 1000
            self.surface.fill((174, 166, 145)) # fill the screen with the chosen color.

            self.levelReset = False
            # This is the initial jump count
            self.strJump = str(self.player.JumpsLeft)
            if (self.player.JumpsLeft == 255):
                self.popup_text = "∞"
                self.popup_timer = 60
            else:
                self.popup_text = self.strJump
                self.popup_timer = 60

            # --- THIS BLOCK OF CODE IS SPECIFICALLY FOR IF THE CURRENT LEVEL IS THE HUB AREA - START ---
            self.hubappear()


            # --- THIS BLOCK OF CODE IS SPECIFICALLY FOR IF THE CURRENT LEVEL IS THE HUB AREA - STOP ---
            
            self.tilemap.render(self.surface) #renders tilemap BEFORE player
            self.player.update(self.deltatime, self.tilemap, (self.movement[1] - self.movement[0], 0))  #moves player left and right
            self.player.render(self.surface) #renders player


            # renders the jump counter
            if self.popup_timer > 0:
                popup_surface = self.font.render(self.popup_text, True, (0, 0, 0))
                popup_surface.set_alpha(100)
                text_rect = popup_surface.get_rect(center=(160, 140)) 
                self.surface.blit(popup_surface, text_rect)
                self.popup_timer -= 1

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
                        # basically enables infinite jumps if jumps is set to 255
                        if (self.player.canJump == True and self.player.JumpsLeft == 255):
                            self.player.velocity[1] = -3
                            self.player.canJump = False
                            self.player.coyote_timer = 0

                        # now THIS is the code for the name of the game
                        if (self.player.canJump == True and self.player.JumpsLeft > 0):
                            self.player.velocity[1] = -3
                            self.player.canJump = False
                            self.player.JumpsLeft -= 1
                            self.player.coyote_timer = 0

                        if (self.noJumps == True):
                            self.load_level(self.currentLevel)
                        if (self.player.JumpsLeft == 0):
                            self.noJumps = True
                    if event.key == pygame.K_r:
                        self.load_level(self.currentLevel)

                    # debugger controls. these keybinds are here to help for debugging the game.
                    if event.key == pygame.K_l:
                        self.load_level("test2.json", True)
                        self.popup_text = 'Level Reset!'
                        self.popup_timer = 60
                    if event.key == pygame.K_p:
                        print(self.player.pos)

                    if event.key == pygame.K_o:
                        cTile = self.player.currentTileGet(self.tilemap, self.player.pos[0], self.player.pos[1])
                        if (cTile != None):
                            print(cTile['type'])
                            if (cTile['type'] == 'exitdoor'):
                                print("LEVEL EXIT")
                            
                    if event.key == pygame.K_i:
                        xTile = int((self.player.pos[0] + self.player.size[0] / 2) // self.tilemap.tile_size)
                        yTile = int((self.player.pos[0] + self.player.size[1] / 2) // self.tilemap.tile_size)
                        tilePos = str(xTile) + ";" + str(yTile)
                        currentTile = self.tilemap.tilemap.get(tilePos)
                        print(tilePos)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            scaled = pygame.transform.scale(self.surface, (960, 864))
            self.screen.blit(scaled, (0, 0))

            pygame.display.update()


Game().run()